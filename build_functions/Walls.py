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

def gen_TopWall(level, position, wall, floor, height, length, width):
    """Generate the top wall of the rectangle with floor inside."""
    x, y, z = position
    # Create top wall
    for l in range(length):
        for h in range(height):
            place_block(level, (x + l, y + h, z), wall)
    
    # Place floor along the inner perimeter of the top wall
    for l in range(0, length):  # Place along the top wall's inner perimeter (x axis)
        place_block(level, (x + l, y, z +1), floor)
        for w in range(1, width):  # Place along the top wall's inner perimeter (z axis)
            place_block(level, (x + l, y, z + w), floor)
            place_block(level, (x + l, y+height+1, z + w), floor)
            
        stair = Block("minecraft", "stone_brick_stairs", properties={"facing": StringTag("south")})
        #place_block(level, (x + l, y + height, z), stair)
        #place_block(level, (x + l, y + height-1, z-1), stair)
        #place_block(level, (x + l, y + height+1, z+1), stair)


def gen_BottomWall(level, position, wall, floor, height, length, width):
    """Generate the bottom wall of the rectangle with floor inside."""
    x, y, z = position
    # Create bottom wall
    for l in range(length):
        for h in range(height):
            place_block(level, (x + l , y + h, z + width - 1), wall)
    
    for l in range(0, length):  # Place along the bottom wall's inner perimeter (x axis)
        place_block(level, (x + l, y, z + width -2), floor)
        for w in range(width-1):
            place_block(level, (x + l, y+height+1, z + w), floor)
            place_block(level, (x + l, y, z + w), floor)
            
        #stair = Block("minecraft", "stone_brick_stairs", properties={"facing": StringTag("north")})
        #place_block(level, (x + l, y + height, z+width-1), stair)
        #place_block(level, (x + l, y + height-1, z+width), stair)
        #place_block(level, (x + l, y + height+1, z+width-2), stair)
    
    #for l in range(0, length):  # Place along the bottom wall's inner perimeter (x axis)
        #place_block(level, (x + l, y, z + width -2), floor)
        #for w in range(width-1):
            #place_block(level, (x + l, y+height+1, z + w), floor)
            
        
    
        
def gen_LeftWall(level, position, wall, floor, height, length, width):
    """Generate the left wall of the rectangle with floor inside."""
    x, y, z = position
    # Create left wall
    for l in range(width):
        for h in range(height):
            place_block(level, (x, y + h, z + l), wall)
        # Place floor along the inner perimeter of the left wall
    for l in range(0, length):  # Place along the left wall's inner perimeter (z axis)
        place_block(level, (x+1, y, z + l), floor)
        for w in range(1, width):  # Place along the left wall's inner perimeter (x axis)
            place_block(level, (x + w, y, z + l), floor)
            place_block(level, (x + w, y+height+1, z + l), floor)
    
        stair = Block("minecraft", "stone_brick_stairs", properties={"facing": StringTag("east")})
        place_block(level, (x, y + height, z+l), stair)
        place_block(level, (x-1, y + height-1, z+l), stair)
        place_block(level, (x+1, y + height+1, z+l), stair)
        
    #for l in range(0, length):  # Place along the left wall's inner perimeter (z axis)
        #place_block(level, (x + w, y+height+1, z + l), floor)
        #for w in range(width-2):  # Place along the left wall's inner perimeter (x axis)
            #place_block(level, (x + w +2, y+height+1, z + l), floor)


def gen_RightWall(level, position, wall, floor, height, length, width):
    x, y, z = position
    # Create right wall
    for l in range(width):
        for h in range(height):
            place_block(level, (x + length - 1, y + h, z + l), wall)
    for l in range(0, length):  # Place along the right wall's inner perimeter (z axis)
        place_block(level, (x + length - 2, y, z + l), floor)
        for w in range(width-1):  # Place along the left wall's inner perimeter (x axis)
            place_block(level, (x + w, y, z + l), floor)
            place_block(level, (x + w, y+height+1, z + l), floor)

        stair = Block("minecraft", "stone_brick_stairs", properties={"facing": StringTag("west")})
        place_block(level, (x+length-1, y + height, z+l), stair)
        place_block(level, (x+length, y + height-1, z+l), stair)
        place_block(level, (x+length-2, y + height+1, z+l), stair)
        
    #for l in range(0, length):  # Place along the right wall's inner perimeter (z axis)
        #for w in range(width-2):  # Place along the left wall's inner perimeter (x axis)
            #place_block(level, (x + w, y+height+1, z + l), floor)

 
# Example Usage:
world_path = "flat"
level = amulet.load_level(world_path)

# Define blocks
wall = Block("minecraft", "stone_bricks")
floor = Block("minecraft", "oak_planks")

# Set base position and height
origin = (0, 0)
base_y = -60
height = 5  # Adjustable height
length = 5  # Length of the rectangle
width = 5  # Width of the rectangle

#gen_TopWall(level, (origin[0], base_y, origin[1]), wall, floor, height, length, width)
#gen_BottomWall(level, (origin[0], base_y, origin[1]+5), wall, floor, height, length, width)
gen_LeftWall(level, (origin[0], base_y, origin[1]), wall, floor, height, length, width)
gen_RightWall(level, (origin[0]+5, base_y, origin[1]), wall, floor, height, length, width)



# Save and close
level.save()
level.close()
