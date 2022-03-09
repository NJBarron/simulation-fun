# LEARNING RESOURCE
# https://www.youtube.com/watch?v=84njPYepKIU

# PACKAGES
import numpy as np
import pygame
import sys
import random
import time

# PYGAME INITS
pygame.init()
pygame.font.init()

# COLORS
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# FONTS
sans_12 = pygame.font.SysFont('Comic Sans MS', 12)

# GAME VARIABLES
clock = pygame.time.Clock()
FRAME_RATE = 60
BACKGROUND = BLACK
WIDTH = 600
HEIGHT = 400
RUNTIME = time.time()

# SIMLUATION VARIABLES
# COLLISIONS ON WITH CLICK_POWER > 1 WILL CAUSE OBJECTS TO FREEZE
START_NODES = 50
CLICK_POWER = 1
COLLISIONS  = False
INFO 		= True

# SETUP PROGRAM
screen = pygame.display.set_mode([WIDTH, HEIGHT], pygame.RESIZABLE)
container = pygame.sprite.Group()

# HELPERS
def newNode(x=None, y=None):

	if x == None or y == None:
		x = np.random.randint(0, WIDTH + 1)
		y = np.random.randint(0, HEIGHT + 1)

	vel = np.random.rand(2) * 2 - 1
	node_color = (random.randint(0,255), random.randint(0,255), random.randint(0,255))

	node = Dot(x, y, WIDTH, HEIGHT, color=node_color, velocity=vel)
	container.add(node)

def getRUNTIME(RUNTIME):
	return round(time.time() - RUNTIME, 2)

def getWidth():
	return pygame.display.get_surface().get_size()[0]

def getHeight():
	return pygame.display.get_surface().get_size()[1]


# CLASS OBJECTS
class Dot(pygame.sprite.Sprite):
	def __init__(self, x, y, width, height, color=BLACK, radius=5, velocity=[0, 0]):
		super().__init__()

		radius = random.randint(6, 9)

		self.image = pygame.Surface([radius * 2, radius * 2])
		pygame.draw.circle(self.image, color, (radius, radius), radius)

		self.rect = self.image.get_rect()
		self.pos = np.array([x, y], dtype=np.float64)
		self.vel = np.asarray(velocity, dtype=np.float64)

		self.WIDTH = width
		self.HEIGHT = height

		self.COLLIDED = False

	def update(self):

		
		if COLLISIONS:
			if self.COLLIDED:
				self.pos += self.vel
			else:
				self.pos -= self.vel
		else:
			self.pos += self.vel


		x, y = self.pos

		if x < 0:
			self.pos[0] = getWidth()
			x = getWidth()

		if x > getWidth():
			self.pos[0] = 0
			x = 0

		if y < 0:
			self.pos[1] = getHeight()
			y = getHeight()

		if y > getHeight():
			self.pos[1] = 0
			y = 0

		self.rect.x = x
		self.rect.y = y

	def collide(self, container):
		if pygame.sprite.spritecollide(self, container, False):

			if self.COLLIDED:
				self.COLLIDED = False
			else:
				self.COLLIDED = True


# GENERATE START_NODES
for x in range(START_NODES):
	newNode(getWidth()/2, getHeight()/2)

# GAME LOOP
while 1:

	# EVENT HANDLER
	for event in pygame.event.get():

		if event.type == pygame.QUIT:
			sys.exit()
		elif event.type == pygame.MOUSEBUTTONUP:

			for _ in range(CLICK_POWER):
				pos = pygame.mouse.get_pos()
				newNode(pos[0], pos[1])

	# RENDER

	screen.fill(BACKGROUND)

	for obj in container:
		container.remove(obj)
		obj.collide(container)
		container.add(obj)

	container.update()
	container.draw(screen)

	if INFO:
		textsurface = sans_12.render(f"objects {len(container.sprites())}", True, RED)
		screen.blit(textsurface, (0, 0))
		textsurface = sans_12.render(f"runtime {getRUNTIME(RUNTIME)}", True, RED)
		screen.blit(textsurface, (0, 15))
		

	# GAME TICK

	pygame.display.flip()
	clock.tick(FRAME_RATE)

