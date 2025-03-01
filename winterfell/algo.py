import random
import time

class Algo:
	def	__init__(self):
		self.action = ["MOVE", "TURN"]
		self.values = [-3, -2, -1, 1, 2, 3]
		self.filename = "action.txt"

	def	random(self):
		while True:
			try:
				with open(self.filename, "r") as file:
					content = file.read().strip()
				if not content:
					with open(self.filename, "w") as file:
						action = random.choice(self.action)
						value = random.choice(self.values)
						file.write(f"{action} {value}\n")
						print(f"Written: {action} {value}")
			except FileNotFoundError:
				print("File does not exist. Creating it...")
				open(self.filename, "w").close()

algo = Algo()
algo.random()