import random
import sys
import getopt
from datetime import datetime, timedelta

from CS3243_P1_09_1 import Puzzle as PuzzleIDS
from CS3243_P1_09_2 import Puzzle as PuzzleOOP
from CS3243_P1_09_3 import Puzzle as PuzzleMHT
from CS3243_P1_09_4 import Puzzle as PuzzleSWP

sampleSize = 10
n = 3
file1 = "exp1.out"
file2 = "exp2.out"
file3 = "exp3.out"
file4 = "exp4.out"
puzzlesFile = "testedPuzzles.txt"

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

print("Using default sample size s = 10, for 3-puzzles.")
print("Use flags [-s S -n N] for sample size S and N-puzzles.")

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
    return n %2 == 0

def checkSmallerAfter(arr, i):
    arrLen = len(arr)
    check = int(arr[i])
    count = 0
    for x in range(i, arrLen):
        if (int(arr[x]) < check)  and int(arr[x]):
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
        countFromBottom = arrLen - r
        if isEven(countFromBottom):
            return not isEven(count)
        else:
            return isEven(count)

    else:
        return isEven(count)

run = 1
allPuzzles = []

puzzleClasses = [PuzzleIDS, PuzzleOOP, PuzzleMHT, PuzzleSWP]
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
    s["generated"] = 0
    s["explored"] = 0

while run <= sampleSize:

  # initialise random board
  randomSequence = [i for i in range(0, n ** 2)]
  random.shuffle(randomSequence)
  blocks = [0 for i in range (0, n)]
  for j in range(0, n):
    blocks[j] = [randomSequence[k] for k in range(j * n, n + j * n)]

  print(blocks)
  if not solvable(blocks) or blocks in allPuzzles:
    continue # generate another board and try again
  else:
    allPuzzles.append(blocks)

  for i in range(len(puzzleClasses)):
    ### Run algorithm
    puzzle = puzzleClasses[i](blocks, goalState)
    puzzle.solve()
    solved = puzzle.solvable
    if not solved:
      stats[i]["unsolved"] += 1
      outfiles[i].write("Failed to solved.\n")
    else:
      depth = puzzle.solutionDepth
      space = puzzle.maxSize
      delta = puzzle.runtime
      explored = puzzle.explored
      generated = puzzle.generated

      stats[i]["space"] += space
      stats[i]["runtime"] += delta
      stats[i]["solved"] += 1
      stats[i]["explored"] += explored
      stats[i]["generated"] += generated

      outfiles[i].write("{0:d},{1:d},{2:.2f},{3:d},{4:d}\n".format(depth, space, delta.seconds + delta.microseconds / 1000000.0, explored, generated))

  run += 1

for i in range(len(puzzleClasses)):
    avgSpace = float(stats[i]["space"]) / sampleSize
    avgRuntime = stats[i]["runtime"] / sampleSize
    avgExplored = stats[i]["explored"] / sampleSize
    avgGenerated = stats[i]["generated"] / sampleSize
    '''print("Average queue/stack size: " + str(avgSpace))
    print("Average runtime: " + str(avgRuntime))
    print("Total solved puzzles: " + str(totalSolved))
    print("Total unsolved puzzles: " + str(totalUnsolved))'''
    outfiles[i].write("Average queue/stack size: " + str(avgSpace) + "\n")
    outfiles[i].write("Average explored: " + str(avgExplored) + "\n")
    outfiles[i].write("Average generated: " + str(avgGenerated) + "\n")
    outfiles[i].write("Average runtime: {0:.2f}\n".format(avgRuntime.seconds + avgRuntime.microseconds / 1000000.0))
    outfiles[i].write("Total solved puzzles: " + str(stats[i]["solved"]) + "\n")
    outfiles[i].write("Total unsolved puzzles: " + str(stats[i]["unsolved"]) + "\n")

for outfile in outfiles:
    outfile.close()

puzzlesOutfile = open(puzzlesFile, 'a')
for puzzle in allPuzzles:
  puzzlesOutfile.write(str(puzzle) + "\n")
