import pygame
import math
import random
from sys import argv

#Initialize
pygame.init()

icon = pygame.image.load("icon.png")
boom = pygame.mixer.Sound("boom.wav")

pygame.display.set_icon(icon)
pygame.display.set_caption("Python N-body")

if len(argv) >= 3:
	width = int(argv[1])
	height = int(argv[2])
else:
	width = 1920
	height = 1080

window = pygame.display.set_mode((width, height))

if len(argv) >= 4:
	if argv[3] == "G":
		G = 6.67408 * 10 ** -11
	else:
		G = int(argv[3]) #6.67408 * 10 ** -11
else:
	G = 1

if len(argv) >= 5:
	trail_quality = int(argv[4])
else:
	trail_quality = 10000

DIV = 100
bodies = []
collisions = False
trails = False

cam_x = 0
cam_y = 0
cam_zoom = 1

simspeed = 1
setmass = 10
stationary = False
start_pos = None

def update():
	#Load global variables
	global bodies
	global collisions
	global trails

	global cam_x
	global cam_y
	global cam_zoom

	global simspeed
	global setmass
	global stationary
	global start_pos

	#Set background
	window.fill((0, 0, 0))

	#Event loop
	for event in pygame.event.get():
		if event.type == pygame.MOUSEBUTTONDOWN:
			if event.button == 1:
				start_pos = event.pos

		if event.type == pygame.MOUSEMOTION:
			if event.buttons[1] == 1:
				cam_x += event.rel[0] / cam_zoom
				cam_y += event.rel[1] / cam_zoom

		if event.type == pygame.MOUSEBUTTONUP:
			if event.button == 1:
				xvel = (event.pos[0] - start_pos[0]) / DIV
				yvel = (event.pos[1] - start_pos[1]) / DIV

				if abs(xvel) < 0.5 and abs(yvel) < 0.5:
					xvel = 0
					yvel = 0

				bodies.append(Body(start_pos[0] / cam_zoom - cam_x, start_pos[1] / cam_zoom - cam_y, xvel, yvel, setmass, stationary, len(bodies)))
				start_pos = None

		if event.type == pygame.MOUSEWHEEL:
			cam_zoom += event.y / 10

		if event.type == pygame.KEYDOWN:
			if event.unicode == "=":
				setmass += 1
			elif event.unicode == "+":
				setmass += 10
			elif event.unicode == "-":
				setmass -= 1
			elif event.unicode == "_":
				setmass -= 10
			elif event.unicode == "u":
				simspeed += 1
			elif event.unicode == "d":
				simspeed -= 1
			elif event.unicode == "s":
				if stationary:
					stationary = False
				else:
					stationary = True
			elif event.unicode == "c":
				if collisions:
					collisions = False
				else:
					collisions = True
			elif event.unicode == "t":
				if trails:
					trails = False
				else:
					trails = True
			elif event.unicode == "f":
				pygame.display.toggle_fullscreen()
			elif event.unicode == "r":
				bodies = []
				cam_x = 0
				cam_y = 0
				cam_zoom = 1
			elif event.unicode == "z":
				cam_x = 0
				cam_y = 0
				cam_zoom = 1
			elif event.key == 27:
				pygame.quit()
				exit()

	#Draw body preview
	if start_pos != None:
		pygame.draw.circle(window, (100, 100, 100), start_pos, abs(setmass) * cam_zoom, setmass <= 0)
		pygame.draw.line(window, (100, 100, 100), start_pos, pygame.mouse.get_pos())

	#Update all bodies
	for i in range(0,len(bodies)):
		if i < len(bodies):
			bodies[i].update(i)

	#Display information
	font = pygame.font.SysFont(None, 24)
	text = [
		font.render("Bodies: "+str(len(bodies)), True, (100, 100, 100)),
		font.render("Sim speed (U, D keys): "+str(simspeed), True, (150, 150, 100)),
		font.render("Mass (+, - keys): "+str(setmass), True, (100, 150, 100)),
		font.render("Stationary (S key): "+str(stationary), True, (100, 150, 100)),
		font.render("Collisions (C key): "+str(collisions), True, (100, 100, 150)),
		font.render("Trails (T key): "+str(trails), True, (100, 100, 150)),
	]
	text2 = [
		font.render("Click & drag LMB to create body", True, (150, 100, 100)),
		font.render("Click & drag MMB to move camera", True, (150, 100, 100)),
		font.render("Scroll to zoom", True, (150, 100, 100)),
		font.render("Press F to toggle fullscreen", True, (150, 100, 100)),
		font.render("Press Z to reset camera", True, (150, 100, 100)),
		font.render("Press R to reset", True, (150, 100, 100)),
		font.render("Press ESC to quit", True, (150, 100, 100)),
	]
	for i in range(0,len(text)):
		window.blit(text[i], (20, 20 + 20 * i))
	for i in range(0,len(text2)):
		window.blit(text2[i], (20, window.get_height() - 20 - 20 * len(text2) + 20 * i))

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
		for i in range(0, simspeed):
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

					if dist <= self.mass * 2 and collisions:
						boom.play()
						if self.mass > body.mass:
							del bodies[body.index]
						else:
							del bodies[self.index]

		self.history.append((self.x, self.y))
		if len(self.history) >= trail_quality:
			del self.history[0]
		self.draw()

	def draw(self):
		if trails:
			for i in range(1, len(self.history)):
				pygame.draw.line(
					window,
					self.color,
					((self.history[i-1][0] + cam_x) * cam_zoom,
					(self.history[i-1][1] + cam_y) * cam_zoom),
					((self.history[i][0] + cam_x) * cam_zoom,
					(self.history[i][1] + cam_y) * cam_zoom))

		if self.mass > 0:
			pygame.draw.circle(window, self.color, ((self.x + cam_x) * cam_zoom, (self.y + cam_y) * cam_zoom), self.mass * cam_zoom, 0)
		elif self.mass < 0:
			pygame.draw.circle(window, self.color, ((self.x + cam_x) * cam_zoom, (self.y + cam_y) * cam_zoom), -self.mass * cam_zoom, 1)

		if simspeed == 0:
			pygame.draw.line(window, (100, 100, 100),
				((self.x + cam_x) * cam_zoom, (self.y + cam_y) * cam_zoom),
				((self.x + cam_x + self.xvel * DIV) * cam_zoom, (self.y + cam_y + self.yvel * DIV) * cam_zoom))

		if self.stationary:
			font = pygame.font.SysFont(None, int(abs(self.mass) * 1.2 * cam_zoom))
			s = font.render("S", True, (0, 0, 0) if self.mass >= 0 else self.color)
			window.blit(s, ((self.x + cam_x) * cam_zoom - abs(self.mass) * cam_zoom / 4, (self.y + cam_y) * cam_zoom - abs(self.mass) * cam_zoom / 3))



#Main
while True:
	update()
