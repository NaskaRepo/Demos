import utils.map2d as map2d
import utils.frameBuffer as frameBuffer
import utils.keyboard as keyboard
import os
import copy
import time
import random
import math
import ctypes


TYPES = {'X':{'name':'dirt' , 'color':'\033[37m', 'state':'solid' , 'func':None},
         'x':{'name':'sand' , 'color':'\033[33m', 'state':'solid' , 'func':None},
		 '#':{'name':'rock' , 'color':'\033[90m', 'state':'solid' , 'func':None},
		 'O':{'name':'water', 'color':'\033[34m', 'state':'liquid', 'func':None},
		 ' ':{'name':'void' , 'color':'\033[0m' , 'state':'void'  , 'func':None}}

def updateDirt(voxelMap, maxX, maxY, loc):
	if loc[1] == 0:
		return voxelMap, [loc]

	if TYPES[voxelMap[loc[0]][loc[1] - 1]]['state'] != 'solid':
		return map2d.swap(voxelMap, loc, (loc[0], loc[1] - 1)), [loc, (loc[0], loc[1] - 1)]

	if random.random() > 0.45:
		if loc[0] + 1 < maxX and TYPES[voxelMap[loc[0] + 1][loc[1] - 1]]['state'] != 'solid':
			return map2d.swap(voxelMap, loc, (loc[0] + 1, loc[1] - 1)), [loc, (loc[0] + 1, loc[1] - 1)]
		if loc[0] - 1 > 1 and TYPES[voxelMap[loc[0] - 1][loc[1] - 1]]['state'] != 'solid':
			return map2d.swap(voxelMap, loc, (loc[0] - 1, loc[1] - 1)), [loc, (loc[0] - 1, loc[1] - 1)]
	else:
		if loc[0] - 1 > 1 and TYPES[voxelMap[loc[0] - 1][loc[1] - 1]]['state'] != 'solid':
			return map2d.swap(voxelMap, loc, (loc[0] - 1, loc[1] - 1)), [loc, (loc[0] - 1, loc[1] - 1)]
		if loc[0] + 1 < maxX and TYPES[voxelMap[loc[0] + 1][loc[1] - 1]]['state'] != 'solid':
			return map2d.swap(voxelMap, loc, (loc[0] + 1, loc[1] - 1)), [loc, (loc[0] + 1, loc[1] - 1)]

	return voxelMap, [loc]


def updateSand(voxelMap, maxX, maxY, loc):
	if random.random() > 0.45:
		if loc[0] + 1 < maxX and loc[0] - 1 > 1 and loc[1] + 1 < maxY and TYPES[voxelMap[loc[0] + 1][loc[1] + 1]]['state'] == 'solid' and TYPES[voxelMap[loc[0] - 1][loc[1]]]['state'] != 'solid':
			return map2d.swap(voxelMap, loc, (loc[0] - 1, loc[1])), [loc, (loc[0] - 1, loc[1])]
		if loc[0] - 1 > 1 and loc[0] + 1 < maxX and loc[1] + 1 < maxY and TYPES[voxelMap[loc[0] - 1][loc[1] + 1]]['state'] == 'solid' and TYPES[voxelMap[loc[0] + 1][loc[1]]]['state'] != 'solid':
			return map2d.swap(voxelMap, loc, (loc[0] + 1, loc[1])), [loc, (loc[0] + 1, loc[1])]
	else:
		if loc[0] - 1 > 1 and loc[0] + 1 < maxX and loc[1] + 1 < maxY and TYPES[voxelMap[loc[0] - 1][loc[1] + 1]]['state'] == 'solid' and TYPES[voxelMap[loc[0] + 1][loc[1]]]['state'] != 'solid':
			return map2d.swap(voxelMap, loc, (loc[0] + 1, loc[1])), [loc, (loc[0] + 1, loc[1])]
		if loc[0] + 1 < maxX and loc[0] - 1 > 1 and loc[1] + 1 < maxY and TYPES[voxelMap[loc[0] + 1][loc[1] + 1]]['state'] == 'solid' and TYPES[voxelMap[loc[0] - 1][loc[1]]]['state'] != 'solid':
			return map2d.swap(voxelMap, loc, (loc[0] - 1, loc[1])), [loc, (loc[0] - 1, loc[1])]

	if loc[1] == 0:
		return voxelMap, [loc]

	if TYPES[voxelMap[loc[0]][loc[1] - 1]]['state'] != 'solid':
		return map2d.swap(voxelMap, loc, (loc[0], loc[1] - 1)), [loc, (loc[0], loc[1] - 1)]

	if random.random() > 0.45:
		if loc[0] + 1 < maxX and TYPES[voxelMap[loc[0] + 1][loc[1] - 1]]['state'] != 'solid':
			return map2d.swap(voxelMap, loc, (loc[0] + 1, loc[1] - 1)), [loc, (loc[0] + 1, loc[1] - 1)]
		if loc[0] - 1 > 1 and TYPES[voxelMap[loc[0] - 1][loc[1] - 1]]['state'] != 'solid':
			return map2d.swap(voxelMap, loc, (loc[0] - 1, loc[1] - 1)), [loc, (loc[0] - 1, loc[1] - 1)]	
	else:
		if loc[0] - 1 > 1 and TYPES[voxelMap[loc[0] - 1][loc[1] - 1]]['state'] != 'solid':
			return map2d.swap(voxelMap, loc, (loc[0] - 1, loc[1] - 1)), [loc, (loc[0] - 1, loc[1] - 1)]
		if loc[0] + 1 < maxX and TYPES[voxelMap[loc[0] + 1][loc[1] - 1]]['state'] != 'solid':
			return map2d.swap(voxelMap, loc, (loc[0] + 1, loc[1] - 1)), [loc, (loc[0] + 1, loc[1] - 1)]
			
	return voxelMap, [loc]


def updateRock(voxelMap, maxX, maxY, loc):
	if loc[1] >= 1 and TYPES[voxelMap[loc[0]][loc[1] - 1]]['state'] != 'solid':
		return map2d.swap(voxelMap, loc, (loc[0], loc[1] - 1)), [loc, (loc[0], loc[1] - 1)]

	return voxelMap, [loc]


def updateWater(voxelMap, maxX, maxY, loc):
	if loc[1] >= 1 and TYPES[voxelMap[loc[0]][loc[1] - 1]]['state'] != 'liquid' and TYPES[voxelMap[loc[0]][loc[1] - 1]]['state'] != 'solid':
		return map2d.swap(voxelMap, loc, (loc[0], loc[1] - 1)), [loc, (loc[0], loc[1] - 1)]

	if random.random() > 0.45:
		if loc[1] >= 1 and loc[0] + 1 < maxX and TYPES[voxelMap[loc[0] + 1][loc[1] - 1]]['state'] != 'liquid' and TYPES[voxelMap[loc[0] + 1][loc[1] - 1]]['state'] != 'solid':
			return map2d.swap(voxelMap, loc, (loc[0] + 1, loc[1] - 1)), [loc, (loc[0] + 1, loc[1] - 1)]
		if loc[1] >= 1 and loc[0] - 1 >= 0 and TYPES[voxelMap[loc[0] - 1][loc[1] - 1]]['state'] != 'liquid' and TYPES[voxelMap[loc[0] - 1][loc[1] - 1]]['state'] != 'solid':
			return map2d.swap(voxelMap, loc, (loc[0] - 1, loc[1] - 1)), [loc, (loc[0] - 1, loc[1] - 1)]
		if loc[0] + 1 < maxX and loc[0] - 1 >= 0 and TYPES[voxelMap[loc[0] + 1][loc[1]]]['state'] != 'solid' and TYPES[voxelMap[loc[0] - 1][loc[1]]]['state'] == 'liquid':
			return map2d.swap(voxelMap, loc, (loc[0] + 1, loc[1])), [loc, (loc[0] + 1, loc[1])]
		if loc[0] - 1 >= 0 and loc[0] + 1 < maxX and TYPES[voxelMap[loc[0] - 1][loc[1]]]['state'] != 'solid' and TYPES[voxelMap[loc[0] + 1][loc[1]]]['state'] == 'liquid':
			return map2d.swap(voxelMap, loc, (loc[0] - 1, loc[1])), [loc, (loc[0] - 1, loc[1])]
	else:
		if loc[1] >= 1 and loc[0] - 1 >= 0 and TYPES[voxelMap[loc[0] - 1][loc[1] - 1]]['state'] != 'liquid'  and TYPES[voxelMap[loc[0] - 1][loc[1] - 1]]['state'] != 'solid':
			return map2d.swap(voxelMap, loc, (loc[0] - 1, loc[1] - 1)), [loc, (loc[0] - 1, loc[1] - 1)]
		if loc[1] >= 1 and loc[0] + 1 < maxX and TYPES[voxelMap[loc[0] + 1][loc[1] - 1]]['state'] != 'liquid'  and TYPES[voxelMap[loc[0] + 1][loc[1] - 1]]['state'] != 'solid':
			return map2d.swap(voxelMap, loc, (loc[0] + 1, loc[1] - 1)), [loc, (loc[0] + 1, loc[1] - 1)]
		if loc[0] - 1 >= 0 and loc[0] + 1 < maxX and TYPES[voxelMap[loc[0] - 1][loc[1]]]['state'] != 'solid' and TYPES[voxelMap[loc[0] + 1][loc[1]]]['state'] == 'liquid':
			return map2d.swap(voxelMap, loc, (loc[0] - 1, loc[1])), [loc, (loc[0] - 1, loc[1])]
		if loc[0] + 1 < maxX and loc[0] - 1 >= 0 and TYPES[voxelMap[loc[0] + 1][loc[1]]]['state'] != 'solid' and TYPES[voxelMap[loc[0] - 1][loc[1]]]['state'] == 'liquid':
			return map2d.swap(voxelMap, loc, (loc[0] + 1, loc[1])), [loc, (loc[0] + 1, loc[1])]
	
	return voxelMap, [loc]
	

def initTypes():
	TYPES['X']['func'] = updateDirt
	TYPES['x']['func'] = updateSand
	TYPES['#']['func'] = updateRock
	TYPES['O']['func'] = updateWater


def updateVoxel(voxelMap, maxX, maxY):
	dirtyMap = map2d.createMap(maxX, maxY, ' ')

	for x in range(0, maxX):
		for y in range(0, maxY):
			if voxelMap[x][y] in TYPES and TYPES[voxelMap[x][y]]['func'] != None and dirtyMap[x][y] != 'X':
				ret = TYPES[voxelMap[x][y]]['func'](voxelMap, maxX, maxY, (x, y))
				voxelMap = ret[0]
				for loc in ret[1]:
					dirtyMap[loc[0]][loc[1]] = 'X'

	return voxelMap


if __name__ == "__main__":
	global maxX
	global maxY

	ctypes.windll.user32.keybd_event(0x7A)
	time.sleep(0.01)
	size = os.get_terminal_size()
	maxX=size[0] - 3
	maxY=size[1] - 3

	initTypes()

	global voxelMap
	voxelMap = map2d.createMap(maxX, maxY, ' ')

	global running
	running = True		

	spawn = (int(maxX/2), maxY-1)

	def inputHandler(char):
		global maxX
		global maxY
		global spawn
		global voxelMap
		if char == 'esc':
			global running
			running = False

		if char == 'z' and voxelMap[spawn[0]][spawn[1] - 1] == ' ':
			voxelMap[spawn[0]][spawn[1]] = 'X'
		if char == 'x' and voxelMap[spawn[0]][spawn[1] - 1] == ' ':
			voxelMap[spawn[0]][spawn[1]] = 'x'
		if char == 'c' and voxelMap[spawn[0]][spawn[1] - 1] == ' ':
			voxelMap[spawn[0]][spawn[1]] = '#'
		if char == 'v' and voxelMap[spawn[0]][spawn[1] - 1] == ' ':
			voxelMap[spawn[0]][spawn[1]] = 'O'
		if char == 'left' and spawn[0] > 0:
			spawn = (spawn[0] - 1, spawn[1])
		if char == 'right' and spawn[0] < maxX - 1:
			spawn = (spawn[0] + 1, spawn[1])
	
	print('\033[?25l', end="")

	kbt = keyboard.keyboard(inputHandler)
	kbt.start()

	fb = frameBuffer.FrameBuffer(maxX, maxY)
	fb.draw(voxelMap)

	while running:
		voxelMap = updateVoxel(voxelMap, maxX, maxY)

		mapFbuff = copy.deepcopy(voxelMap)

		mapFbuff[spawn[0]][spawn[1]] = '@'

		fb.draw(mapFbuff, TYPES)
		time.sleep(0.05)

	print('\033[?25h', end="")
	ctypes.windll.user32.keybd_event(0x7A)

	os.system('cls')

	kbt.shutdown()
	kbt.join()