import bpy
import mathutils
import math

# Set camera properties
cam_loc = mathutils.Vector((6, -6, 3))
cam_rot = mathutils.Euler((math.radians(60.0), 0, math.radians(-45.0)), 'XYZ')
cam_target = mathutils.Vector((0, 0, 0))

# Set render properties
render_res_x = 512
render_res_y = 256
render_scale = 100

# Set plane properties
plane_size = 2

# Set render engine
bpy.context.scene.render.engine = 'CYCLES'

# Delete default cube
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)

# Create plane
bpy.ops.mesh.primitive_plane_add(size=plane_size)

# Create camera
cam_data = bpy.data.cameras.new("Camera")
cam_obj = bpy.data.objects.new("Camera", cam_data)
bpy.context.scene.collection.objects.link(cam_obj)
bpy.context.scene.camera = cam_obj
cam_obj.data.type = 'ORTHO'
cam_obj.data.clip_end = 1000

# Position and aim camera
cam_obj.location = cam_loc
cam_obj.rotation_euler = cam_rot
cam_obj.select_set(True)
bpy.context.view_layer.objects.active = cam_obj
bpy.ops.view3d.camera_to_view_selected()

# Adjust camera orthographic scale
diag = math.sqrt(2 * (plane_size ** 2))
ortho_scale = diag
cam_obj.data.ortho_scale = ortho_scale

# Set render resolution and scale
bpy.context.scene.render.resolution_x = render_res_x
bpy.context.scene.render.resolution_y = render_res_y
bpy.context.scene.render.resolution_percentage = render_scale

# Set render region to match the plane
plane_bb = bpy.context.active_object.bound_box
x = (plane_bb[0][0] + plane_bb[1][0]) / 2
y = (plane_bb[0][1] + plane_bb[4][1]) / 2
w = abs(plane_bb[0][0] - plane_bb[1][0])
h = abs(plane_bb[0][1] - plane_bb[4][1])
bpy.context.scene.render.use_border = True
bpy.context.scene.render.border_min_x = x - w/2
bpy.context.scene.render.border_max_x = x + w/2
bpy.context.scene.render.border_min_y = y - h/2
bpy.context.scene.render.border_max_y = y + h/2

# Disable render region
bpy.context.scene.render.use_border = False

# Set pixel filter
bpy.context.scene.cycles.filter_width = 0.2

# Disable render denoise
bpy.context.scene.cycles.use_denoising = False

# Set transparent background
bpy.context.scene.render.film_transparent = True
