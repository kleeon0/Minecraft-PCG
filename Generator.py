from Tiles import *
from World import *
from build_functions import *
from build_functions.Corners import *
from build_functions.Walls import *
from build_functions.Floor import *
import amulet
from amulet.api.block import Block
from amulet.utils.world_utils import block_coords_to_chunk_coords
from amulet_nbt import StringTag
import random
from getcoords import *
from Heatmap import *

world_path = "C:\\Users\\Creon\\AppData\\Roaming\\.minecraft\\saves\\12"
origin = (-450, 0, -70)

def main(args=None):
    level = amulet.load_level(world_path)
    coords = get_coords(level, origin)
    grouped_regions = group_similar_y_regions_from_coords(coords, min_size=10, tol=2)
    clear_space(level, grouped_regions)

    for region in grouped_regions:
        origin = (region[0][0], region[0][2])
        base_y = region[0][1]+1
        width = region[1][0] - region[0][0]+1
        length = region[1][2] - region[0][2]+1
        if width >= 10 and length >= 10:
            world = World(width,length, origin[0], base_y, origin[1])
            world = world.generateWorld()
            world.editWorld(level, origin, base_y, corner, wall, floor, HEIGHT, LENGTH, WIDTH)
    
    level.save()
    level.close()  
