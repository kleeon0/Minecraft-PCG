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

# directions
NORTH = 0
EAST = 1
SOUTH = 2
WEST = 3

# weights for each type of cell to increase the probability of certain cells
Weights = {
    EMPTY: 10,
    UP_WALL: 5,
    RIGHT_WALL: 5,
    DOWN_WALL: 1,
    LEFT_WALL: 1,
    FLOOR: 10,
    TOP_LEFT_CORNER: 10,
    TOP_RIGHT_CORNER: 10,
    BOTTOM_LEFT_CORNER: 10,
    BOTTOM_RIGHT_CORNER: 10
}

# possible cells for each type of cell in North, East, South, West
Rules = {
    EMPTY: [EMPTY, EMPTY, EMPTY, EMPTY],
    UP_WALL: [EMPTY, UP_WALL, FLOOR, UP_WALL],
    RIGHT_WALL: [RIGHT_WALL, EMPTY, RIGHT_WALL, FLOOR],
    DOWN_WALL: [FLOOR, DOWN_WALL, EMPTY, DOWN_WALL],
    LEFT_WALL: [LEFT_WALL, FLOOR, LEFT_WALL, EMPTY],
    FLOOR: [FLOOR, FLOOR, FLOOR, FLOOR],
    TOP_LEFT_CORNER: [EMPTY, UP_WALL, LEFT_WALL, EMPTY],
    TOP_RIGHT_CORNER: [EMPTY, EMPTY, RIGHT_WALL, UP_WALL],
    BOTTOM_LEFT_CORNER: [LEFT_WALL, DOWN_WALL, EMPTY, EMPTY],
    BOTTOM_RIGHT_CORNER: [RIGHT_WALL, EMPTY, EMPTY, DOWN_WALL]
}


class Tile:
    def __init__(self):
        self.possibilities = list(Rules.keys())
        self.entropy = len(self.possibilities)
        self.neighbors = dict()
        self.collapsed = False
    
    def __str__(self):
        if self.isCollapsed():
            return str(self.possibilities[0])
        else:
            return "None" + str(self.entropy)
        
        
    def addNeighbor(self, direction, tile):
        self.neighbors[direction] = tile
        
    def getEntropy(self):
        return self.entropy
        
    def getNeighbor(self, direction):
        return self.neighbors[direction]    
    
    def getDirections(self):
        return self.neighbors.keys()
    
    def getpossibilities(self):
        return self.possibilities
    
    def isCollapsed(self):
        return self.collapsed
    
    def getType(self):
        return self.possibilities[0]
    
    def copy(self):
        newTile = Tile()
        newTile.possibilities = self.possibilities
        newTile.entropy = self.entropy
        newTile.neighbors = self.neighbors
        newTile.collapsed = self.collapsed
        return newTile

    # change entropy and return if changed
    def updateEntropy(self, neighborPossibilities, direction):
        newPossibilities = []
        changed = False
        
        if not self.isCollapsed():
            if direction == NORTH: 
                opposite = SOUTH
            if direction == EAST:  
                opposite = WEST
            if direction == SOUTH: 
                opposite = NORTH
            if direction == WEST:  
                opposite = EAST
            for neighborPossibility in neighborPossibilities:                
                newPossibilities.append(Rules[neighborPossibility][direction])
            
            for possibility in self.getpossibilities():
                if Rules[possibility][opposite] not in newPossibilities:
                    self.possibilities.remove(possibility)
                    changed = True
           
            self.entropy = len(self.possibilities)
        return changed
        
    
    def contradicts(self):
        for direction in self.getDirections():
            neighborTile = self.getNeighbor(direction)
            # if the tile is not collapsed and the neighbor is collapsed, check if they match
            if neighborTile.isCollapsed() and not self.matchingTiles(neighborTile, direction):
                return True
        return False
    
    def matchingTiles(self, targetTile, direction):
        if direction == NORTH: 
            opposite = SOUTH
        if direction == EAST:  
            opposite = WEST
        if direction == SOUTH: 
            opposite = NORTH
        if direction == WEST:  
            opposite = EAST
        if self.possibilities and targetTile.possibilities and Rules[self.possibilities[0]][direction] == Rules[targetTile.possibilities[0]][opposite]:
            return True
        return False
    
    def collapse(self):
        probabilities = [Weights[possibility] for possibility in self.possibilities]
        self.possibilities = random.choices(self.possibilities, weights=probabilities)
        self.entropy = 0
        self.collapsed = True
    
    