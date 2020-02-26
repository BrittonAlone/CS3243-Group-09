import random
import sys
import getopt
from datetime import datetime, timedelta

### Change import source for different algorithms
from CS3243_P1_09_1 import Puzzle

sampleSize = 3
n = 3
file = "test.out"

try:
  opts, args = getopt.getopt(sys.argv[1:],"s:n:o:")
  for opt, arg in opts:
    if opt == '-s':
      sampleSize = int(arg)
    elif opt == "-n":
      n = int(arg)
    elif opt == "-o":
      file = arg
    
except:
  print('usage: CS3243_P1_09_5.py [-s <sample size> -n <puzzle size> -o <output file>')
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
	arrLen = len(arr);
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
totalSpace, totalSolved, totalUnsolved = 0, 0, 0
totalRuntime = timedelta(0)

outfile = open(sys.argv[1], 'a')

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

  ### Run algorithm
  puzzle = Puzzle(blocks, goalState)
  solved, depth, space, delta = puzzle.solve_with_statistics()

  print("Solved: " + str(solved))
  if solved:
      print("Depth: " + str(depth))
  print("Space: " + str(space))
  print("Time: " + str(delta.seconds))
  totalSpace += space
  totalRuntime += delta
  if solved:
      totalSolved += 1
  else:
      totalUnsolved += 1

  outfile.write(str(depth) + "," + str(space) + "," + str(delta.seconds) + "\n")
  run += 1

avgSpace = float(totalSpace) / sampleSize
avgRuntime = (totalRuntime.seconds + (totalRuntime.microseconds / 1000000)) / sampleSize
print("Average queue/stack size: " + str(avgSpace))
print("Average runtime: " + str(avgRuntime))
print("Total solved puzzles: " + str(totalSolved))
print("Total unsolved puzzles: " + str(totalUnsolved))
outfile.write("Average queue/stack size: " + str(avgSpace))
outfile.write("Average runtime: " + str(avgRuntime))
outfile.write("Total solved puzzles: " + str(totalSolved))
outfile.write("Total unsolved puzzles: " + str(totalUnsolved))
outfile.write("\n")
outfile.close()
