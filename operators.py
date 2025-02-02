import bpy
import numpy as np

class ExportManager(bpy.types.Operator):
    bl_idname = "node.ramp_export"
    bl_label = "ExportManager"

    bl_options = {'REGISTER', 'UNDO'}
    
    filepath: bpy.props.StringProperty(subtype="FILE_PATH")
    
    @classmethod
    def poll(cls, context: bpy.types.Context):
        return context.active_object is not None
    
    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}

    def execute(self, context: bpy.types.Context):
        # get export attribute
        ramp_settings = context.scene.ramp_settings
        if(ramp_settings.exportMode == "Single"):
            rampSrc = getActiveRamp()
            if rampSrc is not None:
                print("yes")
            else:
                self.report({'WARNING'}, "No Color Ramp node selected")
                print("Error: No Color Ramp node selected")
                return {'CANCELLED'}

            colors = getRampColors(rampSrc,ramp_settings.width)
            img = generateImage(colors,context)
            saveImage(img, file_path = self.filepath)
        
        else :
            colors = []
            #iterate the collection and fetch the ramp name
            collected_ramps = context.scene.collected_ramp
            ramp_num = len(collected_ramps)

            if ramp_num == 0:
                self.report({'ERROR'}, "Color Ramp List is empty")
                print("Error: No Color Ramp node selected")
                return {'CANCELLED'}
            
            else :
                for item in collected_ramps:
                    name = item.ramp_name
                    ramp_item = ramp_dict[name]
                    item_colors = getRampColors(ramp_item,ramp_settings.width)
                    appendImageColors(colors,item_colors)
                
            img = generateImage(colors,context)
            saveImage(img, file_path = self.filepath)
                
        self.report({'INFO'}, "Image saved successfully")
        return {'FINISHED'}

def generateSamplePoints(num):  
    step = 1.0 / (num - 1)
    return [i * step for i in range(num)]


def getRampColors(ramp,stripe_width):
    # get the color ramp
    colors = []

    positions = generateSamplePoints(stripe_width)
    for position in positions:
        color_elem = ramp.color_ramp.evaluate(position)
        colors.append(color_elem[0:4])

    return colors

def generateImage(colors,context: bpy.types.Context):

    ramp_settings = context.scene.ramp_settings
    collected_ramps = context.scene.collected_ramp
    
    width = ramp_settings.width
    height = ramp_settings.height

    #if is single len(colors)=width
    #else len(colors)=stepwidth
    if (ramp_settings.exportMode == 'Single') :
        img = bpy.data.images.new('color_ramp', width, height)
        pixels = [channel for color in colors for channel in color]
        
        # for j in range(3):
        #     for i in range(len(pixels)):
        #         pixels.append(pixels[i])
        
        for i in range(height - 1):
            for j in range(width * 4):
                pixels.append(pixels[j])

        img.pixels = pixels
        
        return img
    
    elif (ramp_settings.expandMode == 'Vertical'):
        img = bpy.data.images.new('color_ramp', width , height * len(collected_ramps))
        
        pixels = []
        
        for i in range(len(collected_ramps)):
            for k in range(height):
                for j in range(ramp_settings.width):
                    color = colors[ramp_settings.width * i+j]
                    pixels.extend(color[0:4])
            
        img.pixels = pixels
        return img
    
    else :
        img = bpy.data.images.new('color_ramp', width * len(collected_ramps) , height)
        pixels = [channel for color in colors for channel in color]
        
        for i in range(height - 1):
            for j in range(width * 4 * len(collected_ramps)):
                pixels.append(pixels[j])
                
        img.pixels = pixels
        return img
        

def appendImageColors(colors,item_colors):
    for color_elem in item_colors:
        colors.append(color_elem[0:4])
        
    return colors
    
def saveImage(img, file_path):
    
    img.save(filepath = file_path)
    img.file_format = 'PNG'

    print("Image saved successfully")

def getActiveRamp():
    # get node editor space
    space = bpy.context.space_data
    if not space:
        return None

    # get node tree
    node_tree = space.edit_tree
    if not node_tree:
        return None

    # get selected nodes
    selected_nodes = [node for node in node_tree.nodes if node.select]
    if not selected_nodes:
        return None

    # judge if the selected node is a Color Ramp node
    for node in selected_nodes:
        if node.type == 'VALTORGB':
            return node

    return None

def format_ramp_name(index):
    return f"ramp{index:03d}"

class AddRamp(bpy.types.Operator):
    bl_idname = "node.ramp_slot_add"
    bl_label = "addRampSlot"

    bl_options = {'REGISTER', 'UNDO'}
    
    
    @classmethod
    def poll(cls, context: bpy.types.Context):
        return True

    def execute(self, context: bpy.types.Context):
        collected_ramps = context.scene.collected_ramp
        
        # TODO: add a ramp slot and save it to dic
        # ensure selected node is a color ramp node
        new_ramp = context.scene.collected_ramp.add()

        context.scene.active_ramp_index = len(collected_ramps) - 1
        new_ramp.ramp_name = format_ramp_name(context.scene.active_ramp_index)
        self.report({'INFO'}, "rampname: "+str(new_ramp.ramp_name))
        
        ramp_tex = getActiveRamp()
        addRampToDict(new_ramp.ramp_name,ramp_tex)

        return {'FINISHED'}
    
class RemoveRamp(bpy.types.Operator):
    bl_idname = "node.ramp_slot_remove"
    bl_label = "removeRampSlot"

    bl_options = {'REGISTER', 'UNDO'}
    
    
    @classmethod
    def poll(cls, context: bpy.types.Context):
        return True

    def execute(self, context: bpy.types.Context):
        active_ramp_index = context.scene.active_ramp_index
        collected_ramps = context.scene.collected_ramp
        
        #TODO: remove a ramp slot and delete it from dic
        collected_ramps.remove(active_ramp_index)
        #if ai is 0 and len>0 dont need to change
        #if ai is 1 and len=6 dont need
        #id ai is tail and len>0

        if context.scene.active_ramp_index == len(collected_ramps):
            context.scene.active_ramp_index -= 1
        else: 
            removeRampFromDict(collected_ramps[context.scene.active_ramp_index].ramp_name)      
        return {'FINISHED'}
    
ramp_dict = {}

def addRampToDict(ramp_name, ramp_tex):
    ramp_dict[ramp_name] = ramp_tex
    
def removeRampFromDict(ramp_name):
    del ramp_dict[ramp_name]
    
classes = [ExportManager,AddRamp,RemoveRamp]


def register():
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)


def unregister():
    from bpy.utils import unregister_class

    for cls in classes:
        unregister_class(cls)