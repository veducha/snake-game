import pygame 
from pygame.locals import *
import time
import random as rn

import constants as c

class Apple:
	def __init__(self, parent_screen):
		self.parent_screen = parent_screen
		self.x = rn.randint(0,c.GRID_SIZE)*c.BLOCK
		self.y = rn.randint(0,c.GRID_SIZE)*c.BLOCK

	def draw(self):
		pygame.draw.rect(self.parent_screen, c.RED, [self.x,self.y, c.BLOCK, c.BLOCK], border_radius= 10)

	def move(self):
		self.x = rn.randint(0,c.GRID_SIZE)*c.BLOCK
		self.y = rn.randint(0,c.GRID_SIZE)*c.BLOCK

class Snake:
	def __init__(self, parent_screen, length):
		self.parent_screen = parent_screen
		self.length = length
		self.x = [c.X0]*length
		self.y = [c.Y0]*length
		self.direction = 'right'

	def draw(self):
		pygame.draw.rect(self.parent_screen, c.DARK_GREEN , [self.x[0], self.y[0], c.BLOCK, c.BLOCK], border_radius= 5)
		for i in range(1, self.length):
				pygame.draw.rect(self.parent_screen, c.GREEN , [self.x[i], self.y[i], c.BLOCK, c.BLOCK], border_radius=5)

	def grow(self):
		self.length += 1
		self.x.append(-1)
		self.y.append(-1)

	def move_up(self):
		if self.direction != 'down':
			self.direction = 'up'
	def move_down(self):
		if self.direction != 'up':
			self.direction = 'down'
	def move_left(self):
		if self.direction != 'right':
			self.direction = 'left'
	def move_right(self):
		if self.direction != 'left':
			self.direction = 'right'


	def walk(self):
		for i in range(self.length-1,0,-1):
			self.x[i] = self.x[i-1] 
			self.y[i] = self.y[i-1]			

		if self.direction == 'up':
			self.y[0] = (self.y[0] - c.BLOCK) % c.WIDTH

		if self.direction == 'down':
			self.y[0] = (self.y[0] + c.BLOCK) % c.WIDTH

		if self.direction == 'left':
			self.x[0] = (self.x[0] - c.BLOCK) % c.WIDTH	

		if self.direction == 'right':
			self.x[0] = (self.x[0] + c.BLOCK) % c.WIDTH


class Game:
	def __init__(self):
		pygame.init()
		self.surface = pygame.display.set_mode([c.HEIGHT, c.WIDTH])
		self.surface.fill(c.BEIGE)

		self.snake = Snake(self.surface, 3)
		self.apple = Apple(self.surface)


	def apple_snake_collision(self):
		snakeX = self.snake.x[0]
		snakeY = self.snake.y[0]

		appleX = self.apple.x
		appleY = self.apple.y

		if snakeX == appleX and snakeY == appleY:
			return True
		

	def snake_self_collision(self):
		snakeHeadX = self.snake.x[0]
		snakeHeadY = self.snake.y[0]

		for i in range(3,self.snake.length):
			if snakeHeadX == self.snake.x[i] and snakeHeadY == self.snake.y[i]:
				return True
				

	def display_score(self):
		font = pygame.font.SysFont('arial', size = 20)
		score = font.render(f'Score: {self.snake.length}', True, c.BLACK)
		self.surface.blit(score, (0,0))


	def show_game_over(self):
		self.surface.fill(c.BLACK)
		font = pygame.font.SysFont('arial', size = 40)
		line1 = font.render(f"Game over!", True, c.WHITE)
		self.surface.blit(line1,(100,200))

		font = pygame.font.SysFont('arial', size = 20)
		line2 = font.render(f"Your score is {self.snake.length}", True, c.WHITE)
		self.surface.blit(line2, (180,250))

		font = pygame.font.SysFont('arial', size = 10)
		line2 = font.render("Press enter to start again, or escape to exit", True, c.WHITE)
		self.surface.blit(line2, (80,300))
		pygame.display.flip()

	def reset(self):
		self.snake = Snake(self.surface, 1)
		self.apple = Apple(self.surface)

	def animate(self):
		self.surface.fill(c.BEIGE)
		self.apple.draw()
		self.snake.walk()
		self.snake.draw()
		self.display_score()
		pygame.display.flip()


	def logic(self):
		if self.apple_snake_collision() == True:
			self.snake.grow()
			self.apple.move()

		if self.snake_self_collision() == True:
			raise "Collision occured"


	def run(self):
		running = True
		pause = False

		while running:
			for event in pygame.event.get():
				if event.type == KEYDOWN:

					if event.key == K_RETURN:
						pause = not pause

					if event.key == K_ESCAPE:
							running = False
					if not pause:
						if event.key == K_UP:
							self.snake.move_up()

						if event.key == K_DOWN:
							self.snake.move_down()

						if event.key == K_LEFT:
							self.snake.move_left()

						if event.key == K_RIGHT:
							self.snake.move_right()

				elif event.type == QUIT:
					running = False
			
			if self.snake_self_collision() == True:
				pause = True
				self.show_game_over()

			
			try:
				if not pause:
					self.animate()
					self.logic()
			except Exception as e:
				self.show_game_over()
				pause = True
				self.reset()




			time.sleep(c.SPEED)



if __name__ == "__main__":
	game = Game()
	game.run()



