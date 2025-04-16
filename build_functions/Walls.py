import amulet
from amulet.api.block import Block
from amulet.utils.world_utils import block_coords_to_chunk_coords
from amulet_nbt import StringTag

# T = Top, Bottom, L = Left, R = Right
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

# for building the top wall
#
def gen_TopWall(level, position, wall, floor, height, length, width):
    x, y, z = position

    # define the block properties being used
    slab1 = Block("minecraft", "stone_brick_slab", properties={"type": StringTag("bottom")})
    slab2 = Block("minecraft", "stone_brick_slab", properties={"type": StringTag("top")})

    # Placing the wall 
    for l in range(length):
        for h in range(height):
            place_block(level, (x + l, y + h, z), wall)

    # Placing the floor 
    for l in range(0, length):  
        place_block(level, (x + l, y, z +1), floor)
        for w in range(1, width):  
            place_block(level, (x + l, y, z + w), floor)

    x_length = x + length
    y_height = y + height
    z_minus = z - 1

    # Placing the roof
    for dz in range(-1, width):
        place_block(level, (x_length - 1, y_height + 3, z + dz), slab2)
        place_block(level, (x_length - 1, y_height + 4, z + dz), wall)
        place_block(level, (x_length - 2, y_height + 4, z + dz), wall)
        place_block(level, (x_length - 2, y_height + 5, z + dz), slab1)
        place_block(level, (x_length - 3, y_height + 5, z + dz), wall)
        place_block(level, (x_length - 4, y_height + 5, z + dz), slab1)
        place_block(level, (x_length - 4, y_height + 4, z + dz), wall)
        place_block(level, (x_length - 5, y_height + 4, z + dz), wall)
        place_block(level, (x_length - 5, y_height + 3, z + dz), slab2)
    # Topmost block underneath the roof
    place_block(level, (x_length - 3, y_height + 4, z), floor)
    
    # Placing the outer frame
    for h in range(height+1):
        place_block(level, (x, y + h, z_minus), wall)
        place_block(level, (x + height-1, y + h, z_minus), wall)

    # Filling the backboard
    for l in range(length):
        for k in range(height-1):
            place_block(level, (x + l, y_height + k, z), floor)


# for building the bottom wall
# 
def gen_BottomWall(level, position, wall, floor, height, length, width):
    x, y, z = position

    # Define the block properties being used
    slab1 = Block("minecraft", "stone_brick_slab", properties={"type": StringTag("bottom")})
    slab2 = Block("minecraft", "stone_brick_slab", properties={"type": StringTag("top")})

    # Placing the wall
    for l in range(length):
        for h in range(height):
            place_block(level, (x + l , y + h, z + width - 1), wall)
    
    # Placing the floor
    for l in range(0, length):  
        place_block(level, (x + l, y, z + width -2), floor) 
        for w in range(width-1):
            place_block(level, (x + l, y, z + w), floor) 

    x_length = x + length
    y_height = y + height

    # Placing the roof
    for dz in range(0, width+1):
        place_block(level, (x_length - 1, y_height + 3, z + dz), slab2)
        place_block(level, (x_length - 1, y_height + 4, z + dz), wall)
        place_block(level, (x_length - 2, y_height + 4, z + dz), wall)
        place_block(level, (x_length - 2, y_height + 5, z + dz), slab1)
        place_block(level, (x_length - 3, y_height + 5, z + dz), wall)
        place_block(level, (x_length - 4, y_height + 5, z + dz), slab1)
        place_block(level, (x_length - 4, y_height + 4, z + dz), wall)
        place_block(level, (x_length - 5, y_height + 4, z + dz), wall)
        place_block(level, (x_length - 5, y_height + 3, z + dz), slab2)
    place_block(level, (x_length - 3, y_height + 4, z+l), floor)

    # Backboard
    for k in range(height-1):
        for l in range(length):
            place_block(level, (x + l, y_height + k, z + width - 1), floor)


# for building the left wall
#
def gen_LeftWall(level, position, wall, floor, height, length, width):
    x, y, z = position

    # Define the block properties being used
    under = Block("minecraft", "stone_brick_stairs", properties={"facing": StringTag("west"),
                                                                "half": StringTag("top") })  
    slab = Block("minecraft", "stone_brick_slab", properties={"type": StringTag("bottom")})
    stair = Block("minecraft", "stone_brick_stairs", properties={"facing": StringTag("east")})

    # Place the left wall
    for l in range(width):
        for h in range(height):
            place_block(level, (x, y + h, z + l), wall)

    # Place the floor
    for l in range(0, length):  
        place_block(level, (x+1, y, z + l), floor)
        for w in range(1, width):  
            place_block(level, (x + w, y, z + l), floor)
        
        # Placing the roof 
        y_height = y + height  
        place_block(level, (x, y_height, z+l), stair)
        place_block(level, (x+1, y_height + 1, z+l), stair)
        place_block(level, (x+2, y_height + 2, z+l), stair)
        place_block(level, (x+3, y_height + 3, z+l), stair)
        place_block(level, (x+4, y_height + 3, z+l), under)
        place_block(level, (x+4, y_height + 4, z+l), slab)


# for building the right wall
#
def gen_RightWall(level, position, wall, floor, height, length, width):
    x, y, z = position

    # Define the block properties being used
    under = Block("minecraft", "stone_brick_stairs", properties={"facing": StringTag("east"),
                                                                "half": StringTag("top") })  
    slab = Block("minecraft", "stone_brick_slab", properties={"type": StringTag("bottom")})
    stair = Block("minecraft", "stone_brick_stairs", properties={"facing": StringTag("west")})
    
    # Placing the wall
    for l in range(width):
        for h in range(height):
            place_block(level, (x + length - 1, y + h, z + l), wall)
    
    # Placing the floor
    for l in range(0, length):  
        place_block(level, (x + length - 2, y, z + l), floor)
        for w in range(width-1):  
            place_block(level, (x + w, y, z + l), floor)

        # Placing the roof
        x_length = x + length
        y_height = y + height
        place_block(level, (x_length-1, y_height, z+l), stair)
        place_block(level, (x_length-2, y_height + 1, z+l), stair)
        place_block(level, (x_length-3, y_height + 2, z+l), stair)
        place_block(level, (x_length-4, y_height + 3, z+l), stair)
        place_block(level, (x_length-5, y_height + 3, z+l), under)
        place_block(level, (x_length-5, y_height + 4, z+l), slab)
        
