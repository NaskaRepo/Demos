import os
import msvcrt

# esc	-	'\\x1'
# enter	-	'\\r'
# up	-	'\\xe0' + 'H'
# down	-	'\\xe0' + 'P'
# left	-	'\\xe0' + 'K'
# right	-	'\\xe0' + 'M'

#	This function gets the next key pressed (the above keys are changed to text)
def getKey():
	inputChar = ''

	#	We are going to keep checking the keyboard until a key is pressed
	while len(inputChar) < 1:
		#	msvcrt.getch() checks to see if a key is pressed down.  If no key is pressed it return an empty byte char.  We do some casting and clean up to make it nicer to use
		inputChar = str(msvcrt.getch()).replace("b'", "").replace("'", "")

		#	Handle named keys
		if inputChar == '\\x1':
			return 'esc'
		elif inputChar == '\\r':
			return 'enter'
		elif inputChar == '\\xe0':
			#	Hand special function keys.  We have to call msvcrt.getch twice, the second time will give us more information
			inputChar = str(msvcrt.getch()).replace("b'", "").replace("'", "")

			#	Handle the arrpw keys
			if inputChar == 'H':
				return 'up'
			elif inputChar == 'P':
				return 'down'
			elif inputChar == 'K':
				return 'left'
			elif inputChar == 'M':
				return 'right'
		elif inputChar == '\\000':
			#	Hand more special function keys
			inputChar = str(msvcrt.getch()).replace("b'", "").replace("'", "")

	#	It's a normal key or a key we don't care about
	return inputChar


if __name__ == "__main__":
	os.system('cls')
	print("Press 'esc' to quit\n")
	print("Press a key...")
	
	inputChar = ''

	#	Disply what ever key is pressed, press esc to quit
	while inputChar != 'esc':
		inputChar = getKey()
		os.system('cls')
		print("Press 'esc' to quit\n")
		print("You pressed " + inputChar)
		
	os.system('cls')

	