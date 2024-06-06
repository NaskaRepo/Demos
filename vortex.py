import utils.map2d as map2d
import utils.frameBuffer as frameBuffer
import utils.keyboard as keyboard
import os
import copy
import time
import random
import math


ICONS = {'*':{'color':'\033[' + str(random.randint(91, 99)) + 'm'}, 
         '.':{'color':'\033[' + str(random.randint(91, 99)) + 'm'}, 
		 'O':{'color':'\033[' + str(random.randint(91, 99)) + 'm'}, 
		 'o':{'color':'\033[' + str(random.randint(91, 99)) + 'm'}, 
		 '@':{'color':'\033[' + str(random.randint(91, 99)) + 'm'}, 
		 '#':{'color':'\033[' + str(random.randint(91, 99)) + 'm'}, 
		 '+':{'color':'\033[' + str(random.randint(91, 99)) + 'm'}, 
		 'X':{'color':'\033[' + str(random.randint(91, 99)) + 'm'}, 
		 'x':{'color':'\033[' + str(random.randint(91, 99)) + 'm'}}


def initVortex(maxX, maxY, per=0.05):
	total = maxX * maxY
	num = total * per

	out = []

	for i in range(int(num)):
		x = random.uniform(0, maxX)
		y = random.uniform(0, maxY)

		out += [{'x':x, 'y':y, 'xv':random.uniform(-1, 1),'yv':random.uniform(-1, 1), 'xa':0, 'ya':0, 'icon':random.choice(list(ICONS))}]

	return out


if __name__ == "__main__":
	maxX=128
	maxY=48

	scale = 0.2
    
	mapT = map2d.createMap(maxX, maxY, ' ')
	vortexMap = initVortex(maxX, maxY, 0.05)

	center = {'x':maxX/2, 'y':maxY/2}

	global running
	running = True		

	def inputHandler(char):
		if char == 'esc':
			global running
			running = False

	print('\033[?25l', end="")

	kbt = keyboard.keyboard(inputHandler)
	kbt.start()

	fb = frameBuffer.FrameBuffer(maxX, maxY)
	fb.draw(mapT)

	while running:
		mapTbuff = copy.deepcopy(mapT)

		#	Draw the vortex
		for i in vortexMap:
			if (i['x'] >= 0 and i['x'] < maxX and i['y'] >= 0 and i['y'] < maxY):
				mapTbuff[int(i['x'])][int(i['y'])] = i['icon']
			
			i['x'] += i['xv'] * scale
			i['y'] += i['yv'] * scale

			i['xv'] += i['xa'] * scale
			i['yv'] += i['ya'] * scale

			distX = i['x'] - center['x']
			distY = i['y'] - center['y']

			dist = math.sqrt(abs(distX * distX) + abs(distY * distY))

			i['xa'] = distX * -1 * (1 / dist) * scale
			i['ya'] = distY * -1 * (1 / dist) * scale


		fb.draw(mapTbuff, ICONS)
		time.sleep(0.05)

	print('\033[?25h', end="")

	os.system('cls')
	
	kbt.shutdown()
	kbt.join()