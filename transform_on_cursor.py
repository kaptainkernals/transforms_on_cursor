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
    "author": "Mont29, Kaptainkernals",
    "version": (0, 1),
    "blender": (2, 77, 0),
    "location": "3D view",
    "description": "Rotate based on Cursor - based on cursor rotate script originally written by Mont29",
    "category": "3D View",
    }

import bpy

def cursor(context):
    space = context.space_data
    obj = bpy.context.active_object
    space.pivot_point = 'CURSOR'

def reset_cursor(context):
    space = context.space_data
    back_pvpt = space.pivot_point
    space.pivot_point = back_pvpt

def rotate(context):
    cursor(context)
    bpy.ops.transform.rotate('INVOKE_DEFAULT')
    reset_cursor(context)

def move(context):
    cursor(context)
    bpy.ops.transform.translate('INVOKE_DEFAULT')
    reset_cursor(context)

def scale(context):
    cursor(context)
    bpy.ops.transform.resize('INVOKE_DEFAULT')
    reset_cursor(context)


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


def register():
    bpy.utils.register_class(RotateOnCursor)
    bpy.utils.register_class(MoveOnCursor)
    bpy.utils.register_class(ScaleOnCursor)


def unregister():
    bpy.utils.unregister_class(RotateOnCursor)
    bpy.utils.unregister_class(MoveOnCursor)
    bpy.utils.unregister_class(ScaleOnCursor)


if __name__ == "__main__":
    register()