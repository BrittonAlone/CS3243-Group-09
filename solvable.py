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

	print(count)

	if isEven(arrLen):
		[r, c] = findBlankSpace(state)
		countFromBottom = arrLen - r
		if isEven(countFromBottom):
			return not isEven(count)
		else:
			return isEven(count)


	else:
		return isEven(count)