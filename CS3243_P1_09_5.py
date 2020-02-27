import random
import sys
import getopt
from datetime import datetime, timedelta

### Change import source for different algorithms
from CS3243_P1_09_1 import Puzzle as PuzzleIDS
#from CS3243_P1_09_2 import Puzzle as PuzzleOOP
#from CS3243_P1_09_3 import Puzzle as PuzzleMHT
#from CS3243_P1_09_4 import Puzzle as PuzzleSWP

sampleSize = 3
n = 3
file1 = "exp1.out"
file2 = "exp2.out"
file3 = "exp3.out"
file4 = "exp4.out"

try:
  opts, args = getopt.getopt(sys.argv[1:],"s:n:")
  for opt, arg in opts:
    if opt == '-s':
      sampleSize = int(arg)
    elif opt == "-n":
      n = int(arg)
    
except:
  print('usage: python CS3243_P1_09_5.py [-s <sample size> -n <puzzle size>')
  sys.exit(1)

goalState = [[0 for i in range(n)] for j in range(n)]
for i in range(1, n**2):
    goalState[(i-1)//n][(i-1)%n] = i
    goalState[n - 1][n - 1] = 0

def findBlankSpace(state):
	for i in range(len(state[0])):
		for j in range(len(state[0])):
			if state[i][j] == 0:
				return [i, j]


def isEven(n):
	return n % 2 == 0

def checkSmallerAfter(arr, i):
	arrLen = len(arr)
	check = int(arr[i])
	count = 0
	for x in range(i, arrLen):
		if (int(arr[x]) < check):
			count = count + 1

	return count

def solvable(state):
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
		count = count + checkSmallerAfter(arrStore, i)

	if isEven(arrLen):
		[r, c] = findBlankSpace(state)
		countFromBottom = arrLen - r + 1
		if isEven(countFromBottom):
			return not isEven(count)
		else:
			return isEven(count)


	else:
		return isEven(count)

run = 1

#puzzleClasses = [PuzzleIDS, PuzzleOOP, PuzzleMHT, PuzzleSWP]
puzzleClasses = [PuzzleIDS]
outfiles = [
    open(file1, 'a'),
    open(file2, 'a'),
    open(file3, 'a'),
    open(file4, 'a'),
]

# record statistics for each algorithm
stats = [{} for i in range(len(puzzleClasses))]
for s in stats:
    s["solved"] = 0
    s["unsolved"] = 0
    s["runtime"] = timedelta(0)
    s["space"] = 0

while run <= sampleSize:
  
  # initialise random board
  randomSequence = [i for i in range(0, n ** 2)]
  random.shuffle(randomSequence)
  blocks = [0 for i in range (0, n)]
  for j in range(0, n):
    blocks[j] = [randomSequence[k] for k in range(j * n, n + j * n)]

  print(blocks)
  if not solvable(blocks):
    continue # generate another board and try again

  for i in range(len(puzzleClasses)):
    ### Run algorithm
    puzzle = puzzleClasses[i](blocks, goalState)
    puzzle.solve()
    solved = puzzle.solvable
    depth = puzzle.solutionDepth
    space = puzzle.maxSize
    delta = puzzle.runtime

    '''print("Solved: " + str(solved))
    if solved:
      print("Depth: " + str(depth))
    print("Space: " + str(space))
    print("Time: " + str(delta.seconds))'''
    stats[i]["space"] += space
    stats[i]["runtime"] += delta
    if solved:
      stats[i]["solved"] += 1
    else:
      stats[i]["unsolved"] += 1

    outfiles[i].write(str(depth) + "," + str(space) + "," + str(delta.seconds) + "\n")
  
  run += 1

for i in range(len(puzzleClasses)):
    avgSpace = float(stats[i]["space"]) / sampleSize
    avgRuntime = (stats[i]["runtime"].seconds + (stats[i]["runtime"].microseconds / 1000000)) / sampleSize
    '''print("Average queue/stack size: " + str(avgSpace))
    print("Average runtime: " + str(avgRuntime))
    print("Total solved puzzles: " + str(totalSolved))
    print("Total unsolved puzzles: " + str(totalUnsolved))'''
    outfiles[i].write("Average queue/stack size: " + str(avgSpace) + "\n")
    outfiles[i].write("Average runtime: " + str(avgRuntime) + "\n")
    outfiles[i].write("Total solved puzzles: " + str(stats[i]["solved"]) + "\n")
    outfiles[i].write("Total unsolved puzzles: " + str(stats[i]["unsolved"]) + "\n")

for outfile in outfiles:
    outfile.close()
