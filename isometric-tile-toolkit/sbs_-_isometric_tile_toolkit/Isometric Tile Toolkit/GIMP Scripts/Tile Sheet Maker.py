import os
import glob
from gimpfu import *
import math

def create_tile_sheet(image_folder, tile_width, tile_height):
    # Create a new image for the tile sheet
    image = None
    num_columns = 8
    rows = 0
    columns = 0
    num_tiles = 0
    for i, file_path in enumerate(glob.glob(os.path.join(image_folder, '*.png'))):
        # Load the image
        img = pdb.gimp_file_load(file_path, file_path)

        # Create a new layer for the image
        if image is None:
            num_tiles = math.ceil(img.width / tile_width) * math.ceil(img.height / tile_height)
            num_rows = math.ceil(num_tiles / num_columns)
            image = pdb.gimp_image_new(tile_width * num_columns, tile_height * num_rows, RGB)
            layer = pdb.gimp_layer_new(image, tile_width, tile_height, RGBA_IMAGE, "Layer " + str(i), 100, NORMAL_MODE)
            pdb.gimp_image_add_layer(image, layer, 0)
        else:
            layer = pdb.gimp_layer_new(image, tile_width, tile_height, RGBA_IMAGE, "Layer " + str(i), 100, NORMAL_MODE)
            pdb.gimp_image_add_layer(image, layer, 0)

        # Add the image to the layer
        pdb.gimp_layer_set_offsets(layer, columns * tile_width, rows * tile_height)
        pdb.gimp_edit_copy(img.layers[0])
        floating_sel = pdb.gimp_edit_paste(layer, False)
        pdb.gimp_floating_sel_to_layer(floating_sel)

        # Increment the column and row counters
        columns += 1
        if columns >= num_columns:
            columns = 0
            rows += 1

        # Close the image
        pdb.gimp_image_delete(img)

    # Resize the image canvas
    if image is not None:
        new_height = rows * tile_height + tile_height # add one additional tile height for the last row
        pdb.gimp_image_resize(image, image.width, new_height, 0, 0)

        # Merge all visible layers
        merged_layer = pdb.gimp_image_merge_visible_layers(image, 0)

        pdb.gimp_display_new(image)
    else:
        pdb.gimp_message("Error: No images found in the specified folder.")

# Define the GIMP plugin function
def create_tile_sheet_plugin(image, drawable, image_folder, tile_width, tile_height):
    create_tile_sheet(image_folder, tile_width, tile_height)

# Register the plugin with GIMP
register(
    "python_fu_create_tile_sheet",
    "Create a tile sheet from a folder of images",
    "Create a tile sheet from a folder of images",
    "Screaming Brain Studios",
    "Screaming Brain Studios",
    "2023",
    "<Image>/Filters/Create Tile Sheet...",
    "*",
    [
        (PF_DIRNAME, "image_folder", "Image folder", ""),
        (PF_INT, "tile_width", "Tile width", 256),
        (PF_INT, "tile_height", "Tile height", 128)
    ],
    [],
    create_tile_sheet_plugin
)

# Start the plugin
main()