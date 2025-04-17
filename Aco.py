import random
import math
from collections import deque


def normalize_and_offset_houses_with_margin(houses, margin=20):
    normalized = []
    for house in houses:
        (x1, z1), (x2, z2) = house
        nx1, nz1 = min(x1, x2), min(z1, z2)
        nx2, nz2 = max(x1, x2), max(z1, z2)
        normalized.append(((nx1, nz1), (nx2, nz2)))
    
    offset_x = min(house[0][0] for house in normalized)
    offset_z = min(house[0][1] for house in normalized)
    
    max_x = max(house[1][0] for house in normalized)
    max_z = max(house[1][1] for house in normalized)
    
    transformed = []
    for house in normalized:
        (nx1, nz1), (nx2, nz2) = house
        transformed.append(((nx1 - offset_x + margin, nz1 - offset_z + margin),
                            (nx2 - offset_x + margin, nz2 - offset_z + margin)))
    
    grid_width = (max_x - offset_x) + 1 + 2 * margin
    grid_height = (max_z - offset_z) + 1 + 2 * margin
    return transformed, offset_x - margin, offset_z - margin, grid_width, grid_height

def grid_to_world(point, offset_x, offset_z):
    """Convert a grid coordinate back to world coordinates."""
    return (point[0] + offset_x, point[1] + offset_z)


def get_neighbors(cell, grid):
    """
    Given a cell (x, z) and a 2D grid, return its walkable neighbors.
    Uses 4-directional movement.
    Assumes cell coordinates are integers.
    """
    x, z = int(cell[0]), int(cell[1])
    neighbors = []
    directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
    for dx, dz in directions:
        nx, nz = x + dx, z + dz
        if 0 <= nz < len(grid) and 0 <= nx < len(grid[0]):
            if grid[nz][nx] == 0:
                neighbors.append((nx, nz))
    return neighbors

def manhattan(cell, goal):
    return abs(cell[0] - goal[0]) + abs(cell[1] - goal[1])

def ant_colony_pathfinding(grid, start, goal,
                             num_ants=20, max_iterations=50,
                             alpha=1, beta=2, evaporation_rate=0.5, Q=100):
    start = (int(round(start[0])), int(round(start[1])))
    goal  = (int(round(goal[0])), int(round(goal[1])))
    
    pheromone = {}
    for z in range(len(grid)):
        for x in range(len(grid[0])):
            if grid[z][x] == 0:
                current = (x, z)
                for neighbor in get_neighbors(current, grid):
                    pheromone[(current, neighbor)] = 1.0

    best_path = None
    best_path_length = float('inf')

    for iteration in range(max_iterations):
        all_paths = []
        for _ in range(num_ants):
            current = start
            path = [current]
            visited = set([current])
            max_steps = len(grid) * len(grid[0])
            while current != goal and len(path) < max_steps:
                neighbors = get_neighbors(current, grid)
                allowed_neighbors = [n for n in neighbors if n not in visited]
                if not allowed_neighbors:
                    break
                attractiveness = []
                for neighbor in allowed_neighbors:
                    edge = (current, neighbor)
                    pher = pheromone.get(edge, 1e-6)
                    h = 1.0 / (manhattan(neighbor, goal) + 1e-6)
                    attractiveness.append((neighbor, (pher ** alpha) * (h ** beta)))
                total = sum(score for _, score in attractiveness)
                if total == 0:
                    break
                r = random.uniform(0, total)
                cumulative = 0
                chosen = None
                for neighbor, score in attractiveness:
                    cumulative += score
                    if cumulative >= r:
                        chosen = neighbor
                        break
                if chosen is None:
                    break
                path.append(chosen)
                visited.add(chosen)
                current = chosen
            if current == goal:
                all_paths.append(path)
                if len(path) < best_path_length:
                    best_path = path
                    best_path_length = len(path)
        for edge in pheromone:
            pheromone[edge] *= (1 - evaporation_rate)
        for path in all_paths:
            deposit = Q / len(path)
            for i in range(len(path) - 1):
                edge = (path[i], path[i+1])
                pheromone[edge] += deposit
        # Uncomment the line below to monitor progress.
        # print(f"ACO Iteration {iteration+1}: {len(all_paths)} ants reached goal. Best path length: {best_path_length}")
    return best_path


def center_of_house(house):

    (x1, z1), (x2, z2) = house
    cx = int(round((x1 + x2) / 2))
    cz = int(round((z1 + z2) / 2))
    return (cx, cz)

def find_central_nodes_from_areas(houses):

    if not houses:
        return None, None
    centers = [center_of_house(h) for h in houses]
    n = len(centers)
    centroid = (sum(cx for cx, cz in centers) / n, sum(cz for cx, cz in centers) / n)
    def euclidean(a, b):
        return math.sqrt((a[0]-b[0])**2 + (a[1]-b[1])**2)
    central_house = min(houses, key=lambda h: euclidean(center_of_house(h), centroid))
    entrance_house = max(houses, key=lambda h: euclidean(center_of_house(h), centroid))
    return central_house, entrance_house


def bfs_path(grid, start, goal):
    start = (int(round(start[0])), int(round(start[1])))
    goal  = (int(round(goal[0])), int(round(goal[1])))
    queue = deque([[start]])
    visited = set([start])
    while queue:
        path = queue.popleft()
        current = path[-1]
        if current == goal:
            return len(path), path
        for neighbor in get_neighbors(current, grid):
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(path + [neighbor])
    return None, None



def compute_valid_house_door(house, main_road, grid, aco_params, backtracking_depth=1):
    (x1, z1), (x2, z2) = house
    # Four candidate door positions (midpoints of each wall)
    candidates = [
        (int(round(x1)), int(round((z1+z2)/2))),  # left wall center
        (int(round(x2)), int(round((z1+z2)/2))),  # right wall center
        (int(round((x1+x2)/2)), int(round(z1))),   # top wall center
        (int(round((x1+x2)/2)), int(round(z2)))    # bottom wall center
    ]
    best_candidate = None
    best_cost = float('inf')
    for cand in candidates:
        orig_val = grid[cand[1]][cand[0]]
        grid[cand[1]][cand[0]] = 0  # Ensure candidate cell is open
        nearest = find_nearest_node(cand, main_road)
        cost, path = bfs_path(grid, cand, nearest)
        grid[cand[1]][cand[0]] = orig_val  # Restore original value
        if cost is not None and cost < best_cost:
            best_cost = cost
            best_candidate = cand
    # Backtracking: if none of the primary candidates are valid, try neighbors.
    if best_candidate is None and backtracking_depth > 0:
        for cand in candidates:
            for neighbor in get_neighbors(cand, grid):
                orig_val = grid[neighbor[1]][neighbor[0]]
                grid[neighbor[1]][neighbor[0]] = 0
                nearest = find_nearest_node(neighbor, main_road)
                cost, path = bfs_path(grid, neighbor, nearest)
                grid[neighbor[1]][neighbor[0]] = orig_val
                if cost is not None and cost < best_cost:
                    best_cost = cost
                    best_candidate = neighbor
    # Fallback: if still none, choose candidate with minimal Manhattan distance.
    if best_candidate is None:
        best_candidate = min(candidates, key=lambda c: min(manhattan(c, m) for m in main_road))
    return best_candidate

# =====================================================
# 5. Building the Grid and Road Network (Using Offset and Expanded Grid)
# =====================================================

def build_grid_with_houses(width, height, houses):
    grid = [[0 for _ in range(width)] for _ in range(height)]
    for house in houses:
        (x1, z1), (x2, z2) = house
        for z in range(int(z1), int(z2)+1):
            for x in range(int(x1), int(x2)+1):
                if 0 <= z < height and 0 <= x < width:
                    grid[z][x] = 1
    return grid

def find_nearest_node(node, network):
    return min(network, key=lambda n: manhattan(n, node))

def build_network(grid, houses, aco_params):
    central_house_area, entrance_house_area = find_central_nodes_from_areas(houses)
    def default_door(house):
        (x1, z1), (x2, z2) = house
        return (int(round(x1)), int(round((z1+z2)/2)))
    central_door = default_door(central_house_area)
    entrance_door = default_door(entrance_house_area)
    grid[central_door[1]][central_door[0]] = 0
    grid[entrance_door[1]][entrance_door[0]] = 0

    main_road = ant_colony_pathfinding(
        grid, central_door, entrance_door,
        num_ants=aco_params.get('num_ants', 50),
        max_iterations=aco_params.get('max_iterations', 100),
        alpha=aco_params.get('alpha', 1),
        beta=aco_params.get('beta', 3),
        evaporation_rate=aco_params.get('evaporation_rate', 0.2),
        Q=aco_params.get('Q', 100)
    )
    if main_road is None:
        print("Main road could not be established.")
        return None

    house_doors = []
    for house in houses:
        door = compute_valid_house_door(house, main_road, grid, aco_params)
        house_doors.append(door)
        grid[door[1]][door[0]] = 0

    side_roads = []
    for door in house_doors:
        nearest_on_main = find_nearest_node(door, main_road)
        path_to_main = ant_colony_pathfinding(
            grid, door, nearest_on_main,
            num_ants=aco_params.get('num_ants', 50),
            max_iterations=aco_params.get('max_iterations', 100),
            alpha=aco_params.get('alpha', 1),
            beta=aco_params.get('beta', 3),
            evaporation_rate=aco_params.get('evaporation_rate', 0.2),
            Q=aco_params.get('Q', 100)
        )
        if path_to_main:
            side_roads.append(path_to_main)
    return {"main_road": main_road, "side_roads": side_roads, "house_doors": house_doors}


if __name__ == "__main__":
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
    
    houses_normalized, offset_x, offset_z, grid_width, grid_height = normalize_and_offset_houses_with_margin(houses_world, margin=20)
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
        print(side_roads_world)
        for i, side in enumerate(side_roads_world):
            print(f"Side road for House {i+1}: {side}")
    else:
        print("Failed to build a network.")
