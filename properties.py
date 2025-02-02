import bpy

from bpy.props import(
    IntProperty,
    PointerProperty,
    CollectionProperty,
    StringProperty,
    EnumProperty,
)

class RampTexPropertyGroup(bpy.types.PropertyGroup):
    width: IntProperty(name="Width", default=256, min=1)
    height: IntProperty(name="Height", default=1, min=1)
    expandMode : EnumProperty(
        name="ExpandMode",description = "expand mode",
        items=[("Vertical","Vertical",""),
               ("Horizentol","Horizontal","")]
    )
    exportMode : EnumProperty(
        name="ExportMode",description = "export mode",
        items=[("Single","Single",""),
               ("Multiple","Multiple","")]
)

class RampNamePropertyGroup(bpy.types.PropertyGroup):
    ramp_name : StringProperty(default = "ramp")
  

classes=[RampTexPropertyGroup,RampNamePropertyGroup]

def register():
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)

    bpy.types.Scene.ramp_settings = PointerProperty(type=RampTexPropertyGroup)
    bpy.types.Scene.collected_ramp = CollectionProperty(type= RampNamePropertyGroup)
    bpy.types.Scene.active_ramp_index = IntProperty(default = -1)

def unregister():
    from bpy.utils import unregister_class
    for cls in classes:
        unregister_class(cls)
    
    del bpy.types.Scene.ramp_settings
    del bpy.types.Scene.collected_ramp
    del bpy.types.Scene.active_ramp_index