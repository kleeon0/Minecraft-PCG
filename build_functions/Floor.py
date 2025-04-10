import amulet
from amulet.api.block import Block
from amulet.utils.world_utils import block_coords_to_chunk_coords
from amulet_nbt import StringTag

# T = Top, Bottom, L = Left, R = Right

def place_block(level, position, block):
    """Place a block in the Amulet world."""
    x, y, z = position
    cx, cz = block_coords_to_chunk_coords(x, z)
    chunk = level.get_chunk(cx, cz, "minecraft:overworld")
    offset_x, offset_z = x - 16 * cx, z - 16 * cz
    chunk.blocks[offset_x, y, offset_z] = level.block_palette.get_add_block(block)
    chunk.changed = True

def gen_Floor(level, position, floor,wall,length, width, height):
    """Generate the inner floor that fills the area between the walls."""
    x, y, z = position
    # Fill the inner area with floor blocks (except the edges that are walls)
    for l in range(0, length):  # Exclude the first and last rows (along the length)
        for w in range(0, width):  # Exclude the first and last columns (along the width)
            place_block(level, (x + l, y, z + w), floor)
            place_block(level, (x + l, y + height + 1, z + w), wall)

'''    
# Example Usage:
world_path = "flat"
level = amulet.load_level(world_path)

# Define blocks
wall = Block("minecraft", "stone_bricks")
floor = Block("minecraft", "bamboo_planks")

# Set base position and height
origin = (140, 60)
base_y = -60
height = 3  # Adjustable height
length = 5  # Length of the rectangle
width = 5  # Width of the rectangle

gen_Floor(level, (origin[0]+2, base_y, origin[1]+2), floor, length, width, height)


# Save and close
level.save()
level.close()
'''