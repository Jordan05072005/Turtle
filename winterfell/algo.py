import time
import signal
import sys

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
		correction = 0
		while (True):
			self.move(self.front / 2)
			self.turn(0.5 * correction)
			self.move(max(0, self.front - 2))
			if (self.right > self.left):
				correction = -abs(min(-0.75, (1 / self.front)))
				self.turn(min(-0.75, (1 / self.front)))
			else:
				correction = max(0.75, (1 / self.front) * -1)
				self.turn(max(0.75, (1 / self.front) * -1))



def	signal_handler(sig, frame):
	print("\nExiting the program.")
	algo.reset()
	sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

algo = Algo()
algo.run()