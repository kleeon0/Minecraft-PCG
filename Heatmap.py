import amulet
from amulet.api.block import Block
from amulet.utils.world_utils import block_coords_to_chunk_coords
from amulet_nbt import StringTag
import getcoords
from getcoords import *
from build_functions import *
from build_functions.Corners import *

def group_similar_y_regions_from_coords(coords, min_size=10, tol=2):

    if not coords:
        return []
    
    # Determine bounding box in x and z.
    xs = [c[0] for c in coords]
    zs = [c[2] for c in coords]
    min_x, max_x = min(xs), max(xs)
    min_z, max_z = min(zs), max(zs)
    
    cols = max_x - min_x + 1  # number of columns (x direction)
    rows = max_z - min_z + 1  # number of rows (z direction)
    
    # Build the 2D grid: grid[z - min_z][x - min_x] = y
    grid = [[None for _ in range(cols)] for _ in range(rows)]
    for (x, y, z) in coords:
        grid[z - min_z][x - min_x] = y

    # Matrix to mark cells that are already included in a region.
    used = [[False for _ in range(cols)] for _ in range(rows)]
    regions = []
    
    # Iterate over each cell in row-major order.
    for r in range(rows):
        for c in range(cols):
            if used[r][c]:
                continue
            
            # Begin a candidate rectangle anchored at (r, c)
            base_y = grid[r][c]
            # For the first row, determine maximal horizontal span from (r, c)
            cand_min = base_y
            cand_max = base_y
            width = 0
            for j in range(c, cols):
                if used[r][j]:
                    break
                val = grid[r][j]
                cand_min = min(cand_min, val)
                cand_max = max(cand_max, val)
                if cand_max - cand_min > tol:
                    break
                width += 1
            
            # If we can’t get even the minimal horizontal span, mark this cell as used and continue.
            if width < min_size:
                used[r][c] = True
                continue
            
            # Store the best valid rectangle found starting at (r, c)
            best_area = 0
            best_h = 1
            best_w = width
            best_region_min = cand_min
            best_region_max = cand_max
            
            # current_width is the maximum width available for the candidate rectangle so far.
            current_width = width
            overall_min = cand_min
            overall_max = cand_max
            
            # Try to extend downward (increase height)
            for h in range(2, rows - r + 1):  # h is the candidate rectangle height
                # For the new row (r + h - 1), determine the contiguous span from column c.
                row_min = grid[r + h - 1][c]
                row_max = grid[r + h - 1][c]
                row_width = 0
                for j in range(c, c + current_width):
                    if j >= cols or used[r + h - 1][j]:
                        break
                    v = grid[r + h - 1][j]
                    row_min = min(row_min, v)
                    row_max = max(row_max, v)
                    if row_max - row_min > tol:
                        break
                    row_width += 1
                if row_width < min_size:
                    break  # Cannot even meet minimal width in this new row.
                # Update current_width: new candidate width is the minimum so far.
                current_width = min(current_width, row_width)
                
                # Update overall min and max by combining previous rows with this row.
                overall_min = min(overall_min, row_min)
                overall_max = max(overall_max, row_max)
                if overall_max - overall_min > tol:
                    break  # Adding this row exceeds the allowed tolerance.
                
                # If the extended rectangle meets the minimal size and has a larger area, record it.
                if h >= min_size and current_width >= min_size:
                    area = h * current_width
                    if area > best_area:
                        best_area = area
                        best_h = h
                        best_w = current_width
                        best_region_min = overall_min
                        best_region_max = overall_max
            
            # If a valid rectangle was found, mark its cells as used and record the region.
            if best_area > 0:
                for i in range(r, r + best_h):
                    for j in range(c, c + best_w):
                        used[i][j] = True
                top_left = (c + min_x, best_region_min, r + min_z)
                bottom_right = (c + best_w - 1 + min_x, best_region_max, r + best_h - 1 + min_z)
                regions.append((top_left, bottom_right))
            else:
                # Even if no valid rectangle (meeting min_size) was formed,
                # mark the cell as used so it is not reconsidered.
                used[r][c] = True
    
    return regions

def clear_space(level, regions):
    """Clear the space in the regions."""
    empty = Block("minecraft", "air")
    print(f"Clearing blocks")
    for region in regions:
        (x1, y1, z1), (x2, y2, z2) = region
        # Clear the blocks in the region (this is a placeholder for actual block clearing logic)
        
        #the logic to clear the blocks in the specified region.
        for x in range(x1, x2 + 1):
            for y in range(y1+1, 320):
                for z in range(z1, z2 + 1):
                    # Placeholder for clearing logic
                    place_block(level, (x, y, z), empty)

