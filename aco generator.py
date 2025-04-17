import amulet 
from amulet.api.block import Block
from amulet.utils.world_utils import block_coords_to_chunk_coords
from amulet_nbt import StringTag
from Aco import *


def place_block(level, position, block):
    """Place a block in the Amulet world."""
    x, y, z = position
    cx, cz = block_coords_to_chunk_coords(x, z)
    game_version = ("java", (1, 16, 20))
    chunk = level.get_chunk(cx, cz, "minecraft:overworld")
    offset_x, offset_z = x - 16 * cx, z - 16 * cz
    chunk.blocks[offset_x, y, offset_z] = level.block_palette.get_add_block(block)
    chunk.changed = True
def get_top(level, coord):
    y = 320
    block_name = None
    while block_name != "dirt" and block_name != "grass_block":
        y= y-1
        full=(coord[0], y, coord[1])
        block_name = read_block(level, full)
        if y == -64:
            break
    return full
def placepath(mainroad,sideroad):
    for coords in mainroad:
        coord=get_top(level,coords)
        place_block(level, coord, Block("minecraft", "cobblestone"))
    for coordsarray in sideroad:
        for coords in coordsarray:
                coord=get_top(level,coords)
                place_block(level, coord, Block("minecraft", "cobblestone"))
def read_block(level, position):
    """Read a block from the Amulet world."""
    x, y, z = position
    cx, cz = block_coords_to_chunk_coords(x, z)
    chunk = level.get_chunk(cx, cz, "minecraft:overworld")
    offset_x, offset_z = x - 16 * cx, z - 16 * cz
    
    # Get the block ID at the specified position
    block_id = chunk.blocks[offset_x, y, offset_z]
    
    return chunk.block_palette[block_id].base_name

    
world_path = r"C:\Users\User\AppData\Roaming\.minecraft\saves\12"

level = amulet.load_level(world_path)
acocoords=[]
houses_world = [
        ((375, -209), (364, -198)),
        ((377, -178), (366, -162)),
        ((367, -150), (356, -129)),
        ((377, -135), (366, -124)),
        ((356, -128), (345, -117)),
        ((341, -133), (325, -122)),
        ((325, -126), (314, -115)),
        ((314, -135), (303, -119)),
        ((304, -135), (292, -121)),
        ((332, -170), (321, -159))
]
    
houses_normalized, offset_x, offset_z, grid_width, grid_height = normalize_and_offset_houses_with_margin(houses_world, margin=100)
print("Offset used (world to grid):", offset_x, offset_z)
print("Grid dimensions:", grid_width, grid_height)
    
grid = build_grid_with_houses(grid_width, grid_height, houses_normalized)
    
aco_params = {
        "num_ants": 100, 
        "max_iterations": 200,
        "alpha": 1,
        "beta": 3,
        "evaporation_rate": 0.2,
        "Q": 100
    }
    
network_grid = build_network(grid, houses_normalized, aco_params)
    
if network_grid is not None:
        main_road_world = [grid_to_world(pt, offset_x, offset_z) for pt in network_grid["main_road"]]
        side_roads_world = []
        for side in network_grid["side_roads"]:
            side_roads_world.append([grid_to_world(pt, offset_x, offset_z) for pt in side])
        house_doors_world = [grid_to_world(pt, offset_x, offset_z) for pt in network_grid["house_doors"]]
        
        print("\n--- Main Road (world coordinates) ---")
        print(main_road_world)
        print("\n--- House Doors (world coordinates) ---")
        for i, door in enumerate(house_doors_world):
            print(f"House {i+1} door: {door}")
        print("\n--- Side Roads (world coordinates) ---")
        for i, side in enumerate(side_roads_world):
            print(f"Side road for House {i+1}: {side}")
else:
        print("Failed to build a network.")
placepath(main_road_world,side_roads_world)
level.save()
level.close()  