from PIL import ImageGrab
import turtle
import time

class Display:
	def	__init__(self):
		self.screen = turtle.Screen()
		self.screen.colormode(255)
		self.turtles = [turtle.Turtle() for i in range(3)]
		self.turtles[0].color("blue")
		self.turtles[1].color("red")
		self.turtles[2].color("green")
		self.path = ["naboo/", "gotham/", "winterfell/"]

	def	read_cmd(self, filename):
		with open(filename, "r") as file:
			for line in file:
				return (line.strip().split())

	def	switch_cmd(self, cmd, turtle):
		if not cmd:
			return
		if cmd[0] == "MOVE":
			distance = 10 * int(cmd[1])
			if distance > 0:
				turtle.forward(distance)
			else:
				turtle.backward(-distance)
		elif cmd[0] == "TURN":
			angle = 10 * int(cmd[1])
			if angle > 0:
				turtle.right(angle)
			else:
				turtle.left(-angle)
		else:
			print(f"Invalid command: {cmd}")

	def	update_env(self):
		pass

	def	clear_file(self, path):
		with open(path, "w") as file:
			pass

	def	update(self):
		for i in range(3):
			cmd = self.read_cmd(f"{self.path[i]}action.txt")
			self.switch_cmd(cmd, self.turtles[i])
			self.update_env()
			self.clear_file(f"{self.path[i]}action.txt")
		self.screen.ontimer(self.update, 1)
	
	def	close_on_escape(self):
		self.screen.bye()



display = Display()

display.screen.listen()
display.screen.onkey(display.close_on_escape, "Escape")

display.update()
display.screen.mainloop()