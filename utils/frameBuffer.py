from . import map2d
import copy
import os


class FrameBuffer():
	def __init__(self, maxX=128, maxY=48):
		self.__maxX = maxX
		self.__maxY = maxY
		self.__buffer = None

	def draw(self, mapT, colorMap={}):
		#
		#	TODO :	Add an out of bounds check here for mapT
		#
		if self.__buffer == None:
			map2d.printMap(mapT, colorMap)
			self.__buffer = copy.deepcopy(mapT)
		else:
			frame = ''
		
			for x in range(0, self.__maxX):
				for y in range(0, self.__maxY):
					if self.__buffer[x][y] != mapT[x][y]:
						if mapT[x][y] in colorMap:
							frame += "\033["+str(self.__maxY-y+1)+";"+str(x+2)+"H"+colorMap[mapT[x][y]]['color']+mapT[x][y]+'\033[0m'
							self.__buffer[x][y] = mapT[x][y]					
						else:
							frame += "\033["+str(self.__maxY-y+1)+";"+str(x+2)+"H"+mapT[x][y]
							self.__buffer[x][y] = mapT[x][y]
	
			if len(frame) > 0:
				print(frame)


if __name__ == "__main__":
	maxX=128
	maxY=48

	fb = FrameBuffer(maxX, maxY)
	mapT = map2d.createMap(maxX, maxY, ' ')

	fb.draw(mapT)

	mapT[0][0] = '0'

	fb.draw(mapT)
	
	mapT[1][1] = '1'
	
	fb.draw(mapT)
	
	mapT[2][2] = '2'
	
	fb.draw(mapT)