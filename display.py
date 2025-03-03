import math
import time
from PIL import Image, ImageDraw
import turtle
import sys

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

	def	is_wall_at_border(self, x, y, x_sign, y_sign):
		check_x = math.floor(x) if x_sign > 0 else math.floor(x - 1)
		check_y = math.floor(y) if y_sign > 0 else math.floor(y - 1)
		return self.is_wall(check_x, check_y)

	def	cast_ray(self, start_pos, ray_angle):
		ray_angle = math.radians(ray_angle)
		ray_angle %= 2 * math.pi
		cos_angle, sin_angle = math.cos(ray_angle), math.sin(ray_angle)
		tan_angle = math.tan(ray_angle)
		x_sign, y_sign = int(math.copysign(1, cos_angle)), int(math.copysign(1, sin_angle))
		distance_v = distance_h = float('inf')
		x, y = self.turtle_to_image(start_pos)
		x += 0.5
		y += 0.5
		if cos_angle != 0:
			delta_xi = (1 - (x % 1)) if x_sign == 1 else -(x % 1)
			delta_yi = delta_xi * tan_angle
			ray_x, ray_y = x + delta_xi, y + delta_yi
			delta_xe, delta_ye = x_sign, abs(tan_angle) * y_sign
			while True:
				if self.is_wall_at_border(ray_x, ray_y, x_sign, y_sign):
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
				if self.is_wall_at_border(ray_x, ray_y, x_sign, y_sign):
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
		# self.img_path = "maps/race.png"
		self.img_path = "maps/test.png"
		# self.start = (452 - 400, (707 - 400) * -1, 180)
		self.start = (0, 0, 0)
		self.screen = turtle.Screen()
		self.init_screen()
		self.turtles = [turtle.Turtle() for i in range(3)]
		self.init_turtles()
		self.path = ["naboo/", "gotham/", "winterfell/"]
		self.env = Env(self.img_path, self.screen)
		self.wall_dist = [[float('inf') for i in range(4)] for i in range(3)]
		for i in range(3):
			self.update_env(self.turtles[i], f"{self.path[i]}env.txt", self.wall_dist[i])
		print(f"a\na\na")

	def	init_screen(self):
		img = Image.open(self.img_path)
		img_w, img_h = img.size
		self.screen.setup(img_w, img_h)
		self.screen.bgpic(self.img_path)
		self.screen.colormode(255)

	def	init_turtles(self):
		color = ["blue", "red", "green"]
		for i in range(3):
			self.turtles[i].color(color[i])
			self.turtles[i].shape("turtle")
			self.turtles[i].shapesize(0.5, 0.5, 1)
			self.turtles[i].penup()
			self.turtles[i].setpos(self.start[0], self.start[1])
			self.turtles[i].setheading(self.start[2])

	def	read_cmd(self, filename):
		with open(filename, "r") as file:
			for line in file:
				content = line.strip().split()
				file.close
				return (content)

	
	def	draw_raycast_turtle(self, start, distance, angle):
		turtle.tracer(0, 0)
		original_x, original_y = turtle.pos()
		end_x = start[0] + distance * math.cos(math.radians(angle))
		end_y = start[1] + distance * math.sin(math.radians(angle))
		turtle.penup()
		turtle.goto(start[0], start[1])
		turtle.pendown()
		turtle.goto(end_x, end_y)
		turtle.penup()
		turtle.goto(original_x, original_y)
		turtle.update()

	def ft_forward(self, dist, turtle, env):
		heading_angle = math.radians(turtle.heading())
		offset_x = 10 * math.cos(heading_angle + math.pi / 2)
		offset_y = 10 * math.sin(heading_angle + math.pi / 2)
		# offset_x = math.copysign(offset_x, math.sin(heading_angle))
		# offset_y = math.copysign(offset_y, -math.cos(heading_angle))
		# heading = turtle.heading() % 360
		#left ray #left down : - - // right down : + + // left up : + +
		#right ray #left down : + + // right down : - - // left up : - -
		ray_left = self.env.cast_ray((turtle.xcor() + offset_x, turtle.ycor() + offset_y), turtle.heading())
		ray_right = self.env.cast_ray((turtle.xcor() - offset_x, turtle.ycor() - offset_y), turtle.heading())
		turtle.clear()
		self.draw_raycast_turtle((turtle.xcor() + offset_x, turtle.ycor() + offset_y), ray_left, turtle.heading())
		self.draw_raycast_turtle((turtle.xcor() - offset_x, turtle.ycor() - offset_y), ray_right, turtle.heading())
		sys.stdout.write("\033[F\033[K" * 3)
		print(f"Ray left is : {ray_left}\nRay middle is : {env[0]}\nRay right is : {ray_right}")
		max_safe_dist = min(ray_left, ray_right, env[0])
		movement_distance = min(dist, max_safe_dist - 0.5)
		# if movement_distance > 0:
		# 	turtle.forward(math.floor(movement_distance))

	def	ft_backward(self, dist, turtle, env):
		return
		heading_angle = math.radians(turtle.heading())
		offset_x = 0.5 * math.cos(heading_angle + math.pi / 2)
		offset_y = 0.5 * math.sin(heading_angle + math.pi / 2)
		ray_left = self.env.cast_ray((turtle.xcor() + offset_x, turtle.ycor() + offset_y), turtle.heading() + 180)
		ray_right = self.env.cast_ray((turtle.xcor() - offset_x, turtle.ycor() - offset_y), turtle.heading() + 180)
		max_safe_dist = min(ray_left, ray_right)
		movement_distance = min(dist, max_safe_dist - 0.5)
		if movement_distance > 0:
			turtle.forward(math.floor(movement_distance))

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
			angle = 22.5 * float(cmd[1])
			if angle > 0:
				turtle.right(angle)
			else:
				turtle.left(-angle)
		elif cmd[0] == "RESET":
			turtle.setpos(self.start[0], self.start[1])
			turtle.setheading(self.start[2])
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
			test_x, test_y = self.env.turtle_to_image(self.turtles[i].pos())
			if (self.env.is_wall(test_x, test_y)):
				print("This turtle is stuck")
			self.update_env(self.turtles[i], f"{self.path[i]}env.txt", self.wall_dist[i])
			self.clear_file(f"{self.path[i]}action.txt")
		self.screen.ontimer(self.update, 1000)
	
	def	close_on_escape(self):
		self.screen.bye()

display = Display()

display.screen.listen()
display.screen.onkey(display.close_on_escape, "Escape")

display.update()
display.screen.mainloop()