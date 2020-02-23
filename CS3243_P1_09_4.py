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
        self. goal_position = {}
        for x, row in enumerate(goal_state):
            for y, num in enumerate(row):
                self.goal_position[num] = (x, y)

    def solve(self):
        #check if unsolvable

        print("Start A* search with heuristic: Number of swaps")
        startTime=datetime.now()
        #initialise with initial state
        stack = PriorityQueue()
        #stack keeps a list of nodes [fn, state, moves]
        stack.put([len(self.actions) + puzzle.gethn(self.init_state), self.init_state, self.actions])
        visited = set()
        max_stack = 1

        #node = 1
        while stack.qsize() > 0:
            #print("Explore nodes:  "+ str(node))
            if stack.qsize() > max_stack:
                max_stack = stack.qsize()
            #print(stack)
            currNode = stack.get()
            if puzzle.tuplifyStates(currNode[1]) in visited:
                continue
            visited.add(puzzle.tuplifyStates(currNode[1])) #A* graph search
            #goal state found
            if currNode[1] == self.goal_state:
                endTime = datetime.now()
                print("Goal state found!")
                print("Move sequence:")
                print(currNode[2])
                delta = endTime - startTime
                print("Time taken: " + str(delta.seconds) + "."
                + str(delta.microseconds) + " seconds.")
                print("Number of moves: " + str(len(currNode[2])))
                print("Number of nodes visited: " + str(len(visited)))
                print("Maximum number of nodes in the queue: " + str(max_stack) + " nodes.")
                return currNode[2]
            successors = puzzle.findSuccessors(currNode)
            for successor in successors:
                if puzzle.tuplifyStates(successor[1]) in visited:
                    continue
                hn = puzzle.gethn(successor[1]) + len(successor[2])
                successor[0] = hn
                stack.put(successor)
            #node += 1

    # you may add more functions if you think is useful

    def find_position(self, number, state):#return pisition of number in current state
        n = len(state)
        i, j = 0, 0
        for i in range(0, n):
            for j in range(0, n):
                if number == state[i][j]:
                    return i, j


    def heuristic2(self, state):
        n = len(state)
        Manhattan_D = 0
        i, j = 0, 0
        for i in range(0, n):
            for j in range(0, n):
                target = self.goal_state[i][j]
                p, q = find_position(self, target, state)
                Manhattan_D += abs(p - i) + abs(q - j)
        return Manhattan_D

    def swap(a, b):
        temp = a
        a = b
        b = temp

    def find_mismatch(self, state):#return the first mismatch square, if all match, return false
        n = len(state)
        i, j = 0, 0
        for i in range(0, n):
            for j in range(0, n):
                if state[i][j] != 0 and state[i][j] != self.goal_state[i][j]:
                    return i, j
        return -1, -1

    """Number of Swaps Heuristic"""
    def gethn(self, state):
        n = len(state)
        temp_state = [[0 for i in range(n)] for j in range(n)]
        i, j = 0, 0
        for i in range(0,n):
            for j in range(0,n):
                temp_state[i][j] = state[i][j]
        steps, blank = 0, 0
        mismatch_i, mismatch_j = find_mismatch(self, state)
        while (mismatch_i, mismatch_j) != (-1, -1):
            blank_i, blank_j = find_position(self, blank, state)
            if (blank_i, blank_j) != ((n - 1), (n - 1)):
                target = self.goal_state[blank_i][blank_j]
                target_i, target_j = find_position(self, target, state)
                swap(state[blank_i][blank_j], state[target_j][target_j])
                steps += 1
                mismatch_i, mismatch_j = find_mismatch(self, state)
            else:
                swap(state[blank_i][blank_j], state[mismatch_i][mismatch_j])
                steps += 1
                mismatch_i, mismatch_j = find_mismatch(self, state)
        i, j = 0, 0
        for i in range(0, n):
            for j in range(0, n):
                state[i][j] = temp_state[i][j]
        return steps

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
