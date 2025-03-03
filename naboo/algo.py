import time
import signal
import sys
import random

class Algo:
	def	__init__(self):
		self.wait = 0.001
		self.front = float('inf')
		self.back = float('inf')
		self.left = float('inf')
		self.right = float('inf')
		self.update_env()

	def	update_env(self):
		with open("env.txt", "r") as f:
			for line in f:
				parts = line.strip().split()
				if len(parts) == 2:
					value = float(parts[1])
					if parts[0] == "FRONT":
						self.front = value
					elif parts[0] == "LEFT":
						self.left = value
					elif parts[0] == "RIGHT":
						self.right = value
					elif parts[0] == "BACK":
						self.back = value

	def	move(self, a) :
		with open("action.txt", "r+") as f :
			while (len(f.read()) != 0):
				f.seek(0, 0)
				time.sleep(self.wait)
			f.write(f"MOVE {a}")
			f.close()
			self.update_env()

	def	turn(self, a) :
		with open("action.txt", "r+") as f :
			while (len(f.read()) != 0):
				f.seek(0, 0)
				time.sleep(self.wait)
			f.write(f"TURN {a}")
			f.close()
			self.update_env()

	def	reset(self) :
		with open("action.txt", "r+") as f :
			while (len(f.read()) != 0):
				f.seek(0, 0)
				time.sleep(self.wait)
			f.write("RESET")
			f.close()
			self.update_env()
	
	def	run(self):
		self.reset()
		while (True):
			if (random.randint(0, 1)):
				self.move(random.randint(1, 10000) * random.random())
			else:
				self.turn(random.randint(-4, 4) * random.random())


def	signal_handler(sig, frame):
	print("\nExiting the program.")
	algo.reset()
	sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

algo = Algo()
algo.run()