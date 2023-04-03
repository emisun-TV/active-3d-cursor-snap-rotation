bl_info = {
    "name": "Active 3D Cursor Snap Rotation",
    "description": "Lets you snap active object/bone or 3D cursor with rotation",
    "author": "Emil Sundström",
    "version": (1, 0, 0),
    "blender": (3, 4, 0),
    "location": "Object/Pose > Snap",
    "support": "COMMUNITY",
    "category": "Snapping Menu"
}

import bpy

class SnapCursorToActiveRotationOperator(bpy.types.Operator):
    """Lets you set the rotation of the 3D cursor from the active object"""

    bl_idname = "view3d.snap_cursor_to_active_rotation"
    bl_label = "Snap Cursor To Active Rotation"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        if bpy.context.active_pose_bone is not None:
            bpy.context.scene.cursor.matrix = bpy.context.active_pose_bone.id_data.matrix_world @ bpy.context.active_pose_bone.matrix
        elif bpy.context.active_object is not None:
            bpy.context.scene.cursor.matrix = bpy.context.active_object.matrix
        bpy.context.scene.cursor.rotation_mode = bpy.context.scene.cursor.rotation_mode
        bpy.context.view_layer.update()
        return {'FINISHED'}

class SnapActiveToCursorRotation(bpy.types.Operator):
    """Lets you snap the active object to the 3D cursor with rotation"""
    
    bl_idname = "view3d.snap_active_to_cursor_rotation"
    bl_label = "Snap Active To Cursor Rotation"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        if bpy.context.active_pose_bone is not None:
            scale = bpy.context.active_pose_bone.scale.copy()
            bpy.context.active_pose_bone.matrix = bpy.context.active_pose_bone.id_data.matrix_world.inverted_safe() @ bpy.context.scene.cursor.matrix
            print(scale)
            bpy.context.active_pose_bone.scale = scale
        elif bpy.context.active_object is not None:
            scale = bpy.context.active_object.scale.copy()
            bpy.context.active_object.matrix_world = bpy.context.scene.cursor.matrix
            bpy.context.active_object.scale = scale
        bpy.context.view_layer.update()
        return {'FINISHED'}

def menu_func(self, context):
    self.layout.operator(SnapCursorToActiveRotationOperator.bl_idname, text="Cursor To Active Rotation")
    self.layout.operator(SnapActiveToCursorRotation.bl_idname, text="Active To Cursor Rotation")


def register():
    bpy.utils.register_class(SnapCursorToActiveRotationOperator)
    bpy.utils.register_class(SnapActiveToCursorRotation)
    bpy.types.VIEW3D_MT_snap.append(menu_func)


def unregister():
    bpy.utils.unregister_class(SnapCursorToActiveRotationOperator)
    bpy.utils.unregister_class(SnapActiveToCursorRotation)
    bpy.types.VIEW3D_MT_snap.remove(menu_func)


if __name__ == "__main__":
    register()