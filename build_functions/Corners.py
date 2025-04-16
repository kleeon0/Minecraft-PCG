import amulet
from amulet.api.block import Block
from amulet.utils.world_utils import block_coords_to_chunk_coords
from amulet_nbt import StringTag

# UL = Upper Left, UR = Upper Right, BL = Bottom Left, BR = Bottom Right
# Orientation is facing North

# Core function to place blocks in the world
# Uses Amulet API to handle block placement
def place_block(level, position, block):
    x, y, z = position
    cx, cz = block_coords_to_chunk_coords(x, z)
    chunk = level.get_chunk(cx, cz, "minecraft:overworld")
    offset_x, offset_z = x - 16 * cx, z - 16 * cz
    chunk.blocks[offset_x, y, offset_z] = level.block_palette.get_add_block(block)
    chunk.changed = True

# for building the upper left corner
#
def gen_ULCorner(level, position, corner, floor, height, length):
    x, y, z = position

    # define the block properties being used
    wall = Block("minecraft", "stone_brick_wall")
    # Left-side uses east-facing stairs
    stair = Block("minecraft", "stone_brick_stairs", properties={"facing": StringTag("east")})
    under = Block("minecraft", "stone_brick_stairs", properties={"facing": StringTag("west"),
                                                                "half": StringTag("top") })  
    slab = Block("minecraft", "stone_brick_slab", properties={"type": StringTag("bottom")})

    height_y = y + height
    z_minus = z - 1

    # Wall placing
    for h in range(height):
        for dx in range(length):
            place_block(level, (x + dx, y + h, z), corner) # x-axis
        for dz in range(1, length):
            place_block(level, (x, y + h, z + dz), corner) # z-axis
        for dy in range(height):
            place_block(level, (x, y + dy, z_minus), wall) # outer wall frame

    # Floor placing
    for dx in range(length):
        place_block(level, (x + dx, height_y, z_minus), corner) # frame
        for dz in range(length):
            place_block(level, (x + dx, y, z + dz), floor) # floor
    
    # Roof placing
    # ** List of tuples could also be used instead of below
    # ** Method below is used for easier editing
    # ** Applies to all similar situations
    for i in range(-1, length):
        place_block(level, (x, height_y, z+i), stair)
        place_block(level, (x+1, height_y+1, z+i), stair)
        place_block(level, (x+2, height_y+2, z+i), stair)
        place_block(level, (x+3, height_y+3, z+i), stair)
        place_block(level, (x+4, height_y+3, z+i), under)
        place_block(level, (x+4, height_y+4, z+i), slab)
    # Roof underside
    place_block(level, (x+2, height_y + 1, z_minus), under)
    place_block(level, (x+3, height_y + 2, z_minus), under)
    place_block(level, (x+4, height_y + 3, z_minus), under)

    # Frame filler
    for i in range(height - 1):
        for dx in range(length - 1 - i):
            place_block(level, (x + dx + i + 1, y + h + i + 1, z), floor)


# for building the upper right corner
#
def gen_URCorner(level, position, corner, floor, height,length):
    x, y, z = position

    # define the block properties being used
    wall = Block("minecraft", "stone_brick_wall")
    stair = Block("minecraft", "stone_brick_stairs", properties={"facing": StringTag("west")})
    under = Block("minecraft", "stone_brick_stairs", properties={"facing": StringTag("east"),
                                                                "half": StringTag("top") }) 
    slab = Block("minecraft", "stone_brick_slab", properties={"type": StringTag("bottom")})

    height_y = y + height
    z_minus = z - 1

    # Wall placing
    for h in range(height):
        for dx in range(length):
            place_block(level, (x - dx, y + h, z), corner)  # x-axis
        for dz in range(1, length):
            place_block(level, (x, y + h, z + dz), corner)  # z-axis
        for dy in range(height):
            place_block(level, (x, y + dy, z_minus), wall)  # outer wall frame

    # Floor placing
    for dx in range(length):
        place_block(level, (x - dx, height_y, z_minus), corner) # frame
        for dz in range(length):
            place_block(level, (x - dx, y, z + dz), floor) # floor

    # Roof placing
    for i in range(-1, length):
        place_block(level, (x, height_y, z+i), stair)
        place_block(level, (x-1, height_y+1, z+i), stair)
        place_block(level, (x-2, height_y+2, z+i), stair)
        place_block(level, (x-3, height_y+3, z+i), stair)
        place_block(level, (x-4, height_y + 3, z+i), under)
        place_block(level, (x-4, height_y+4, z+i), slab)
    # Roof underside
    place_block(level, (x-2, height_y + 1, z_minus), under)
    place_block(level, (x-3, height_y + 2, z_minus), under)
    place_block(level, (x-4, height_y + 3, z_minus), under)

    #Frame filler
    for i in range(height - 1):
        for dx in range(length - 1 - i):
            place_block(level, (x - dx - i - 1, y + h + i + 1, z), floor)

        
# for building the bottom left corner
#
def gen_BLCorner(level, position, corner, floor, height, length):
    x, y, z = position

    # define the block properties being used
    wall = Block("minecraft", "stone_brick_wall")
    stair = Block("minecraft", "stone_brick_stairs", properties={"facing": StringTag("east")})
    under = Block("minecraft", "stone_brick_stairs", properties={"facing": StringTag("west"),
                                                                "half": StringTag("top") })  
    slab = Block("minecraft", "stone_brick_slab", properties={"type": StringTag("bottom")})

    height_y = y + height
    z_plus = z + 1

    # Wall placing
    for h in range(height):
        for dx in range(length):
            place_block(level, (x + dx, y + h, z), corner) # x-axis
        for dz in range(1, length):
            place_block(level, (x, y + h, z - dz), corner) # z-axis
        for dy in range(height):
            place_block(level, (x, y + dy, z_plus), wall) # outer wall frame

    # Floor placing
    for dx in range(length):
        place_block(level, (x + dx, height_y, z_plus), corner) # frame
        for dz in range(length):
            place_block(level, (x + dx, y, z - dz), floor) # floor

    # Roof placing
    for i in range(0, length +1):
        place_block(level, (x, height_y, z_plus - i), stair)
        place_block(level, (x+1, height_y + 1, z_plus - i), stair)
        place_block(level, (x+2, height_y + 2, z_plus - i), stair)
        place_block(level, (x+3, height_y + 3, z_plus - i), stair)
        place_block(level, (x+4, height_y + 3, z_plus - i), under)
        place_block(level, (x+4, height_y + 4, z_plus - i), slab)
    # Roof underside
    place_block(level, (x+2, height_y + 1, z_plus), under)
    place_block(level, (x+3, height_y + 2, z_plus), under)
    place_block(level, (x+4, height_y + 3, z_plus), under)

    # Frame filler
    for i in range(height - 1):
        for dx in range(length - 1 - i):
            place_block(level, (x + dx + i + 1, y + h + i + 1, z), floor)


# for building the bottom right corner
#
def Gen_BRCorner(level, position, corner, floor, height,length):
    x, y, z = position
    
    # define the block properties being used
    stair = Block("minecraft", "stone_brick_stairs", properties={"facing": StringTag("west")})
    under = Block("minecraft", "stone_brick_stairs", properties={"facing": StringTag("east"),
                                                                "half": StringTag("top") }) 
    slab = Block("minecraft", "stone_brick_slab", properties={"type": StringTag("bottom")})
    wall = Block("minecraft", "stone_brick_wall")
    
    height_y = y + height
    z_plus = z + 1

    # Wall placing
    for h in range(height):
        for dx in range(length):
            place_block(level, (x - dx, y + h, z), corner) # x-axis
        for dz in range(1, length):
            place_block(level, (x, y + h, z - dz), corner) # z-axis
        for dy in range(height):
            place_block(level, (x, y + dy, z_plus), wall) # outer wall frame
    
    # Floor placing
    for dx in range(length):
        place_block(level, (x - dx, height_y, z_plus), corner) # frame
        for dz in range(length):
            place_block(level, (x - dx, y, z - dz), floor) # floor

    # Roof placing
    for i in range(0, length +1):
        place_block(level, (x, height_y, z_plus-i), stair)
        place_block(level, (x-1, height_y+1, z_plus-i), stair)
        place_block(level, (x-2, height_y+2, z_plus-i), stair)
        place_block(level, (x-3, height_y+3, z_plus-i), stair)
        place_block(level, (x-4, height_y+3, z_plus-i), under)
        place_block(level, (x-4, height_y+4, z_plus-i), slab)
    # Roof underside
    place_block(level, (x, height_y-1, z_plus), wall)
    place_block(level, (x-2, height_y+1, z_plus), under)
    place_block(level, (x-3, height_y+2, z_plus), under)

    # Frame filler
    for i in range(height - 1):
        for dx in range(length - 1 - i):
            place_block(level, (x - dx - i - 1, y + h + i + 1, z), floor)
