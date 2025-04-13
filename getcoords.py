import amulet
from amulet.api.block import Block
from amulet.utils.world_utils import block_coords_to_chunk_coords
from amulet_nbt import StringTag

def read_block(level, position):
    """Read a block from the Amulet world."""
    x, y, z = position
    cx, cz = block_coords_to_chunk_coords(x, z)
    chunk = level.get_chunk(cx, cz, "minecraft:overworld")
    offset_x, offset_z = x - 16 * cx, z - 16 * cz
    
    # Get the block ID at the specified position
    block_id = chunk.blocks[offset_x, y, offset_z]
    
    return chunk.block_palette[block_id].base_name

def get_coords(level, origin):
    coords = []
    coord = origin
    for z in range(256):
        for x in range(256):
            y = 320
            block_name = None
            while block_name != "dirt" and block_name != "grass_block":
                y= y-1
                coord = (origin[0]+ x, origin[1]+ y, origin[2]+z)
                block_name = read_block(level, coord)
                #print(coord, block_name)
                if y == -64:
                    break
            coords.append(coord)
    return coords

