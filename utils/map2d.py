import os

def createMap(xIn=10, yIn=10, char='*'):
	mapT = []

	for x in range(xIn):
		mapT += [[]]

		for y in range(yIn):
			mapT[x] += [char]

	return mapT


def printMap(mapT, colorMap={}):
	#	Clears the screen
	os.system('cls')

	# Error check (makes sure the map has an x and y)
	if len(mapT) < 1 or len(mapT[0]) < 0:
		print("Map Error :  map was not formed correctly")
		return

	# This converts the coordinates from data to screen space
	# len(mapT)			This gets the max X length of the map
	# [*range()]		This takes the length and makes it a list (Ex. 3 gets changed into [0, 1, 2])
	xCoords = [*range(len(mapT))]
	yCoords = [*range(len(mapT[0]))]

	# We reverse the y coordinates because we are printing from the top left of the screen so we want to start drawing at max Y instead of 0 Y
	yCoords.reverse()

	# Same as the old totorial 3 but a little fancier
	buffer = "+" + "-" * len(mapT) + "+\n"
	for y in yCoords:
		buffer += "|"
	
		for x in xCoords:
			if mapT[x][y] in colorMap:
				buffer += colorMap[mapT[x][y]]['color'] + mapT[x][y] + '\033[0m'
			else:
				buffer += mapT[x][y]

		buffer += "|\n"

	buffer += "+" + "-" * len(mapT) + "+"
		
	print(buffer)


def swap(mapT, locA, locB):
	temp = mapT[locA[0]][locA[1]]
	mapT[locA[0]][locA[1]] = mapT[locB[0]][locB[1]]
	mapT[locB[0]][locB[1]] = temp
	return mapT


if __name__ == "__main__":
	# Test code
	mapT = createMap()

	mapT[1][1] = ' '

	printMap(mapT)
