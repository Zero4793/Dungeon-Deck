import random
from copy import deepcopy
import pygame

class Player:
	def __init__(self, _gamestate, _id):
		self.gamestate = _gamestate
		self.id = _id
		self.opp = None
		self.deck = None
		self.graveyard = []
		self.hand = []
		self.board = []
		self.life = 20

	def render(self, screen, y):
		font = pygame.font.SysFont('Arial', 30)
		for i,card in enumerate(self.board):
			card.render(screen, (i*100, y))
		stats = font.render(f'Life: {self.life} | Deck: {len(self.deck)} | Hand: {len(self.hand)} | Grave: {len(self.graveyard)}', True, (200,200,200))  # Black text
		screen.blit(stats, (0, y+100))

	def draw(self, num):
		for _ in range(num):
			def action():
				if not self.deck:
					return
				print(f'Player {self.id} draws a card')
				self.hand.append(self.deck.pop())
			self.gamestate.events.append((30, action))

	def startTurn(self):
		print(f'Player {self.id} starts turn:')
		self.draw(1)
		# TODO: upkeep effects
		for card in self.board:
			card.turnStart()

	def endTurn(self):
		print(f'Player {self.id} ends turn:')
		for card in self.board:
			card.turnEnd()

	def chooseAction(self, gamestate) -> tuple:
		return random.choice(gamestate.legalMoves())
	
	def __str__(self) -> str:
		s =  f'\nLife: {self.life} | Deck: {len(self.deck)} | Hand: {len(self.hand)} | Grave: {len(self.graveyard)}'
		s += f'\nBoard: {str([str(card) for card in self.board])}'
		return s

	def summon(self, _card):
		def action():
			print(f'{_card.name} summoned')
			card = deepcopy(_card)
			self.board.append(card)
			card.owner = self
			card.summon()
		self.gamestate.events.append((30, action))
