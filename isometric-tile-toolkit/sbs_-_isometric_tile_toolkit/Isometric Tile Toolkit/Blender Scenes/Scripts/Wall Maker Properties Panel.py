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
        row.prop(context.scene.render, "resolution_x", text="X")
        row.prop(context.scene.render, "resolution_y", text="Y")

        row = layout.row()
        row.label(text="Material Texture:")

        row = layout.row()
        row.prop(context.object.active_material.node_tree.nodes["Image Texture"].image, "filepath")

        row = layout.row()
        row.operator("object.rotate_zero", text="Left Wall")
        row.operator("object.rotate_minus_90", text="Right Wall")

        row = layout.row()
        row.operator("render.render", text="Render")


class OBJECT_OT_RotateZero(bpy.types.Operator):
    bl_idname = "object.rotate_zero"
    bl_label = "Left Wall"

    def execute(self, context):
        plane = bpy.data.objects['Plane']
        plane.rotation_euler.z = 0
        return {'FINISHED'}

class OBJECT_OT_RotateMinus90(bpy.types.Operator):
    bl_idname = "object.rotate_minus_90"
    bl_label = "Right Wall"

    def execute(self, context):
        plane = bpy.data.objects['Plane']
        plane.rotation_euler.z = -1.5708
        return {'FINISHED'}

classes = [MyPanel, OBJECT_OT_RotateZero, OBJECT_OT_RotateMinus90]

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