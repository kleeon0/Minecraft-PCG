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
    
    # returns a string representation of the tile for debugging
    # if the tile is collapsed, it returns the type of the tile
    # if the tile is not collapsed, it returns "None" and the entropy
    def __str__(self):
        if self.isCollapsed():
            return str(self.possibilities[0])
        else:
            return "None" + str(self.entropy)
        

    # adds neighboring tile to the tile    
    def addNeighbor(self, direction, tile):
        self.neighbors[direction] = tile
    
    # returns the entropy of the tile    
    def getEntropy(self):
        return self.entropy
    
    # returns the number of possibilities for the tile    
    def getNeighbor(self, direction):
        return self.neighbors[direction]    
    
    # the direction of the neighbors of that tile
    def getDirections(self):
        return self.neighbors.keys()
    
    # returns the possibilities for the tile
    def getpossibilities(self):
        return self.possibilities
    
    # returnsif the tile is collapsed
    def isCollapsed(self):
        return self.collapsed
    
    # returns the type of the tile if it is collapsed
    def getType(self):
        return self.possibilities[0]
    
    # returns a copy of the tile
    def copy(self):
        newTile = Tile()
        newTile.possibilities = self.possibilities
        newTile.entropy = self.entropy
        newTile.neighbors = self.neighbors
        newTile.collapsed = self.collapsed
        return newTile

    # collapse method referenced from https://github.com/CodingQuest2023/Algorithms/
    # change entropy and return if changed
    def updateEntropy(self, neighborPossibilities, direction):
        newPossibilities = []
        changed = False
        # if the tile is not collapsed and the direction is valid
        if not self.isCollapsed():
            if direction == NORTH: 
                opposite = SOUTH
            if direction == EAST:  
                opposite = WEST
            if direction == SOUTH: 
                opposite = NORTH
            if direction == WEST:  
                opposite = EAST
            # add the possibilities of the neighbor tile to the new possibilities
            for neighborPossibility in neighborPossibilities:                
                newPossibilities.append(Rules[neighborPossibility][direction])
            # remove the possibilities that are not in the new possibilities
            for possibility in self.getpossibilities():
                if Rules[possibility][opposite] not in newPossibilities:
                    self.possibilities.remove(possibility)
                    # change the entropy if the possibilities are changed
                    changed = True
           
            self.entropy = len(self.possibilities)
        return changed
        
    # checks if the tile contradicts with its neighbors
    def contradicts(self):
        for direction in self.getDirections():
            neighborTile = self.getNeighbor(direction)
            # if the tile is not collapsed and the neighbor is collapsed, check if they match
            if neighborTile.isCollapsed() and not self.matchingTiles(neighborTile, direction):
                return True
        return False
    
    # checks if the tile matches with its neighbors
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
    
    # collapses the tile by randomly choosing one of the possibilities
    def collapse(self):
        probabilities = [Weights[possibility] for possibility in self.possibilities]
        self.possibilities = random.choices(self.possibilities, weights=probabilities)
        self.entropy = 0
        self.collapsed = True
    
    
