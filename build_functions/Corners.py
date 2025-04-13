import amulet
from amulet.api.block import Block
from amulet.utils.world_utils import block_coords_to_chunk_coords
from amulet_nbt import StringTag

# UL = Upper Left, UR = Upper Right, BL = Bottom Left, BR = Bottom Right

def place_block(level, position, block):
    """Place a block in the Amulet world."""
    x, y, z = position
    cx, cz = block_coords_to_chunk_coords(x, z)
    game_version = ("java", (1, 16, 20))
    chunk = level.get_chunk(cx, cz, "minecraft:overworld")
    offset_x, offset_z = x - 16 * cx, z - 16 * cz
    chunk.blocks[offset_x, y, offset_z] = level.block_palette.get_add_block(block)
    chunk.changed = True

def gen_ULCorner(level, position, corner, floor, height, length):
    x, y, z = position
    for h in range(height):
        # for x-axis
        for dx in range(length):
            place_block(level, (x + dx, y + h, z), corner)
        # for z-axis
        for dz in range(1, length): # Start from 1 to avoid placing on the same block
            place_block(level, (x, y + h, z + dz), corner)

    # Fill in the floor
    for dx in range(length):
        for dz in range(length):
            place_block(level, (x + dx, y, z + dz), floor)
    
    stair = Block("minecraft", "stone_brick_stairs", properties={"facing": StringTag("east")})
    for i in range(-1, length):
        place_block(level, (x, y + height, z+i), stair)
        place_block(level, (x-1, y + height-1, z+i), stair)
        place_block(level, (x+1, y + height+1, z+i), stair)
        place_block(level, (x+2, y + height+2, z+i), stair)


def gen_URCorner(level, position, corner, floor, height,length):
    x, y, z = position
    for h in range(height):
        for dx in range(length):
            place_block(level, (x - dx, y + h, z), corner)
        for dz in range(1, length):
            place_block(level, (x, y + h, z + dz), corner)

    for dx in range(length):
        for dz in range(length):
            place_block(level, (x - dx, y, z + dz), floor)

    stair = Block("minecraft", "stone_brick_stairs", properties={"facing": StringTag("west")})
    for i in range(-1, length):
        place_block(level, (x, y + height, z+i), stair)
        place_block(level, (x+1, y + height-1, z+i), stair)
        place_block(level, (x-1, y + height+1, z+i), stair)
        place_block(level, (x-2, y + height+2, z+i), stair)
        

def gen_BLCorner(level, position, corner, floor, height, length):
    x, y, z = position
    for h in range(height):
        for dx in range(length):
            place_block(level, (x + dx, y + h, z), corner)
        for dz in range(1, length):
            place_block(level, (x, y + h, z - dz), corner)

    for dx in range(length):
        for dz in range(length):
            place_block(level, (x + dx, y, z - dz), floor) 

    stair = Block("minecraft", "stone_brick_stairs", properties={"facing": StringTag("east")})
    for i in range(0, length +1):
        place_block(level, (x, y + height, z-i+1), stair)
        place_block(level, (x-1, y + height-1, z-i+1), stair)
        place_block(level, (x+1, y + height+1, z-i+1), stair)
        place_block(level, (x+2, y + height+2, z-i+1), stair)


def gen_BRCorner(level, position, corner, floor, height,length):
    x, y, z = position
    for h in range(height):
        for dx in range(length):
            place_block(level, (x - dx, y + h, z), corner)
        for dz in range(1, length):
            place_block(level, (x, y + h, z - dz), corner)
    
    for dx in range(length):
        for dz in range(length):
            place_block(level, (x - dx, y, z - dz), floor)

    stair = Block("minecraft", "stone_brick_stairs", properties={"facing": StringTag("west")})
    for i in range(0, length +1):
        place_block(level, (x, y + height, z-i+1), stair)
        place_block(level, (x+1, y + height-1, z-i+1), stair)
        place_block(level, (x-1, y + height+1, z-i+1), stair)
        place_block(level, (x-2, y + height+2, z-i+1), stair)
