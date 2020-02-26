import os
import sys
import math
import heapq
from datetime import datetime
from Queue import PriorityQueue

class Node(object):
    def __init__(self, state, cost, depth, parent,action):
        self.state = state
        self.cost = cost
        self.depth = depth
        self.parent = parent
        self.action = action

    #input the 2d array of state to find the zero tile
    def findBlankSpace(self):
        for i in range(n):
            for j in range(n):
                if self.state[i][j] == 0:
                    return [i, j]

    def setHeuristicCost(self, hcost):
        self.heuristicCost = hcost

    def __str__(self):
        return ''.join(''.join(map(str, row)) for row in self.state)

    def __eq__(self, other):
        return self.cost == other.cost

    def __ne__(self, other):
        return self.cost != other.cost

    def __lt__(self, other):
        return self.cost < other.cost

    def __gt__(self, other):
        return self.cost > other.cost

    def __le__(self, other):
        return self.cost <= other.cost

    def __ge__(self, other):
        return self.cost >= other.cost

    def __hash__(self):
        return hash(tuple(map(tuple, self.state)))

class Puzzle(object):
    def __init__(self, init_state, goal_state):
        # you may add more attributes if you think is useful
        self.init_state = init_state
        self.goal_state = goal_state
        self.n = len(init_state)
        self.actions = list()
        self. goal_position = {}
        for x, row in enumerate(goal_state):
            for y, num in enumerate(row):
                self.goal_position[num] = (x, y)

    def solve(self):
        #check if unsolvable

        ACTIONS = ["UP", "DOWN", "LEFT", "RIGHT"]
        CHANGE = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        n = self.n

        print("Start A* search with heuristic: Manhattan")
        startTime=datetime.now()
        startNode= Node(self.init_state, \
        self.gethn(self.init_state), 0, None, None)
        pq = PriorityQueue()
        pq.put(startNode)
        visited = {}
        max_pq= 1
        explored = 1

        while pq:
            if pq.qsize() > max_pq:
                max_pq = pq.qsize()
            currNode = pq.get()
            if self.tuplifyStates(currNode.state) in visited:
                continue
            visited[self.tuplifyStates(currNode.state)] = True #A* graph search
            #goal state found
            if currNode.state == self.goal_state:
                endTime = datetime.now()
                self.findPath(currNode)
                print("Goal state found!")
                print("Move sequence:")
                print(self.actions)
                delta = endTime - startTime
                print("Time taken: " + str(delta.seconds) + "."
                + str(delta.microseconds) + " seconds.")
                print("Number of moves: " + str(len(self.actions)))
                print("Number of nodes visited: " + str(len(visited)))
                print("Number of nodes explored: " + str(explored))
                print("Maximum number of nodes saved: " + str(max_pq) + " nodes.")
                return self.actions
            #if currNode not goal state, find next states
            for i in range(4):
                if currNode.action is not None:
                    j = ACTIONS.index(currNode.action) % 2
                    if i == ACTIONS.index(currNode.action) + (-1) ** j:
                        continue
                blank_x, blank_y = currNode.findBlankSpace()
                dx, dy = CHANGE[i]
                if blank_x + dx < 0 or blank_x + dx >= n \
                or blank_y + dy < 0 or blank_y + dy >= n:
                    continue

                nextState = list(map(list, currNode.state))
                nextState[blank_x][blank_y] = nextState[blank_x+dx][blank_y+dy]
                nextState[blank_x+dx][blank_y+dy] = 0

                if self.tuplifyStates(nextState) not in visited:
                    hn = self.gethn(nextState)
                    depth = currNode.depth + 1
                    nextNode = Node(nextState, depth+hn, depth, currNode, ACTIONS[i])
                    pq.put(nextNode)
                    explored += 1

        return ["UNSOLVABLE"]

    # you may add more functions if you think is useful
    def gethn(self, state): #heuristic function to be inserted
        distance = 0
        for x, row in enumerate(state):
            for y, num in enumerate(row):
                if num == 0:
                    continue
                distance += abs(self.goal_position[num][0] - x) + \
                abs(self.goal_position[num][1] - y)

        return distance #manhattan distance heurisitic

    # hashing the 2D array of states
    def stringifyStates(self, state):
        return ''.join(''.join(map(str, row)) for row in state)

    def tuplifyStates(self, state):
        return tuple(map(tuple, state))

    #find the path for result:
    def findPath(self, node):
        if node.parent is not None:
            self.findPath(node.parent)
        if node.action is not None:
            self.actions.append(node.action)


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
