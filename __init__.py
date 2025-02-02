
bl_info = {
    "name": "Ramp Exporter",
    "author": "The Only Problem",
    "version": (1, 0, 0),
    "blender": (4, 1, 0),
    "location": "Shader Node Editor",
    "description": "Export ShaderNode 'ColorRamp' to a imagefile",
    "warning": "",
    "doc_url": "",
    "category": "Node",
}

import bpy
from . import operators
from . import interface
from . import properties

addon_keymaps = []

def register():
    properties.register()
    operators.register()
    interface.register()

    # handle the keymap
    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon
    if kc:
        km = kc.keymaps.new(name='Node Editor', space_type='NODE_EDITOR')
        kmi = km.keymap_items.new('node.ramp_export', 'E', 'PRESS', shift=True)
        addon_keymaps.append((km, kmi))

def unregister():
    for km, kmi in addon_keymaps:
        km.keymap_items.remove(kmi)
    addon_keymaps.clear()

    interface.unregister()
    operators.unregister()
    properties.unregister()
