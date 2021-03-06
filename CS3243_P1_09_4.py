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

        print("Start A* search with heuristic: Number of swaps")
        startTime=datetime.now()
        #initialise with initial state
        stack = PriorityQueue()
        #stack keeps a list of nodes [fn, state, moves]
        stack.put([len(self.actions) + self.gethn(self.init_state), self.init_state, self.actions])
        visited = set()
        max_stack = 1
        generated = 1

        #node = 1
        while stack.qsize() > 0:
            #print("Explore nodes:  "+ str(node))
            if stack.qsize() > max_stack:
                max_stack = stack.qsize()
            #print(stack)
            currNode = stack.get()
            if self.tuplifyStates(currNode[1]) in visited:
                continue
            visited.add(self.tuplifyStates(currNode[1])) #A* graph search
            #goal state found
            if currNode[1] == self.goal_state:
                endTime = datetime.now()
                delta = endTime - startTime
                self.solvable = True
                self.maxSize = max_stack
                self.solutionDepth = len(currNode[2])
                self.runtime = delta
                self.generated = generated
                self.explored = len(visited)
                print("Goal state found!")
                print("Move sequence:")
                print(currNode[2])
                print("Time taken: " + str(delta.seconds) + "."
                + str(delta.microseconds) + " seconds.")
                print("Number of moves: " + str(len(currNode[2])))
                print("Number of nodes explored: " + str(len(visited)))
                print("Number of nodes generated: " + str(generated))
                print("Maximum number of nodes in the queue: " + str(max_stack) + " nodes.")
                return currNode[2]
            successors = self.findSuccessors(currNode)
            for successor in successors:
                if self.tuplifyStates(successor[1]) in visited:
                    continue
                hn = self.gethn(successor[1]) + len(successor[2])
                successor[0] = hn
                stack.put(successor)
                generated += 1
            del(currNode)

    # you may add more functions if you think is useful

    def find_position(self, number, state):
        n = len(state)
        i, j = 0, 0
        for i in range(0, n):
            for j in range(0, n):
                if number == state[i][j]:
                    return i, j


    """Number of Swaps Heuristic"""
    def gethn(self, state):
        n = len(state)
        steps = 0
        mismatch_dic = {}
        reverse_mismatch_dic = {}
        i, j = 0, 0
        for i in range(0, n):
            for j in range(0, n):
                current = state[i][j]
                key = n * i + j + 1
                if key == n * n:
                    key = 0
                if current != self.goal_state[i][j]:
                    mismatch_dic[key] = current
                    reverse_mismatch_dic[current] = key
                if current == 0 and key == 0:
                    mismatch_dic[0] = 0
                    reverse_mismatch_dic[0] = 0
        while len(mismatch_dic) != 0:
            if len(mismatch_dic) == 1:
                break
            if mismatch_dic[0] == 0:
                mismatch_dic.pop(0)
                temp = mismatch_dic.popitem()
                mismatch_dic[0] = 0
                mismatch_dic[temp[0]] = temp[1]
                mismatch_dic[0] = temp[1]
                mismatch_dic[temp[0]] = 0
                reverse_mismatch_dic[temp[1]] = 0
                reverse_mismatch_dic[0] = temp[0]
                steps += 1
                continue
            blank_current = reverse_mismatch_dic[0]
            blank_next = reverse_mismatch_dic[blank_current]
            mismatch_dic[blank_next] = 0
            reverse_mismatch_dic[0] = blank_next
            mismatch_dic.pop(blank_current)
            steps += 1
        return steps

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
        blankSpace = self.findBlankSpace(node[1])
        if blankSpace[0] != len(node[1]) - 1:
            successors.append(self.slideUp(node))
        if blankSpace[0] != 0:
            successors.append(self.slideDown(node))
        if blankSpace[1] != len(node[1]) - 1:
            successors.append(self.slideLeft(node))
        if blankSpace[1] != 0:
            successors.append(self.slideRight(node))
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
        blankSpace = self.findBlankSpace(state)
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
        blankSpace = self.findBlankSpace(state)
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
        blankSpace = self.findBlankSpace(state)
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
        blankSpace = self.findBlankSpace(state)
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
