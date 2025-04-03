import amulet
from amulet.api.block import Block
from amulet.utils.world_utils import block_coords_to_chunk_coords
from amulet_nbt import StringTag

def generate_house(level, origin, width, height, desired_corner_type):
    """Generate a house with the given parameters in the Amulet world."""
    
    # Manually define block types (replace with actual Minecraft block names and properties)
    wall_block = Block("minecraft", "stone_bricks")  # Stone bricks for the wall
    corner_block = Block("minecraft", "chiseled_stone_bricks")  # Chiseled stone bricks for corners
    stair_block = Block("minecraft", "stone_brick_stairs")  # Stone brick stairs for the roof
    floor_block = Block("minecraft", "oak_planks")  # Oak planks for the floor

    # Set the Y base height
    base_y = -60

    # Define the four corners with the correct base_y
    top_left = (origin[0], base_y, origin[1])
    top_right = (origin[0] + width - 1, base_y, origin[1])
    bottom_left = (origin[0], base_y, origin[1] + height - 1)
    bottom_right = (origin[0] + width - 1, base_y, origin[1] + height - 1)

    # Place the corner block based on the desired corner type
    if desired_corner_type == "top left":
        place_block(level, top_left, corner_block)
    elif desired_corner_type == "top right":
        place_block(level, top_right, corner_block)
    elif desired_corner_type == "bottom left":
        place_block(level, bottom_left, corner_block)
    elif desired_corner_type == "bottom right":
        place_block(level, bottom_right, corner_block)

    # Build walls (use the correct height for wall blocks)
    build_wall(level, top_left, top_right, wall_block, base_y, height)
    build_wall(level, top_right, bottom_right, wall_block, base_y, height)
    build_wall(level, bottom_right, bottom_left, wall_block, base_y, height)
    build_wall(level, bottom_left, top_left, wall_block, base_y, height)

    # Generate a roof
    generate_roof(level, origin, width, height, stair_block, base_y + height)

    # Build the floor inside the house
    build_floor(level, origin, width, height, floor_block, base_y)

    return level

def place_block(level, position, block):
    """Place a block in the Amulet world."""
    x, y, z = position  # Ensure y is part of the position (x, y, z)
    # Ensure we are placing the block in the correct chunk
    cx, cz = block_coords_to_chunk_coords(x, z)
    chunk = level.get_chunk(cx, cz, "minecraft:overworld")
    offset_x, offset_z = x - 16 * cx, z - 16 * cz
    
    # Set the block
    chunk.blocks[offset_x, y, offset_z] = level.block_palette.get_add_block(block)
    chunk.changed = True

def build_wall(level, start, end, block, base_y, height):
    """Build a straight wall between two coordinates."""
    x1, _, z1 = start
    x2, _, z2 = end

    # Loop through each x and z coordinate along the wall, placing blocks at each height
    if x1 == x2:  # Vertical wall (same x-coordinate)
        for y in range(base_y, base_y + height):
            for z in range(min(z1, z2), max(z1, z2) + 1):
                place_block(level, (x1, y, z), block)  # Place a block at (x, y, z)
    elif z1 == z2:  # Horizontal wall (same z-coordinate)
        for y in range(base_y, base_y + height):
            for x in range(min(x1, x2), max(x1, x2) + 1):
                place_block(level, (x, y, z1), block)  # Place a block at (x, y, z)

def generate_roof(level, origin, width, height, stair_block, roof_y):
    """Generate a triangular roof on two sides of the house."""
    
    # The roof will be placed at roof_y, gradually building up
    # We need two slopes: one from the left and one from the right
    left_peak = origin[0] + width // 2  # X-coordinate for the peak on the left side
    right_peak = origin[0] + width // 2  # X-coordinate for the peak on the right side
    
    # Loop through both sides of the roof and place the stairs
    for i in range(min(width, height)):  # Loop through the width and height of the house
        # Left side of the roof
        for x in range(origin[0], origin[0] + i + 1):
            for z in range(origin[1], origin[1] + height):
                place_block(level, (x, roof_y + i, z), stair_block)  # Place stairs on left side

        # Right side of the roof
        for x in range(origin[0] + width - 1, origin[0] + width - 1 - i, -1):
            for z in range(origin[1], origin[1] + height):
                place_block(level, (x, roof_y + i, z), stair_block)  # Place stairs on right side

def build_floor(level, origin, width, height, floor_block, base_y):
    """Fill the inside of the house with a floor."""
    for x in range(origin[0], origin[0] + width):
        for z in range(origin[1], origin[1] + height):
            place_block(level, (x, base_y, z), floor_block)  # Pass y = base_y for the floor

# Load the Minecraft world using Amulet
world_path = "C:\\Users\\sivap\\AppData\\Roaming\\.minecraft\\saves\\HouseGenTest"
level = amulet.load_level(world_path)

# Generate the house at a specified position, with a width and height
origin = (20, 30)  # House starting coordinates (x, z)
width = 5  # Width of the house
height = 5  # Height (length) of the house
desired_corner_type = "top left"  # Corner style (you can change this to 'top right', 'bottom left', or 'bottom right')

generate_house(level, origin, width, height, desired_corner_type)

# Save and close the world
level.save()
level.close()
