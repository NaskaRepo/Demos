import utils.map2d as map2d
import utils.frameBuffer as frameBuffer
import utils.keyboard as keyboard
import os
import copy
import time
import random
import math
import ctypes


ICONS = {'*':{'color':'\033[' + str(random.randint(91, 99)) + 'm'}, 
         '.':{'color':'\033[' + str(random.randint(91, 99)) + 'm'}, 
		 'O':{'color':'\033[' + str(random.randint(91, 99)) + 'm'}, 
		 'o':{'color':'\033[' + str(random.randint(91, 99)) + 'm'}, 
		 '@':{'color':'\033[' + str(random.randint(91, 99)) + 'm'}, 
		 '#':{'color':'\033[' + str(random.randint(91, 99)) + 'm'}, 
		 '+':{'color':'\033[' + str(random.randint(91, 99)) + 'm'}, 
		 'X':{'color':'\033[' + str(random.randint(91, 99)) + 'm'}, 
		 'x':{'color':'\033[' + str(random.randint(91, 99)) + 'm'}}
MAX_SPEED = 2
RANGE_PULL = 8
RANGE_PUSH = 2
NUM_BOIDS = 50
STRENGTH_SELF = 0.02
STRENGTH_PULL = 0.01
STRENGTH_PUSH = 0.03
STRENGTH_DISTANCE = 1.5


def scaleToLength(vect, length):
	total = abs(vect[0]) + abs(vect[1])
	return [length * (vect[0] / total), length * (vect[1] / total)]


class Boid:
	def __init__(self, x, y, maxX, maxY):
		self.maxBounds = [maxX, maxY]
		self.position = [x, y]
		self.velocity = [-1, -1]#[random.uniform(-1, 1), random.uniform(-1, 1)]
		self.icon = random.choice(list(ICONS))


	def wrapEdges(self):
		if self.position[0] < 0:
			self.position[0] = self.maxBounds[0] - 1
		if self.position[1] < 0:
			self.position[1] = self.maxBounds[1] - 1
		if self.position[0] >= self.maxBounds[0]:
			self.position[0] = 0
		if self.position[1] >= self.maxBounds[1]:
			self.position[1] = 0


	def update(self, flock):
		self.position[0] += self.velocity[0]
		self.position[1] += self.velocity[1]

		self.wrapEdges()

		averageVelocity = [0, 0]
		averagePosition = [0, 0]
		averageSeparation = [0, 0]
		numNeighbors = 0

		for boid in flock:
			if boid == self:
				continue

			distance = math.sqrt((self.position[0] - boid.position[0])**2 + (self.position[1] - boid.position[1])**2)

			if distance < RANGE_PULL:
				averageVelocity[0] += boid.velocity[0] * ((distance / RANGE_PULL) * STRENGTH_DISTANCE)
				averageVelocity[1] += boid.velocity[1] * ((distance / RANGE_PULL) * STRENGTH_DISTANCE)
				averagePosition[0] += boid.position[0] * ((distance / RANGE_PULL) * STRENGTH_DISTANCE)
				averagePosition[1] += boid.position[1] * ((distance / RANGE_PULL) * STRENGTH_DISTANCE)

				if distance < RANGE_PUSH:
					diff = [self.position[0] - boid.position[0], self.position[1] - boid.position[1]]
					if distance != 0:
						diff = scaleToLength(diff, 1 / distance)
					else:
						self.position[0] += random.uniform(-1, 1)
						self.position[1] += random.uniform(-1, 1)
					
					averageSeparation[0] += diff[0]
					averageSeparation[1] += diff[1]

				numNeighbors += 1

		if numNeighbors > 0:
			averageVelocity[0] /= numNeighbors
			averageVelocity[1] /= numNeighbors
			averagePosition[0] /= numNeighbors
			averagePosition[1] /= numNeighbors
			averageSeparation[0] /= numNeighbors
			averageSeparation[1] /= numNeighbors

		self.velocity[0] += averageVelocity[0] * STRENGTH_SELF
		self.velocity[1] += averageVelocity[1] * STRENGTH_SELF
		self.velocity[0] += averagePosition[0] * STRENGTH_PULL
		self.velocity[1] += averagePosition[1] * STRENGTH_PULL
		self.velocity[0] -= averageSeparation[0] * STRENGTH_PUSH
		self.velocity[1] -= averageSeparation[1] * STRENGTH_PUSH

		self.velocity = scaleToLength(self.velocity, MAX_SPEED)


if __name__ == "__main__":
	ctypes.windll.user32.keybd_event(0x7A)
	time.sleep(0.1)
	size = os.get_terminal_size()
	maxX=size[0] - 3
	maxY=size[1] - 3

	flock = [Boid(random.randint(0, maxX - 1), random.randint(0, maxY - 1), maxX, maxY) for _ in range(NUM_BOIDS)]

	mapT = map2d.createMap(maxX, maxY, ' ')

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

		for boid in flock:
			boid.update(flock)
			mapTbuff[int(boid.position[0])][int(boid.position[1])] = boid.icon

		fb.draw(mapTbuff, ICONS)
		time.sleep(0.05)

	print('\033[?25h', end="")
	ctypes.windll.user32.keybd_event(0x7A)

	os.system('cls')
	
	kbt.shutdown()
	kbt.join()