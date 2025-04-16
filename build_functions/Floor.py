import amulet
from amulet.api.block import Block
from amulet.utils.world_utils import block_coords_to_chunk_coords
from amulet_nbt import StringTag

# Orientation is facing North

# Core function to place blocks in the world
# Uses Amulet API to handle block placement
def place_block(level, position, block):
    """Place a block in the Amulet world."""
    x, y, z = position
    cx, cz = block_coords_to_chunk_coords(x, z)
    chunk = level.get_chunk(cx, cz, "minecraft:overworld")
    offset_x, offset_z = x - 16 * cx, z - 16 * cz
    chunk.blocks[offset_x, y, offset_z] = level.block_palette.get_add_block(block)
    chunk.changed = True

# Function to generate the inner floor
# fills the area between the walls
#
def gen_Floor(level, position, floor, length, width, height):
    x, y, z = position

    # Define the block properties being used
    slab1 = Block("minecraft", "stone_brick_slab", properties={"type": StringTag("bottom")})
    slab2 = Block("minecraft", "stone_brick_slab", properties={"type": StringTag("top")})

    # Placing the floor
    for l in range(0, length):  # Exclude the first and last rows 
        for w in range(0, width):  # Exclude the first and last columns 
            place_block(level, (x + l, y, z + w), floor)

    # Placing the roof
    x_length = x + length
    y_height = y + height
    for dz in range( width):
        place_block(level, (x_length - 1, y_height + 3, z + dz), slab2)
        place_block(level, (x_length - 1, y_height + 4, z + dz), wall)
        place_block(level, (x_length - 2, y_height + 4, z + dz), wall)
        place_block(level, (x_length - 2, y_height + 5, z + dz), slab1)
        place_block(level, (x_length - 3, y_height + 5, z + dz), wall)
        place_block(level, (x_length - 4, y_height + 5, z + dz), slab1)
        place_block(level, (x_length - 4, y_height + 4, z + dz), wall)
        place_block(level, (x_length - 5, y_height + 4, z + dz), wall)
        place_block(level, (x_length - 5, y_height + 3, z + dz), slab2)

    
