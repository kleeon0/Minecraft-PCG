import random

# cell types
EMPTY = 0
UP_WALL = 1
RIGHT_WALL = 2
DOWN_WALL = 3
LEFT_WALL = 4
FLOOR = 5
TOP_LEFT_CORNER = 6
TOP_RIGHT_CORNER = 7
BOTTOM_LEFT_CORNER = 8
BOTTOM_RIGHT_CORNER = 9
EMPTY = 10

# directions
NORTH = 0
EAST = 1
SOUTH = 2
WEST = 3

# possible cells for each type of cell in North, East, South, West
Rules = {
    TOP_LEFT_CORNER: [EMPTY, UP_WALL, LEFT_WALL, EMPTY],
    TOP_RIGHT_CORNER: [EMPTY, EMPTY, RIGHT_WALL, UP_WALL],
    BOTTOM_LEFT_CORNER: [LEFT_WALL, DOWN_WALL, EMPTY, EMPTY],
    BOTTOM_RIGHT_CORNER: [RIGHT_WALL, EMPTY, EMPTY, DOWN_WALL],
    UP_WALL: [EMPTY, UP_WALL, FLOOR, UP_WALL],
    RIGHT_WALL: [RIGHT_WALL, EMPTY, RIGHT_WALL, FLOOR],
    DOWN_WALL: [FLOOR, DOWN_WALL, EMPTY, DOWN_WALL],
    LEFT_WALL: [LEFT_WALL, FLOOR, LEFT_WALL, EMPTY],
    FLOOR: [FLOOR, FLOOR, FLOOR, FLOOR],
    EMPTY: []
}


class Tile:
    def __init__(self):
        self.possibilities = list(Rules.keys())
        self.entropy = len(self.possibilities)
        self.neighbors = dict()
        self.collapsed = False
    
    def __str__(self):
        return f"Tile with possibilities: {self.possibilities} and entropy: {self.entropy}"
        
    def addneighbor(self, direction, tile):
        self.neighbors[direction] = tile
        
    def getEntropy(self):
        return self.entropy
        
    def getNeighbor(self, direction):
        return self.neighbors[direction]    
    
    def getDirecitons(self):
        return self.neighbors.keys()
    
    def getpossibilities(self):
        return self.possibilities
    
    def isCollapsed(self):
        return self.collapsed
    
    def collapse(self):
        self.possibilities = random.choices(self.possibilities)
        self.entropy = 0
        self.collapsed = True
    
    def propogate(self):
        for direction in self.neighbors.keys():
            neighbor = self.getNeighbor(direction)
            opposite = (direction + 2) % 4
            if opposite == NORTH:
                neighbor.possibilities.remove(SOUTH)
            elif opposite == EAST:
                neighbor.possibilities.remove(WEST)
            elif opposite == SOUTH:
                neighbor.possibilities.remove(NORTH)
            elif opposite == WEST:
                neighbor.possibilities.remove(EAST)
            # for tile in neighbor.possibilities:
            #     if tile in Rules[self.possibilities[0]]: (self.possibilities[0] is the tile that was collapsed)
            #         neighbor.possibilities.add(tile)
            valid_possibilities = []
            for tile in neighbor.possibilities:
                for possibilities in self.possibilities:
                    if possibilities in Rules[tile]:
                        valid_possibilities.append(tile)
            neighbor.possibilities = valid_possibilities
            neighbor.entropy = len(neighbor.possibilities)
    
t = Tile()
print(t)
t.collapse()
print(t)