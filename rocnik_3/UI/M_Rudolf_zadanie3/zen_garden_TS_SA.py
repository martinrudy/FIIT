import numpy as np
import tkinter
import functools
import datetime
import random
import copy
import math
import time


maxTabuSize = 30



class Garden:
    outOfBoundsId = -2
    rockId = -1
    emptyId = 0
 
    def __init__(self, size, rocks):
        self.size = size
        self.rocks = rocks
        self.area = self.createArea()
        self.solution = None
        self.bestScore = 0
        return
        
    def reset(self):
        self.area = self.createArea()
        return
        
    def createArea(self):
        area = np.zeros(self.size, dtype=np.int8)
        for rock in self.rocks:
            area[rock] = self.rockId
        return area
        
    def startPositions(self):
        sps = []
        height, width = self.size
        for i in range(width):
            sps.append((0, i))
            sps.append((height - 1, i))
        for i in range(height):
            sps.append((i, 0))
            sps.append((i, width - 1))
        return sps
        
    def guessDir(self, pos):
        direction = 0
        height, _ = self.size
        if(pos[0] == 0):
            direction = 3
        elif(pos[0] == height -1):
            direction = 1
        elif(pos[1] == 0):
            direction = 2
        return direction
        
    @property
    def score(self):
        return np.count_nonzero(self.area)
        
class Monk:
 
    @staticmethod
    def neighbor(chromosome):
        positions = list(chromosome[0]) #copy
        decisions = list(chromosome[1]) #copy
        swap1, swap2 = random.sample(range(len(positions)), 2)
        tmp = positions[swap1]
        positions[swap1] = positions[swap2]
        positions[swap2] = tmp
        return [positions, decisions]
 
    directions = np.array([
        (0, -1),
        (-1, 0),
        (0, 1), 
        (1, 0) 
    ])
 
    def __init__(self, positionPool, rotationPool):
        self.positionPool = list(positionPool)
        self.rotationPool = list(rotationPool)
        self.position, self.direction = self.positionPool.pop()
        self.runId = 1
        self.rotId = 0
        return
    
    def rotate(self, rotation):
        self.direction = (self.direction + rotation) % 4
        return
        
    def availableRotations(self, garden):
        avalRot = []
        for rot in (-1, 1):
            self.rotate(rot)
            if(self.aheadTile(garden) == 0 or self.aheadTile(garden) == Garden.outOfBoundsId):
                avalRot.append(rot)
            self.rotate(-rot)
        return avalRot
        
    def aheadPos(self):
        return tuple(self.position + Monk.directions[self.direction])
    
    def moveForward(self):
        self.position = self.aheadPos()
        #print("Moved to:", self.position)
        return
    
    def aheadTile(self, garden):
        aheadPos = self.aheadPos()
        if(
            aheadPos[0] >= garden.size[0]
            or aheadPos[0] < 0
            or aheadPos[1] >= garden.size[1]
            or aheadPos[1] < 0
        ):
            return Garden.outOfBoundsId
        else:
            return garden.area[aheadPos]
        
    def solve(self, garden):
        garden.area[self.position] = self.runId
        while(True):
            aheadTile = self.aheadTile(garden)
            if(aheadTile == Garden.outOfBoundsId): 
                if(len(self.positionPool) == 0): 
                    break
                newPos, newDir = self.positionPool.pop()
                if(garden.area[newPos] != Garden.emptyId): 
                    continue
                self.runId += 1
                self.position = newPos
                self.direction = newDir
                garden.area[self.position] = self.runId
            elif(aheadTile == Garden.emptyId): 
                self.moveForward()
                garden.area[self.position] = self.runId
            else: 
                avalRot = self.availableRotations(garden)
                if(len(avalRot) == 0): 
                    break
                elif(len(avalRot) == 1): 
                    self.rotate(avalRot[0])
                    #print("Doing the only option for rotation")
                else: 
                    choice = self.rotationPool[self.rotId]
                    self.rotId = (self.rotId + 1) % len(self.rotationPool)
                    self.rotate(avalRot[choice])
                    #print("Two options, monk choose to turn:", ["left", "right"][choice])
            #return False
        return True
     
def wrapped_partial(func, *args, **kwargs):
    partial_func = functools.partial(func, *args, **kwargs)
    functools.update_wrapper(partial_func, func)
    return partial_func

def printGarden(garden):
    iterator2 = 1
    for spot in garden.area:
        print(spot)
        """
        for i in range(0, len(spot)):
            print(spot[i], end ="")
            if(iterator2 % garden.size[0] == 0):
                print("\n")
            iterator2 += 1
        """
        if(iterator2 % garden.size[0] == 0):
            print("\n")
        iterator2 += 1

def swapPosition(sps):
    pos1 = random.randint(0, len(sps)-1)
    if(pos1 > 0):
        sps[pos1], sps[pos1 - 1] = sps[pos1 - 1], sps[pos1]
    else:
        sps[pos1], sps[pos1 + 1] = sps[pos1 + 1], sps[pos1]
    return sps


def getNeighbors(garden, chromosome):
    neighbors = []
    newchrom = chromosome
    for _ in range(10):
        g = copy.deepcopy(garden)
        g.reset()
        newchrom = monk.neighbor(chromosome)
        neigmonk = Monk(*newchrom)
        neigmonk.solve(g)
        neighbors.append(g)
    return neighbors

def getRandomNeighbor(garden, chromosome):
    g = copy.deepcopy(garden)
    g.reset()
    neigmonk = Monk(*chromosome)
    neigmonk.solve(g)
    return g

def SA(garden, monk, chromosome):
    initial_temp = 90
    final_temp = 0.1
    alpha = 0.01
    best = garden
    current_temp = initial_temp 
    k = 0

    while(current_temp > final_temp):
        k = 0
        for _ in range(10):
            if(best.score > best.bestScore):
                best.bestScore = best.score
                best.solution = chromosome
            chromosome = monk.neighbor(best.solution)
            neighbor = getRandomNeighbor(best, chromosome)
            diff = best.score - neighbor.score
            if(diff < 0):
                best = neighbor
            elif(random.random() < 1/((math.e) ** (diff / current_temp))):
                best = neighbor
            else:
                k +=1
        current_temp -= alpha
        if(k == 10):
            print("zavrel som kvoli susedom")
            break
    return best


def tabuSearch(candidate, monk, chromosome):
    stop = 0
    sBest = candidate
    bestCandidate = candidate
    tabuList = []
    neighborhood = []
    tabuList.append(candidate)
    while(stop < 1000):
        print("Score:", sBest.score)
        print("Best score:", sBest.bestScore)
        #print("Best solution:", sBest.solution)
        if(sBest.score > sBest.bestScore):
            sBest.bestScore = sBest.score
            sBest.solution = chromosome
        #printGarden(bestCandidate)
        neighborhood = getNeighbors(sBest, sBest.solution)
        #bestCandidate = random.choice(neighborhood)
        for sCandidate in neighborhood:
            if(sCandidate in tabuList):
                continue
            elif(sCandidate.score > bestCandidate.score):
                bestCandidate = sCandidate
        if (bestCandidate.score > sBest.score):
            sBest = bestCandidate
        tabuList.append(bestCandidate)
        if(len(tabuList) > maxTabuSize):
            tabuList.pop(0)
        stop += 1
    return
        
if __name__ == "__main__":
    rocks = (
        (2,6),
        (3,2),
        (4,5),
        (7,9),
        (7,10)
    )
    g = Garden((10,12), rocks)
    sps = g.startPositions()
    random.shuffle(sps)
    chromosome = [(sp, g.guessDir(sp)) for sp in sps]
    chromosome = [chromosome, [0, 1, 1, 1]]
    monk = Monk(*chromosome) #decision pool

    monk.solve(g)
    start = time.time()
    tabuSearch(g, monk, chromosome)
    #sa = SA(g, monk, chromosome)
    #print(sa.bestScore)
    end = time.time()
    print("%.5gs" % (end-start))