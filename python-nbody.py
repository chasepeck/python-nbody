import pygame
import math
import random
from sys import argv

#Initialize
pygame.init()
pygame.mixer.init()

icon = pygame.image.load("icon.png")
boom = pygame.mixer.Sound("boom.wav")

pygame.display.set_icon(icon)
pygame.display.set_caption("Python N-body")

window = pygame.display.set_mode((int(argv[1]), int(argv[2])))

G = int(argv[3]) #6.67408 * 10 ** 11

collisions = bool(int(argv[4]))
trails = bool(int(argv[5]))

bodies = []
setmass = 10
stationary = False
start_x = None
start_y = None

def update():
	global bodies
	global setmass
	global stationary
	global start_x
	global start_y

	#Set background
	window.fill((0, 0, 0))

	#Event loop
	for event in pygame.event.get():
		if event.type == pygame.MOUSEBUTTONDOWN:
			start_x, start_y = event.pos

		if event.type == pygame.MOUSEBUTTONUP:
			x, y = event.pos
			div = 100
			xvel = (x - start_x) / div
			yvel = (y - start_y) / div

			if abs(xvel) < 0.5:
				xvel = 0
			if abs(yvel) < 0.5:
				yvel = 0

			bodies.append(Body(start_x, start_y, xvel, yvel, setmass, stationary, len(bodies)))
			start_x = None
			start_y = None

		if event.type == pygame.KEYDOWN:
			if event.unicode == "=":
				setmass += 1
			elif event.unicode == "+":
				setmass += 10
			elif event.unicode == "-":
				setmass -= 1
			elif event.unicode == "_":
				setmass -= 10
			elif event.unicode == "s":
				if stationary:
					stationary = False
				else:
					stationary = True

		if event.type == pygame.QUIT:
			running = False

	#Draw body preview
	if start_x != None and start_y != None:
		pygame.draw.circle(window, (100, 100, 100), (start_x, start_y), setmass, 0)
		pygame.draw.line(window, (100, 100, 100), (start_x, start_y), pygame.mouse.get_pos())

	#Update all bodies
	for i in range(0,len(bodies)):
		if i < len(bodies):
			bodies[i].update(i)

	#Display information
	font = pygame.font.SysFont(None, 24)
	text = [
		font.render("Bodies: "+str(len(bodies)), True, (100, 100, 100)),
		font.render("Mass (+, - keys): "+str(setmass), True, (100, 100, 100)),
		font.render("Stationary (S key): "+str(stationary), True, (100, 100, 100))
	]
	for i in range(0,len(text)):
		window.blit(text[i], (20, 20 + 20 * i))

	#Update display
	pygame.display.update()




class Body:
	def __init__(self, x, y, xvel, yvel, mass, stationary, index):
		self.x = x
		self.y = y
		self.xvel = xvel
		self.yvel = yvel
		self.mass = mass
		self.stationary = stationary
		self.index = index

		self.color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
		self.history = []

	def update(self, index):
		self.index = index

		self.x += self.xvel
		self.y += self.yvel

		for body in bodies:
			if body.index != self.index:
				dist_x = abs(body.x - self.x)
				dist_y = abs(body.y - self.y)
				dist = math.sqrt(dist_x ** 2 + dist_y ** 2)

				force = G * (body.mass * self.mass / dist ** 2)

				if not self.stationary:
					self.xvel += (body.x - self.x) / dist * force
					self.yvel += (body.y - self.y) / dist * force

				if not body.stationary:
					body.xvel += (self.x - body.x) / dist * force
					body.yvel += (self.y - body.y) / dist * force

				if trails:
					self.history.append((self.x, self.y))

				if dist <= self.mass + 10 and collisions:
					boom.play()
					if self.mass > body.mass:
						del bodies[body.index]
					else:
						del bodies[self.index]
		self.draw()

	def draw(self):
		if trails:
			for i in range(1, len(self.history)):
				pygame.draw.line(window, self.color, self.history[i-1], self.history[i])
			if len(self.history) >= 10000:
				del self.history[0]

		pygame.draw.circle(window, self.color, (self.x, self.y), self.mass, 0)

		if self.stationary:
			font = pygame.font.SysFont(None, int(self.mass * 1.2))
			s = font.render("S", True, (0, 0, 0))
			window.blit(s, (self.x - self.mass / 4, self.y - self.mass / 3))



#Main
running = True

while running:
	update()