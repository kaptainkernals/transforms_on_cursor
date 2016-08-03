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
    "description": "Rotate on cursor based on Mont29's pivot point cursor code, rotate based on new orientation based on selected vertices",
    "category": "3D View",
    }

import bpy

def rotate(context):
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
        bpy.ops.transform.rotate('INVOKE_DEFAULT')
        bpy.ops.transform.delete_orientation()
        bpy.context.space_data.transform_orientation = 'GLOBAL'
        bpy.context.scene.cursor_location = saved_location
        space.pivot_point = back_pvpt


class RotateOnCursor(bpy.types.Operator):
    '''Rotate on Cursor'''
    bl_idname = "mesh.rotate_on_cursor"
    bl_label = "Rotate On Cursor"

    @classmethod
    def poll(cls, context):
        return context.active_object != None

    def execute(self, context):
        rotate(context)
        return {'FINISHED'}

class MoveOnCursor(bpy.types.Operator):
    '''Move on Cursor'''
    bl_idname = "mesh.move_on_cursor"
    bl_label = "Move On Cursor"

    @classmethod
    def poll(cls, context):
        return context.active_object != None

    def execute(self, context):
        move(context)
        return {'FINISHED'}

class ScaleOnCursor(bpy.types.Operator):
    '''Scale on Cursor'''
    bl_idname = "mesh.scale_on_cursor"
    bl_label = "Scale On Cursor"

    @classmethod
    def poll(cls, context):
        return context.active_object != None

    def execute(self, context):
        scale(context)
        return {'FINISHED'}

class RotateOnOrientation(bpy.types.Operator):
    '''Rotate on Orientation'''
    bl_idname = "mesh.rotate_on_orientation"
    bl_label = "Rotate On Orientation"

    @classmethod
    def poll(cls, context):
        return context.active_object != None

    def execute(self, context):
        orientation(context)
        return {'FINISHED'}


def register():
    bpy.utils.register_class(RotateOnCursor)
    bpy.utils.register_class(MoveOnCursor)
    bpy.utils.register_class(ScaleOnCursor)
    bpy.utils.register_class(RotateOnOrientation)


def unregister():
    bpy.utils.unregister_class(RotateOnCursor)
    bpy.utils.unregister_class(MoveOnCursor)
    bpy.utils.unregister_class(ScaleOnCursor)
    bpy.utils.unregister_class(RotateOnOrientation)


if __name__ == "__main__":
    register()