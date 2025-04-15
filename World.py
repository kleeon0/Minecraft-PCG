import amulet
from amulet.api.block import Block
from amulet.utils.world_utils import block_coords_to_chunk_coords
from amulet_nbt import StringTag
import random
from Tiles import *
from build_functions import *
from build_functions.Corners import *
from build_functions.Walls import *
from build_functions.Floor import *

#CONSTANTS
TILE_SIZE = 5
HEIGHT = 5  # Adjustable height
LENGTH = 5  # Length of the rectangle
WIDTH = 5  # Width of the rectangle
BASE_Y = -60  # Base Y position for the world
wall = Block("minecraft", "stone_bricks")
floor = Block("minecraft", "oak_planks")
corner = Block("minecraft", "chiseled_stone_bricks")

class World:
    def __init__(self, x, y, originX, originY, originZ):
        self.x = x
        self.y = y
        self.cols = x//TILE_SIZE
        self.rows = y//TILE_SIZE
        self.grid = [[Tile() for _ in range(self.rows)] for _ in range(self.cols)]
        # implementing grid with tiles function
        self.originX = originX
        self.originZ = originZ
        self.origin = (originX, originZ)
        self.base_y = originY
        
        # assigning a neighbor tile for each tile
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
        
        
        # for loop to remove certain tile types depending on the position
        # pre-collapse the corners
        for x in range(self.cols):
            for y in range(self.rows):
                # tiles are it needs to be collapsed as well as the corners
                if (y == 0):
                    self.grid[x][y].possibilities = [DOWN_WALL, BOTTOM_LEFT_CORNER, BOTTOM_RIGHT_CORNER, EMPTY]
                    self.grid[x][y].entropy = 4
                if (y == self.rows - 1):
                    self.grid[x][y].possibilities = [UP_WALL, TOP_LEFT_CORNER, TOP_RIGHT_CORNER, EMPTY]
                    self.grid[x][y].entropy = 4

                if (x == 0):
                    self.grid[x][y].possibilities = [LEFT_WALL, BOTTOM_LEFT_CORNER, TOP_LEFT_CORNER, EMPTY]
                    self.grid[x][y].entropy = 4

                if (x == self.cols - 1):
                    self.grid[x][y].possibilities = [RIGHT_WALL, BOTTOM_RIGHT_CORNER, TOP_RIGHT_CORNER, EMPTY]
                    self.grid[x][y].entropy = 4
                    
                if (x == 0 and y == 0):
                    self.grid[x][y].possibilities = [EMPTY, BOTTOM_LEFT_CORNER]
                    self.grid[x][y].entropy = 2

                    
                if (x == self.cols - 1 and y == 0):
                    self.grid[x][y].possibilities = [EMPTY, BOTTOM_RIGHT_CORNER]
                    self.grid[x][y].entropy = 2

                    
                if (x == 0 and y == self.rows - 1):
                    self.grid[x][y].possibilities = [EMPTY, TOP_LEFT_CORNER]
                    self.grid[x][y].entropy = 2

                    
                if (x == self.cols-1 and y == self.rows-1):
                    self.grid[x][y].possibilities = [EMPTY, TOP_RIGHT_CORNER]
                    self.grid[x][y].entropy = 2
        self.constrain(self.grid[x][y])
                    
        
               
    ## get the lowest entropy value
    def getLowestEntropy(self):
        lowestEntropy = len(Rules)
        for y in range(self.rows):
            for x in range(self.cols):
                tileEntropy = self.grid[x][y].getEntropy()
                if tileEntropy > 0:
                    if tileEntropy < lowestEntropy:
                        lowestEntropy = tileEntropy
        return lowestEntropy
    
    ## get the tiles with the lowest entropy
    def getLowestEntropyTiles(self):
        lowestEntropy = self.getLowestEntropy()
        tiles = []
        if lowestEntropy == 0:
            return tiles
        for y in range(self.rows):
            for x in range(self.cols):
                tileEntropy = self.grid[x][y].getEntropy()
                if tileEntropy == lowestEntropy:
                    tiles.append(self.grid[x][y])
        return tiles
    
    ## one pass of the wave function collapse algorithm
    def WaveFunctionCollapse(self):
        # get the tiles with the lowest entropy
        lowestEntropyTiles = self.getLowestEntropyTiles()
        collapsed = False
        if lowestEntropyTiles == []:
            return collapsed
        # choose a random tile to collapse
        else:
            tile = random.choice(lowestEntropyTiles)
            tile.collapse()
            self.constrain(tile)
            self.updateWeight(tile)
            collapsed = True
        # returns true if a tile was collapsed
        return collapsed
    
    # function to constrain the tiles based on the tile that was collapsed
    def constrain(self, tile):
        # create a stack to hold the tiles to be updated
        tilesStack = []
        # add the neighbor tile to the stack
        tilesStack.append(tile)
        # loop as long as there are tiles in the stack to constrain
        while not len(tilesStack) == 0:
            tile = tilesStack.pop()
            for direction in tile.getDirections():
                neighbor = tile.getNeighbor(direction)
                # update the entropy of the neighbor tile based on the tile that was constrained
                if not neighbor.isCollapsed():
                    changed = neighbor.updateEntropy(tile.getpossibilities() ,direction)
                    # if the entropy of the neighbor changed, add it to the stack to change the neighbors of the neighbor
                    if changed:
                        tilesStack.append(neighbor)
    
    # check if all the tiles are collapsed
    def allCollapsed(self):
        allcollapsed = True
        for r in range(self.rows):
            for c in range(self.cols):
                if not self.grid[c][r].isCollapsed():
                    allcollapsed = False
        return allcollapsed
    
    # collapse all the tiles to empty
    def collapse_to_empty(self):
        for r in range(self.rows):
            for c in range(self.cols):
                tile = self.grid[c][r]
                if not self.grid[c][r].isCollapsed():
                    tile.probabilities = [EMPTY]
                    tile.entropy = 0
                    tile.collapsed = True
    
    # update the weights of the tiles based on the type of tile that was collapsed
    def updateWeight(self, tile):
        type = tile.getpossibilities()[0]
        if self.cols > 5 or self.rows > 5:
            if type == TOP_LEFT_CORNER or type == TOP_RIGHT_CORNER or type == BOTTOM_LEFT_CORNER or type == BOTTOM_RIGHT_CORNER:
                Weights[EMPTY] *= 100
            elif type == EMPTY:
                Weights[EMPTY] *= 0.5
        else:
            if type == TOP_LEFT_CORNER or type == TOP_RIGHT_CORNER or type == BOTTOM_LEFT_CORNER or type == BOTTOM_RIGHT_CORNER:
                Weights[EMPTY] *= 2
            elif type == EMPTY:
                Weights[EMPTY] *= 0.4
    
    # check if the tiles contradict their neighbors
    def hasContradiction(self):
        for r in range(self.rows):
            for c in range(self.cols):
                if self.grid[c][r].contradicts():
                    return True
        return False
    

    # to clear the world
    def clearWorld(self):
        self = World(self.x, self.y)
    
    # to print out the grid for debugging purposes
    def print(self):
        for y in range(self.rows-1,-1,-1):
            print("[", end='')
            for x in range(self.cols):
                print(self.grid[x][y], end=',')
            print("]")
            print()
    
    # function to generate the world   
    def editWorld(self, level, origin, base_y, corner, wall, floor, height, length, width):
        # x and z coordinates to place tile
        x_pointer = origin[0]
        z_pointer = origin[1]
        for z in range(self.rows-1,-1,-1):
            for x in range(self.cols):
                # get the tile type and place the block
                tile = self.grid[x][z]
                tileType = tile.getType()
                if tileType == TOP_LEFT_CORNER:
                    gen_ULCorner(level, (x_pointer, base_y, z_pointer), corner, floor, height, length)
                elif tileType == TOP_RIGHT_CORNER:  
                    gen_URCorner(level, (x_pointer+4, base_y, z_pointer), corner, floor, height, length)
                elif tileType == BOTTOM_LEFT_CORNER:
                    gen_BLCorner(level, (x_pointer, base_y, z_pointer+4), corner, floor, height, length)
                elif tileType == BOTTOM_RIGHT_CORNER:
                    Gen_BRCorner(level, (x_pointer+4,base_y, z_pointer+4), corner, floor, height, length)          
                elif tileType == UP_WALL:
                    gen_TopWall(level, (x_pointer, base_y, z_pointer), wall, floor, height, length, width)
                elif tileType == DOWN_WALL:
                    gen_BottomWall(level, (x_pointer, base_y, z_pointer), wall, floor, height, length, width)
                elif tileType == LEFT_WALL:
                    gen_LeftWall(level, (x_pointer, base_y, z_pointer), wall, floor, height, length, width)
                elif tileType == RIGHT_WALL:
                    gen_RightWall(level, (x_pointer, base_y, z_pointer), wall, floor, height, length, width)
                elif tileType == FLOOR:
                    gen_Floor(level, (x_pointer, base_y, z_pointer), floor, length, width, height)
                elif tileType == EMPTY:
                    None
                else:
                    print("Error: Tile not found")
                x_pointer += TILE_SIZE
            x_pointer = origin[0]
            z_pointer += TILE_SIZE
        
    # runs wfc on the world and does it again if it has a contradiction or if it is not all collapsed
    def generateWorld(self):
        while self.WaveFunctionCollapse():
            continue
        # if the world has a contradiction or not all collapsed, clear it and run the wfc again        
        while not self.allCollapsed() or self.hasContradiction():
            self = World(self.x,self.y, self.origin[0], self.base_y, self.origin[1]).generateWorld()
        return self


