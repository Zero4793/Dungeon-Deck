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

	def displaySelf(self, screen):
		W,H = screen.get_size()
		self.gamestate.write(screen,f'Life: {self.life}', (110,H-40))
		self.displayDecks(screen,5,H-155)
		self.displayHand(screen,W/2,H-150)
		self.displayBoard(screen,W/2,H/2+25)
		return

	def displayRival(self, screen):
		W,H = screen.get_size()
		self.gamestate.write(screen,f'Life: {self.life}', (110,5))
		self.displayDecks(screen,5,5)
		self.displayRivalHand(screen,W/2,0)
		self.displayBoard(screen,W/2,H/2-125)
		return
	
	def displayDecks(self, screen, px, py):
		# Draw deck
		pygame.draw.rect(screen, (100,100,100), (px, py, 100, 150))
		self.gamestate.write(screen,f'{len(self.deck)}', (px+20, py+40), 50)
		# Graveyard
		px += screen.get_width()-105
		pygame.draw.rect(screen, (100,100,100), (px, py, 100, 150))
		self.gamestate.write(screen,f'{len(self.graveyard)}', (px+30, py+40), 50)

	def displayHand(self, screen, mid, y):
		w = min(800,105*len(self.hand))
		d = (w-100)/(len(self.hand)-1) if len(self.hand)>1 else 0
		x = mid - w/2
		for card in self.hand:
			card.displayInHand(screen, x, y)
			x += d

	def displayRivalHand(self, screen, mid, y):
		w = min(800,105*len(self.hand))
		d = (w-100)/(len(self.hand)-1) if len(self.hand)>1 else 0
		x = mid - w/2
		for card in self.hand:
			pygame.draw.rect(screen, (200,200,200), (x, y, 100, 150))
			pygame.draw.rect(screen, (150,150,150), (x, y, 100, 150), 5)
			x += d
	
	def displayBoard(self, screen, mid, y):
		w = min(screen.get_width()-100,105*len(self.board))
		d = (w-100)/(len(self.board)-1) if len(self.board)>1 else 0
		x = mid - w/2
		for card in self.board:
			card.displayOnBoard(screen, x, y)
			x += d

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
