import os
import sys
from copy import copy, deepcopy
from collections import deque
from datetime import datetime

class Puzzle(object):
    def __init__(self, init_state, goal_state):
        self.init_state = init_state
        self.goal_state = goal_state
        self.actions = list()

    class State:
        def __init__(self, board, moves):
            self.board = board # Board object
            self.moves = moves # list of moves

    def findSuccessors(self, state):
        successors = []
        if state.board.blankSpace[1] != 0:
            newBoard = self.moveBlankSpaceLeft(state.board)
            newMoves = list(state.moves)
            newMoves.append("LEFT")
            successors.append(self.State(newBoard, newMoves))
        if state.board.blankSpace[1] != len(state.board.blocks[0]) - 1:
            newBoard = self.moveBlankSpaceRight(state.board)
            newMoves = list(state.moves)
            newMoves.append("RIGHT")
            successors.append(self.State(newBoard, newMoves))
        if state.board.blankSpace[0] != 0:
            newBoard = self.moveBlankSpaceUp(state.board)
            newMoves = list(state.moves)
            newMoves.append("UP")
            successors.append(self.State(newBoard, newMoves))
        if state.board.blankSpace[0] != len(state.board.blocks[0]) - 1:
            newBoard = self.moveBlankSpaceDown(state.board)
            newMoves = list(state.moves)
            newMoves.append("DOWN")
            successors.append(self.State(newBoard, newMoves))
        return successors

    class Board:
        def __init__(self, blocks):
            self.blocks = blocks
            for i in range(len(blocks[0])):
                for j in range(len(blocks[0])):
                    if blocks[i][j] == 0:
                        self.blankSpace = [i, j]
                        break
            
    def moveBlankSpaceLeft(self, board):
        newBlocks = deepcopy(board.blocks)
        newBlocks[board.blankSpace[0]][board.blankSpace[1]] = newBlocks[board.blankSpace[0]][board.blankSpace[1] - 1]
        newBlocks[board.blankSpace[0]][board.blankSpace[1] - 1] = 0
        return self.Board(newBlocks)

    def moveBlankSpaceRight(self, board):
        newBlocks = deepcopy(board.blocks)
        newBlocks[board.blankSpace[0]][board.blankSpace[1]] = newBlocks[board.blankSpace[0]][board.blankSpace[1] + 1]
        newBlocks[board.blankSpace[0]][board.blankSpace[1] + 1] = 0
        return self.Board(newBlocks)

    def moveBlankSpaceUp(self, board):
        newBlocks = deepcopy(board.blocks)
        newBlocks[board.blankSpace[0]][board.blankSpace[1]] = newBlocks[board.blankSpace[0] - 1][board.blankSpace[1]]
        newBlocks[board.blankSpace[0] - 1][board.blankSpace[1]] = 0
        return self.Board(newBlocks)

    def moveBlankSpaceDown(self, board):
        newBlocks = deepcopy(board.blocks)
        newBlocks[board.blankSpace[0]][board.blankSpace[1]] = newBlocks[board.blankSpace[0] + 1][board.blankSpace[1]]
        newBlocks[board.blankSpace[0] + 1][board.blankSpace[1]] = 0
        return self.Board(newBlocks)

    def solve(self):
        if self.init_state == self.goal_state:
            print("Initial and goal states are identical!")
            return []
        # Iterative Depth Search (IDS)
        # start with depth of 3
        print("Starting IDS.")
        startTime = datetime.now()
        depth = 3
        while True: # outer loop that repeats for each depth
            print("Trying depth " + str(depth) + "...")

            # initialise stack with initial state
            stack = deque()
            stack.append(self.State(self.Board(init_state), []))

            visited = set() # set of explored block layouts

            while len(stack) > 0:
                currState = stack.pop()
                if self.stringifyBlocks(currState.board.blocks) in visited:
                    continue
                visited.add(self.stringifyBlocks(currState.board.blocks))
                if len(currState.moves) == depth: # maximum depth reached for path
                    continue
                successors = self.findSuccessors(currState)
                for successor in successors:
                    if successor.board.blocks == self.goal_state:
                        # goal state found
                        endTime = datetime.now()
                        print("Goal state found!")
                        print("Move sequence:")
                        print(successor.moves)
                        delta = endTime - startTime
                        print("Time taken: " + str(delta.seconds) + "." 
                        + str(delta.microseconds) + " seconds.")
                        return successor.moves
                    stack.append(successor)

            depth += 1 # increment depth limit and try again          

    # hashing an entire Board or State object is too slow, so we hash the 2D array of blocks instead    
    def stringifyBlocks(self, blocks):
        return ''.join(''.join(map(str, row)) for row in blocks)            

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
