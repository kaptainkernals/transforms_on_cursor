# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####


bl_info = {
    "name": "Transform on Cursor",
    "author": "Kaptainkernals",
    "version": (0, 3),
    "blender": (2, 77, 0),
    "location": "3D view",
    "description": "Transform on cursor, rotate based on new orientation from selected vertices",
    "category": "3D View",
    }

import bpy

def rotate(context):
    # inspired by Mont29's pivot point cursor code
    space = context.space_data
    if space.type == 'VIEW_3D':
        obj = bpy.context.active_object
        back_pvpt = space.pivot_point
        space.pivot_point = 'CURSOR'
        bpy.ops.transform.rotate('INVOKE_DEFAULT')
        space.pivot_point = back_pvpt


def move(context):
    space = context.space_data
    if space.type == 'VIEW_3D':
        obj = bpy.context.active_object
        back_pvpt = space.pivot_point
        space.pivot_point = 'CURSOR'
        bpy.ops.transform.translate('INVOKE_DEFAULT')
        space.pivot_point = back_pvpt

def scale(context):
    space = context.space_data
    if space.type == 'VIEW_3D':
        obj = bpy.context.active_object
        back_pvpt = space.pivot_point
        space.pivot_point = 'CURSOR'
        bpy.ops.transform.resize('INVOKE_DEFAULT')
        space.pivot_point = back_pvpt

def orientation(context):
    space = context.space_data
    if space.type == 'VIEW_3D':
        saved_location = bpy.context.scene.cursor_location.copy()
        bpy.ops.transform.create_orientation(name="rotation_orientation", use=True, overwrite=True)
        bpy.ops.view3d.snap_cursor_to_selected()
        bpy.ops.mesh.select_all(action='SELECT')
        back_pvpt = space.pivot_point
        space.pivot_point = 'CURSOR'
        bpy.ops.transform.rotate('INVOKE_DEFAULT', constraint_axis=(False, True, False), constraint_orientation='rotation_orientation')
        bpy.ops.transform.delete_orientation()
        bpy.context.space_data.transform_orientation = 'GLOBAL'
        bpy.context.scene.cursor_location = saved_location
        space.pivot_point = back_pvpt


class RotateOnCursor(bpy.types.Operator):
    '''Rotate on Cursor'''
    bl_idname = "mesh.rotate_on_cursor"
    bl_label = "Rotate On Cursor"

    operator = bpy.props.StringProperty("")

    count = 0

    def modal(self, context, event):
        self.count += 1

        if self.count == 1:
            if self.operator == "Translate":
                move(context)
            if self.operator == "Rotate":
                rotate(context)
            if self.operator == "Scale":
                scale(context)
            if self.operator == "RotateOnOrientation":
                orientation(context)

        if event.type in {'X', 'Y', 'Z'}:
            return {'PASS_THROUGH'}

        if event.type in {'RIGHTMOUSE', 'ESC', 'LEFTMOUSE'}:
            return {'FINISHED'}

        return {'PASS_THROUGH'}

    def invoke(self, context, event):
        context.window_manager.modal_handler_add(self)
        return {'RUNNING_MODAL'}

addon_keymaps = []

def RegisterHotkeys():    
    kcfg = bpy.context.window_manager.keyconfigs.addon
    if kcfg:
        #EDIT MODE
        km = kcfg.keymaps.new(name='3D View', space_type='VIEW_3D')

        kmi = km.keymap_items.new("mesh.rotate_on_cursor", 'R', 'PRESS', shift=True, alt=True)
        kmi.properties.operator = "RotateOnOrientation"
        addon_keymaps.append((km, kmi))

        kmi = km.keymap_items.new("mesh.rotate_on_cursor", 'G', 'PRESS', shift=True, alt=True, ctrl=True)
        kmi.properties.operator = "Translate"
        addon_keymaps.append((km, kmi))

        kmi = km.keymap_items.new("mesh.rotate_on_cursor", 'R', 'PRESS', shift=True, alt=True, ctrl=True)
        kmi.properties.operator = "Rotate"
        addon_keymaps.append((km, kmi))

        kmi = km.keymap_items.new("mesh.rotate_on_cursor", 'S', 'PRESS', shift=True, alt=True, ctrl=True)
        kmi.properties.operator = "Scale"
        addon_keymaps.append((km, kmi))

        # OBJECT MODE
        km = kcfg.keymaps.new(name='Object Mode', space_type='VIEW_3D')
        kmi = km.keymap_items.new("mesh.rotate_on_cursor", 'G', 'PRESS', shift=True, alt=True, ctrl=True)
        kmi.properties.operator = "Translate"
        addon_keymaps.append((km, kmi))

        kmi = km.keymap_items.new("mesh.rotate_on_cursor", 'R', 'PRESS', shift=True, alt=True, ctrl=True)
        kmi.properties.operator = "Rotate"
        addon_keymaps.append((km, kmi))

        kmi = km.keymap_items.new("mesh.rotate_on_cursor", 'S', 'PRESS', shift=True, alt=True, ctrl=True)
        kmi.properties.operator = "Scale"
        addon_keymaps.append((km, kmi))

def UnRegisterHotkeys():
    for km, kmi in addon_keymaps:
        km.keymap_items.remove(kmi)
    addon_keymaps.clear()

def register():
    bpy.utils.register_class(RotateOnCursor)
    RegisterHotkeys()


def unregister():
    bpy.utils.unregister_class(RotateOnCursor)
    UnRegisterHotkeys()


if __name__ == "__main__":
    register()
    unregister()