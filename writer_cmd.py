
front = 0
left = 0
right = 0 
back = 0

def set_var():
	global front, left, right, back
	with open("env.txt", "r") as f:
		line = f.readline()
		while line :
			if ("FRONT" in line):
				front = int(line[6 :])
			elif ("LEFT" in line):
				left = int(line[5 :])
			elif ("RIGHT" in line):
				right = int(line[6 :])
			elif ("BACK" in line):
				back = int(line[5 :])
			line = f.readline()

def MOVE(a) :
	with open("action.txt", "r+") as f :
		while (len(f.read()) != 0):
			f.seek(0, 0)
		f.write(f"MOVE {a}")
		f.close()
		set_var()

def TURN(a) :
	with open("action.txt", "r+") as f :
		while (len(f.read()) != 0):
			f.seek(0, 0)
		f.write(f"TURN {a}")
		f.close()

def RESET() :
	with open("action.txt", "r+") as f :
		while (len(f.read()) != 0):
			f.seek(0, 0)
		f.write("RESET")
		f.close()

def CLEAR() :
	with open("action.txt", "w") as f :
		f.close()

CLEAR()
MOVE(3)
CLEAR()
TURN(3)
print(back)