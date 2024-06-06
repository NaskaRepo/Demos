from . import getKey
import threading
import os


class keyboard(threading.Thread):
	def __init__(self, callback=None, handleOveride=True):
		super().__init__()

		self.__callback = callback
		self.__running = False
		self.__handleOveride = handleOveride
		self.__inputChar = ''
		

	def run(self):
		self.__running = True
		
		while self.__running:
			self.__inputChar = getKey.getKey()

			if self.__callback != None:
				self.__callback(self.__inputChar)
			elif self.__inputChar == 'esc':
				self.__running = False
			else:
				print(self.__inputChar)

			if self.__handleOveride and self.__inputChar == 'esc':
				self.__running = False


	def shutdown(self):
		self.__running = False


if __name__ == "__main__":
	import time

	testing = ''

	def handleInput(char):
		global testing
		testing = char

	os.system('cls')

	kbt = keyboard(handleInput)
	kbt.start()

	while testing != 'esc':
		os.system('cls')
		print(testing)
		time.sleep(0.1)

	kbt.shutdown()
	kbt.join()

	os.system('cls')
