import pygame
import sys
from gamestate import Gamestate
from card import Card

# Initialize Pygame and main screen
pygame.init()
screen = pygame.display.set_mode((800, 450))
pygame.display.set_caption('Dungeon Deck')
clock = pygame.time.Clock()

def main():
	keyheld = set()
	game = Gamestate()

	while True:
		# Handle events
		events = pygame.event.get()
		for event in events:
			# Quit the game
			if event.type == pygame.QUIT:
				return
			# track held keys
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE:
					return
				if event.key == pygame.K_RETURN and not game.events:
					# take action
					game = game.update()
				keyheld.add(pygame.key.name(event.key))
			if event.type == pygame.KEYUP and pygame.key.name(event.key) in keyheld:
				keyheld.remove(pygame.key.name(event.key))

		game.process()
		if not game.events:
			game = game.update()
		if game.win is not None:
			print(f'Player {game.win} wins!')
			return

		col = (50,50,50) if game.events else (0)
		screen.fill(col)
		# game.display()
		game.render(screen)

		# Update/render the display
		pygame.display.flip()
		# Cap the frame rate
		clock.tick(60)

		
main()
pygame.quit()
sys.exit()
