import bpy
from bpy.types import Panel, Menu
from . import operators
from . import properties

from bpy.types import Panel, Menu

class RAMP_UL_texslots_example(bpy.types.UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname):
        ob = data
        slot = item
        
        if self.layout_type in {'DEFAULT', 'COMPACT'}:
            # 859 : ramp icon
            layout.prop(item, "name", text=item.ramp_name, emboss=False, icon_value= 859)

        elif self.layout_type == 'GRID':
            layout.alignment = 'CENTER'
            layout.label(text="", icon_value=icon)

            
class RampExporterPanel(bpy.types.Panel):
    bl_idname = "NODE_PT_RampExporter"
    bl_space_type = 'NODE_EDITOR'
    bl_label = "Ramp Exporter"
    bl_region_type = "UI"
    bl_category = "Ramp Exporter"

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True
        layout.use_property_decorate = False
        
        layout.label(text="(Quick access: Shift+E)")
        
        ramp_settings = context.scene.ramp_settings
        layout.prop(ramp_settings, "width", text="Stripe Width")
        layout.prop(ramp_settings, "height",text="Stripe Height")
        layout.prop(ramp_settings,"exportMode",expand = True,text="Export Mode")

        
        scene = context.scene
        if ramp_settings.exportMode == "Multiple" :
            row = layout.row()
            

            
            row.template_list("RAMP_UL_texslots_example", "", scene, "collected_ramp", scene, "active_ramp_index")

            col = row.column(align=True)
            col.operator("node.ramp_slot_add", icon='ADD', text="")
            col.operator("node.ramp_slot_remove", icon='REMOVE', text="")

        
            
            col.separator()

            col.operator("object.material_slot_move", icon='TRIA_UP', text="").direction = 'UP'
            col.operator("object.material_slot_move", icon='TRIA_DOWN', text="").direction = 'DOWN'
            layout.prop(ramp_settings,"expandMode",text="Expand Mode")
        layout.separator()

        layout.operator("node.ramp_export", text="Export Ramp")


    @classmethod
    def poll(cls, context: bpy.types.Context):
        tree_type = context.space_data.tree_type
        return tree_type == 'ShaderNodeTree' or tree_type == 'CompositorNodeTree'
    
classes = [RampExporterPanel, 
           RAMP_UL_texslots_example
          ]

def register():
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)


def unregister():
    from bpy.utils import unregister_class

    for cls in classes:
        unregister_class(cls)