import math
from PIL import Image, ImageGrab
import turtle

class	Env:
	def	__init__(self, img_path, screen):
		self.screen = screen
		self.image = Image.open(img_path).convert("RGB")
		self.img_w, self.img_h = self.image.size

	def turtle_to_image(self, coo):
		screen_w = self.img_w
		screen_h = self.img_h
		img_x = int((coo[0] + screen_w / 2))
		img_y = int((screen_h / 2 - coo[1]))
		return img_x, img_y

	def	get_pixel_color(self, x, y):
		if 0 <= x < self.img_w and 0 <= y < self.img_h:
			return self.image.getpixel((x, y))
		else:
			return None
	
	def is_wall(self, x, y):
		color = self.get_pixel_color(x, y)
		if (color != (255, 255, 255)):
			return (1)
		return (0)

	def	cast_ray(self, start_pos, ray_angle):
		ray_angle = math.radians(ray_angle)
		ray_angle %= 2 * math.pi
		cos_angle, sin_angle = math.cos(ray_angle), math.sin(ray_angle)
		tan_angle = math.tan(ray_angle)
		x_sign, y_sign = int(math.copysign(1, cos_angle)), int(math.copysign(1, sin_angle))
		distance_v = distance_h = float('inf')
		x, y = self.turtle_to_image(start_pos)
		if cos_angle != 0:
			delta_xi = (1 - (x % 1)) if x_sign == 1 else -(x % 1)
			delta_yi = delta_xi * tan_angle
			ray_x, ray_y = x + delta_xi, y + delta_yi
			delta_xe, delta_ye = x_sign, abs(tan_angle) * y_sign
			while True:
				if self.is_wall(math.floor(ray_x), math.floor(ray_y)):
					distance_v = math.hypot(x - ray_x, y - ray_y)
					break
				if not (0 <= int(ray_x) < self.img_w and 0 <= int(ray_y) < self.img_h):
					break
				ray_x += delta_xe
				ray_y += delta_ye
		if sin_angle != 0:
			delta_yi = (1 - (y % 1)) if y_sign == 1 else -(y % 1)
			delta_xi = delta_yi / tan_angle
			ray_x, ray_y = x + delta_xi, y + delta_yi
			delta_xe, delta_ye = abs(1 / tan_angle) * x_sign, y_sign
			while True:
				if self.is_wall(math.floor(ray_x), math.floor(ray_y)):
					distance_h = math.hypot(x - ray_x, y - ray_y)
					break
				if not (0 <= int(ray_x) < self.img_w and 0 <= int(ray_y) < self.img_h):
					break
				ray_x += delta_xe
				ray_y += delta_ye
		final_distance = min(distance_v, distance_h)
		return max(0, final_distance)


class	Display:
	def	__init__(self):
		img_path = "maps/test3.png"
		img = Image.open(img_path)
		img_w, img_h = img.size
		self.screen = turtle.Screen()
		self.screen.setup(img_w, img_h)
		self.screen.bgpic(img_path)
		self.screen.colormode(255)
		self.turtles = [turtle.Turtle() for i in range(3)]
		self.turtles[0].color("blue")
		self.turtles[0].shape("turtle")
		self.turtles[0].shapesize(0.5, 0.5, 1)
		self.turtles[1].color("red")
		self.turtles[1].shape("turtle")
		self.turtles[1].shapesize(0.5, 0.5, 1)
		self.turtles[2].color("green")
		self.turtles[2].shape("turtle")
		self.turtles[2].shapesize(0.5, 0.5, 1)
		self.path = ["naboo/", "gotham/", "winterfell/"]
		self.env = Env(img_path, self.screen)
		self.wall_dist = [[float('inf') for i in range(4)] for i in range(3)]
		for i in range(3):
			self.update_env(self.turtles[i], f"{self.path[i]}env.txt", self.wall_dist[i])

	def	read_cmd(self, filename):
		with open(filename, "r") as file:
			for line in file:
				content = line.strip().split()
				file.close
				return (content)

	def	ft_forward(self, dist, turtle, env):
		max_dist = max(0, env[0] - 0.5)
		final_dist = min(dist, max_dist)
		if final_dist >= max_dist * 0.9:
			step = final_dist * 0.9
			new_x, new_y = self.env.turtle_to_image((turtle.xcor() + step * math.cos(math.radians(turtle.heading())),
													turtle.ycor() + step * math.sin(math.radians(turtle.heading()))))
			if not self.env.is_wall(new_x, new_y):
				turtle.forward(step)
			final_dist *= 0.1
		while final_dist > 0:
			step = min(1, final_dist)
			new_x, new_y = self.env.turtle_to_image((turtle.xcor() + step * math.cos(math.radians(turtle.heading())),
													turtle.ycor() + step * math.sin(math.radians(turtle.heading()))))
			if self.env.is_wall(new_x, new_y):
				break
			turtle.forward(step)
			final_dist -= step

	def	ft_backward(self, dist, turtle, env):
		max_dist = max(0, env[2] - 0.5)
		final_dist = min(dist, max_dist)
		if final_dist >= max_dist * 0.9:
			step = final_dist * 0.9
			new_x, new_y = self.env.turtle_to_image((turtle.xcor() - step * math.cos(math.radians(turtle.heading())),
													turtle.ycor() - step * math.sin(math.radians(turtle.heading()))))
			if not self.env.is_wall(new_x, new_y):
				turtle.backward(step)
			final_dist *= 0.1
		while final_dist > 0:
			step = min(1, final_dist)
			new_x, new_y = self.env.turtle_to_image((turtle.xcor() - step * math.cos(math.radians(turtle.heading())),
													turtle.ycor() - step * math.sin(math.radians(turtle.heading()))))
			if self.env.is_wall(new_x, new_y):
				break
			turtle.backward(step)
			final_dist -= step


	def	switch_cmd(self, cmd, turtle, env):
		if not cmd:
			return
		if cmd[0] == "MOVE":
			distance = 10 * float(cmd[1])
			if distance > 0:
				self.ft_forward(distance, turtle, env)
			else:
				self.ft_backward(-distance, turtle, env)
		elif cmd[0] == "TURN":
			angle = 10 * float(cmd[1])
			if angle > 0:
				turtle.right(angle)
			else:
				turtle.left(-angle)
		else:
			print(f"Invalid command: {cmd}")

	def	update_env(self, turtle, path, env):
		text = ["FRONT", "LEFT", "BACK", "RIGHT"]
		with open(path, "w") as file:
			for i in range(4):
				distance = self.env.cast_ray(turtle.pos(), turtle.heading() + 90 * i)
				env[i] = distance
				file.write(f"{text[i]} {distance}\n")
		file.close()

	def	clear_file(self, path):
		with open(path, "w") as file:
			file.close()

	def	update(self):
		for i in range(3):
			cmd = self.read_cmd(f"{self.path[i]}action.txt")
			if (not cmd):
				continue
			self.switch_cmd(cmd, self.turtles[i], self.wall_dist[i])
			self.update_env(self.turtles[i], f"{self.path[i]}env.txt", self.wall_dist[i])
			self.clear_file(f"{self.path[i]}action.txt")
		self.screen.ontimer(self.update, 10)
	
	def	close_on_escape(self):
		self.screen.bye()



display = Display()

display.screen.listen()
display.screen.onkey(display.close_on_escape, "Escape")

display.update()
display.screen.mainloop()