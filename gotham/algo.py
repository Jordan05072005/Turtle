import random
import time

class Algo:
	def	__init__(self):
		self.action = ["MOVE", "TURN"]
		n = 5
		self.values = [i for i in range(-n, n + 1) if i != 0]
		self.filename = "action.txt"

	def	random(self):
		while True:
			try:
				with open(self.filename, "r") as file:
					content = file.read().strip()
				if not content:
					with open(self.filename, "w") as file:
						# file.write("TURN 1")
						action = random.choice(self.action)
						value = random.choice(self.values)
						file.write(f"{action} {value}\n")
				else:
					time.sleep(0.01)
			except FileNotFoundError:
				print("File does not exist. Creating it...")
				open(self.filename, "w").close()

algo = Algo()
algo.random()