import os
import sys
import math
from datetime import datetime
from Queue import PriorityQueue

class Puzzle(object):
    def __init__(self, init_state, goal_state):
        # you may add more attributes if you think is useful
        self.init_state = init_state
        self.goal_state = goal_state
        self.actions = list()
        self.solvable = False
        self.maxSize = 1
        self.solutionDepth = 0
        self.runtime = 0
        self. goal_position = {}
        for x, row in enumerate(goal_state):
            for y, num in enumerate(row):
                self.goal_position[num] = (x, y)

    def solve(self):
        #check if unsolvable
        if not self.isSolvable(self.init_state):
            print("UNSOLVABLE")
            return ["UNSOLVABLE"]

        print("Start A* search with heuristic: Tiles out of place")
        startTime=datetime.now()
        #initialise with initial state
        stack = PriorityQueue()
        #stack keeps a list of nodes [fn, state, moves]
        stack.put([len(self.actions) + puzzle.gethn(self.init_state), self.init_state, self.actions])
        visited = set()
        max_stack = 1
        explored = 1

        while stack.qsize() > 0:
            if stack.qsize() > max_stack:
                max_stack = stack.qsize()
            currNode = stack.get()
            if puzzle.tuplifyStates(currNode[1]) in visited:
                continue
            visited.add(puzzle.tuplifyStates(currNode[1])) #A* graph search
            #goal state found
            if currNode[1] == self.goal_state:
                endTime = datetime.now()
                delta = endTime - startTime
                self.solvable = True
                self.maxSize = max_stack
                self.solutionDepth = len(currNode[2])
                self.runtime = delta
                print("Goal state found!")
                print("Move sequence:")
                print(currNode[2])
                print("Time taken: " + str(delta.seconds) + "."
                + str(delta.microseconds) + " seconds.")
                print("Number of moves: " + str(len(currNode[2])))
                print("Number of nodes expanded: " + str(len(visited)))
                print("Number of nodes explored: " + str(explored))
                print("Maximum number of nodes in the queue: " + str(max_stack) + " nodes.")
                return currNode[2]
            successors = puzzle.findSuccessors(currNode)
            for successor in successors:
                if puzzle.tuplifyStates(successor[1]) in visited:
                    continue
                hn = puzzle.gethn(successor[1]) + len(successor[2])
                successor[0] = hn
                stack.put(successor)
                explored += 1
            del(currNode)

    """Tile out of Place Heurisitic"""
    def gethn(self, state): #heuristic function to be inserted
        n=len(state)
        mismatches = 0
        i, j = 0, 0
        for i in range(0, n):
            for j in range(0, n):
                if state[i][j] == 0:
                    continue
                if state[i][j] != self.goal_state[i][j]:
                    mismatches += 1
        return mismatches #tile out of place heurisitic

    #Solvability check
    def isEven(self, n):
        return n % 2 == 0

    def checkSmallerAfter(self, arr, i):
        arrLen = len(arr)
        check = int(arr[i])
        count = 0
        for x in range(i, arrLen):
            if (int(arr[x]) < check)  and int(arr[x]):
                count = count + 1

        return count

    def isSolvable(self, state):
        # Solvable if linearly adds up to an even number
        # arr is a 2D array
        arrLen = len(state)
        arrStore = []

        for arrH in state:
            for arrV in arrH:
                arrStore.append(arrV)

        arrStoreLen = len(arrStore)

        count = 0
        for i in range(arrStoreLen):
            count = count + self.checkSmallerAfter(arrStore, i)

        if self.isEven(arrLen):
            [r, c] = self.findBlankSpace(state)
            countFromBottom = arrLen - r
            if self.isEven(countFromBottom):
                return not self.isEven(count)
            else:
                return self.isEven(count)


        else:
            return self.isEven(count)


    #find the next valid moves
    def findSuccessors(self, node):
        successors = []
        blankSpace = puzzle.findBlankSpace(node[1])
        if blankSpace[0] != len(node[1]) - 1:
            successors.append(puzzle.slideUp(node))
        if blankSpace[0] != 0:
            successors.append(puzzle.slideDown(node))
        if blankSpace[1] != len(node[1]) - 1:
            successors.append(puzzle.slideLeft(node))
        if blankSpace[1] != 0:
            successors.append(puzzle.slideRight(node))
        return successors

    #input the 2d array of state to find the zero tile
    def findBlankSpace(self, state):
        for i in range(len(state[0])):
            for j in range(len(state[0])):
                if state[i][j] == 0:
                    return [i, j]

    def slideUp(self, node):
        state = node[1]
        n = len(node[1])
        blankSpace = puzzle.findBlankSpace(state)
        moves = []
        for move in node[2]:
            moves.append(move)
        moves.append("UP")
        newState = [[0 for i in range(n)] for j in range(n)]
        i, j = 0, 0
        for i in range(n):
            for j in range(n):
                newState[i][j] = state[i][j]
        newState[blankSpace[0]][blankSpace[1]] = newState[blankSpace[0] + 1][blankSpace[1]]
        newState[blankSpace[0] + 1][blankSpace[1]] = 0
        return [node[0],newState, moves]

    def slideDown(self, node):
        state = node[1]
        n = len(node[1])
        blankSpace = puzzle.findBlankSpace(state)
        moves = []
        for move in node[2]:
            moves.append(move)
        moves.append("DOWN")
        newState = [[0 for i in range(n)] for j in range(n)]
        i, j = 0, 0
        for i in range(n):
            for j in range(n):
                newState[i][j] = state[i][j]
        newState[blankSpace[0]][blankSpace[1]] = newState[blankSpace[0] - 1][blankSpace[1]]
        newState[blankSpace[0] - 1][blankSpace[1]] = 0
        return [node[0],newState, moves]

    def slideLeft(self, node):
        state = node[1]
        n = len(node[1])
        blankSpace = puzzle.findBlankSpace(state)
        moves = []
        for move in node[2]:
            moves.append(move)
        moves.append("LEFT")
        newState = [[0 for i in range(n)] for j in range(n)]
        i, j = 0, 0
        for i in range(n):
            for j in range(n):
                newState[i][j] = state[i][j]
        newState[blankSpace[0]][blankSpace[1]] = newState[blankSpace[0]][blankSpace[1] + 1]
        newState[blankSpace[0]][blankSpace[1] + 1] = 0
        return [node[0],newState, moves]

    def slideRight(self, node):
        state = node[1]
        n = len(node[1])
        blankSpace = puzzle.findBlankSpace(state)
        moves = []
        for move in node[2]:
            moves.append(move)
        moves.append("RIGHT")
        newState = [[0 for i in range(n)] for j in range(n)]
        i, j = 0, 0
        for i in range(n):
            for j in range(n):
                newState[i][j] = state[i][j]
        newState[blankSpace[0]][blankSpace[1]] = newState[blankSpace[0]][blankSpace[1] - 1]
        newState[blankSpace[0]][blankSpace[1] - 1] = 0
        return [node[0],newState, moves]

    # hashing the 2D array of states
    def stringifyStates(self, state):
        return ''.join(''.join(map(str, row)) for row in state)

    def tuplifyStates(self, state):
        return tuple(map(tuple, state))

if __name__ == "__main__":
    # do NOT modify below

    # argv[0] represents the name of the file that is being executed
    # argv[1] represents name of input file
    # argv[2] represents name of destination output file
    if len(sys.argv) != 3:
        raise ValueError("Wrong number of arguments!")

    try:
        f = open(sys.argv[1], 'r')
    except IOError:
        raise IOError("Input file not found!")

    lines = f.readlines()

    # n = num rows in input file
    n = len(lines)
    # max_num = n to the power of 2 - 1
    max_num = n ** 2 - 1

    # Instantiate a 2D list of size n x n
    init_state = [[0 for i in range(n)] for j in range(n)]
    goal_state = [[0 for i in range(n)] for j in range(n)]


    i,j = 0, 0
    for line in lines:
        for number in line.split(" "):
            if number == '':
                continue
            value = int(number , base = 10)
            if  0 <= value <= max_num:
                init_state[i][j] = value
                j += 1
                if j == n:
                    i += 1
                    j = 0

    for i in range(1, max_num + 1):
        goal_state[(i-1)//n][(i-1)%n] = i
    goal_state[n - 1][n - 1] = 0

    puzzle = Puzzle(init_state, goal_state)
    ans = puzzle.solve()

    with open(sys.argv[2], 'a') as f:
        for answer in ans:
            f.write(answer+'\n')
