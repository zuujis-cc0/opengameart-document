import bpy

class MyPanel(bpy.types.Panel):
    bl_idname = "OBJECT_PT_my_panel"
    bl_label = "Tile Properties"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Tile Properties"

    def draw(self, context):
        layout = self.layout
        obj = context.object

        row = layout.row()
        row.label(text="Render Size:")

        row = layout.row()
        row.prop(context.scene.render, "resolution_x", text="Resolution X")
        row.prop(context.scene.render, "resolution_y", text="Resolution Y")

        row = layout.row()
        row.label(text="Material Texture:")

        row = layout.row()
        row.prop(context.object.active_material.node_tree.nodes["Image Texture"].image, "filepath")

        row = layout.row()
        row.operator("object.rotate_left", text="Rotate Left")
        row.operator("object.rotate_right", text="Rotate Right")

        row = layout.row()
        row.operator("render.render", text="Render")

class OBJECT_OT_RotateLeft(bpy.types.Operator):
    bl_idname = "object.rotate_left"
    bl_label = "Rotate Left"

    def execute(self, context):
        cube = bpy.data.objects['Cube']
        cube.rotation_euler.z += 1.5708
        return {'FINISHED'}

class OBJECT_OT_RotateRight(bpy.types.Operator):
    bl_idname = "object.rotate_right"
    bl_label = "Rotate Right"

    def execute(self, context):
        cube = bpy.data.objects['Cube']
        cube.rotation_euler.z -= 1.5708
        return {'FINISHED'}

classes = [MyPanel, OBJECT_OT_RotateLeft, OBJECT_OT_RotateRight]

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)

if __name__ == "__main__":
    register()

# Get the Layout workspace
layout_workspace = bpy.data.workspaces['Layout']

# Get the first screen in the Layout workspace
layout_screen = layout_workspace.screens[0]

# Get the 3D Viewport in the Layout screen
for area in layout_screen.areas:
    if area.type == 'VIEW_3D':
        for space in area.spaces:
            if space.type == 'VIEW_3D':
                # Set the shading mode
                space.shading.type = 'RENDERED'

# Update the UI
bpy.context.view_layer.update()