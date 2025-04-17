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
from Clustermap import *

# minecraft world path
world_path = "C:\\Users\\Creon\\AppData\\Roaming\\.minecraft\\saves\\Video Demo"
# top left corner of the area to be generated
origin = (0, 0, 0)

# load the world
level = amulet.load_level(world_path)

# get surface coordinates from origin of the world
coords = get_coords(level, origin)

# group regions to clear out
grouped_regions = group_similar_y_regions_from_coords(coords, min_size=5, tol=2)
clear_space(level, grouped_regions)

# get surface coordinates from flattened out world
coords = get_coords(level, origin)
grouped_regions = group_similar_y_regions_from_coords(coords, min_size=2, tol=2)

# group regions that we are going to run WFC on
grouped_regions = [region for region in grouped_regions if region[1][0] - region[0][0]+1 >= 10 and region[1][2] - region[0][2]+1 >= 10]
clear_space(level, grouped_regions)
print("Generating content")
for region in grouped_regions:
    origin = (region[0][0], region[0][2])
    base_y = region[0][1]+1
    # get the size of the region for WFC
    width = region[1][0] - region[0][0]+1
    length = region[1][2] - region[0][2]+1
    if width >= 10 and length >= 10:
        world = World(width,length, origin[0], base_y, origin[1])
        world = world.generateWorld()
        world.editWorld(level, origin, base_y, corner, wall, floor, HEIGHT, LENGTH, WIDTH)

level.save()
level.close()  

