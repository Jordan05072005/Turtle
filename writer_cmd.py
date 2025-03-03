
front = 0
left = 0
right = 0 
back = 0

class Algo:
	def __init__(self):
		self.front = float('inf')
		self.back = float('inf')
		self.left = float('inf')
		self.right = float('inf')
		self.update_env()

	def update_env(self):
		with open("env.txt", "r") as f:
			line = f.readline()
			while line :
				if ("FRONT" in line):
					self.front = int(line[6 :])
				elif ("LEFT" in line):
					self.left = int(line[5 :])
				elif ("RIGHT" in line):
					self.right = int(line[6 :])
				elif ("BACK" in line):
					self.back = int(line[5 :])
				line = f.readline()

	def move(self, a) :
		with open("action.txt", "r+") as f :
			while (len(f.read()) != 0):
				f.seek(0, 0)
			f.write(f"MOVE {a}")
			f.close()
			self.update_env()

	def turn(self, a) :
		with open("action.txt", "r+") as f :
			while (len(f.read()) != 0):
				f.seek(0, 0)
			f.write(f"TURN {a}")
			f.close()
			self.update_env()

	def reset(self) :
		with open("action.txt", "r+") as f :
			while (len(f.read()) != 0):
				f.seek(0, 0)
			f.write("RESET")
			f.close()
			self.update_env()
	
	def run(self):
		while (True):
			self.move(self.front / 2);
		pass

algo = Algo()
algo.run()