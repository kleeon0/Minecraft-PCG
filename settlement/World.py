# https://www.youtube.com/watch?v=Wx6PNRksIdw

import random
from Constraints import *
from Tiles import *

#CONSTANTS
TILE_SIZE = 5

class World:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.rows = x/TILE_SIZE
        self.cols = y/TILE_SIZE
        self.grid = [[Tile() for _ in range(self.rows)] for _ in range(self.cols)]
        
        # for loop to remove certain tile types depending on the position
        for x in range(self.cols):
            for y in range(self.rows):
                if (x == 0 and y == 0):
                    self.grid[x][y].possibilities = [FLOOR, BOTTOM_LEFT_CORNER]
                if (x == self.cols - 1 and y == 0):
                    self.grid[x][y].possibilities = [FLOOR, BOTTOM_RIGHT_CORNER]
                if (x == 0 and y == self.rows - 1):
                    self.grid[x][y].possibilities = [FLOOR, TOP_LEFT_CORNER]
                if (x == self.cols-1 and y == self.rows-1):
                    self.grid[x][y].possibilities = [FLOOR, TOP_RIGHT_CORNER]
        
        # Collapse the corners
        
        
        
        for x in range(self.cols):
            for y in range(self.rows):
                tile = self.grid[x][y]
                if y > 0:
                    tile.addNeighbor(SOUTH, self.grid[x][y-1])
                if y < self.rows - 1:
                    tile.addNeighbor(NORTH, self.grid[x][y+1])
                if x > 0:
                    tile.addNeighbor(WEST, self.grid[x-1][y])
                if x < self.cols - 1:
                    tile.addNeighbor(EAST, self.grid[x+1][y])
                    
    def getEntropy(self, x, y):
        return self.grid[x][y].getEntropy()
    
    def getLowestEntropy(self):
        lowestEntropy = len(Rules)
        for y in range(self.rows):
            for x in range(self.cols):
                tileEntropy = self.getEntropy(x,y)
                if tileEntropy > 0:
                    if tileEntropy < lowestEntropy:
                        lowestEntropy = tileEntropy
        return lowestEntropy
      
    def updateNeighbors(self):
        for y in range(self.rows):
            for x in range(self.cols):
                self.grid[x][y].updateNeighbors()
                
    def updateEntropy(self):
        tiles = []
        for tile in self.possibilities():
            isValid = True
            if self.getNeighbor[NORTH].isCollapsed() and not self.matchingTiles(tile, self.getNeighbor[NORTH].getPossibilities()):
                isValid = False
            if self.getNeighbor[EAST].isCollapsed() and not self.matchingTiles(tile, self.getNeighbor[EAST].getPossibilities()):
                isValid = False
            if self.getNeighbor[SOUTH].isCollapsed() and not self.matchingTiles(tile, self.getNeighbor[SOUTH].getPossibilities()):
                isValid = False
            if self.getNeighbor[WEST].isCollapsed() and not self.matchingTiles(tile, self.getNeighbor[WEST].getPossibilities()):
                isValid = False
            if isValid:
                tiles.append(tile)
        self.possibilities = tiles
        self.entropy = len(tiles)
        

    def _matchingTiles(self,tile, targetTile):
        if targetTile in Rules[tile]:
            return True
        return False