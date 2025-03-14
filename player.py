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

	def process(self):
		for card in self.hand:
			card.button.process()

	def displaySelf(self, screen):
		W,H = screen.get_size()
		self.gamestate.write(screen,f'Life: {self.life}', (110,H-40))
		self.displayDecks(screen,5,H-155)
		self.displayBoard(screen,W/2,H/2+25)
		self.displayHand(screen,W/2,H-150,False)

	def displayRival(self, screen):
		W,H = screen.get_size()
		self.gamestate.write(screen,f'Life: {self.life}', (110,5))
		self.displayDecks(screen,5,5)
		self.displayBoard(screen,W/2,H/2-125)
		self.displayHand(screen,W/2,0,True)
	
	def displayDecks(self, screen, px, py):
		# Graveyard
		pygame.draw.rect(screen, (100,100,100), (px, py, 100, 150))
		self.gamestate.write(screen,f'{len(self.graveyard)}', (px+25, py+45), 50)
		# Deck
		px += screen.get_width()-110
		pygame.draw.rect(screen, (100,100,100), (px, py, 100, 150))
		self.gamestate.write(screen,f'{len(self.deck)}', (px+25, py+45), 50)

	def displayHand(self, screen, mid, y, hide):
		w = min(800,105*len(self.hand))
		d = (w-100)/(len(self.hand)-1) if len(self.hand)>1 else 0
		x = mid - w/2
		held = None
		for card in self.hand:
			card.displayCard(screen, x, y, hide, 10)
			x += d
			if hide: continue
			if card.button.held():
				held = card
			elif card.button.hover:
				card.pos.y-=5
		if held:
			held.owner.gamestate.cursorTarget(screen, held.pos + pygame.Vector2(50, 0))
			held.pos.y-=10

	def displayBoard(self, screen, mid, y):
		w = min(screen.get_width()-100,105*len(self.board))
		d = (w-100)/(len(self.board)-1) if len(self.board)>1 else 0
		x = mid - w/2
		for card in self.board:
			card.displayToken(screen, x, y, 5)
			x += d

	def draw(self, num):
		for _ in range(num):
			def action():
				if not self.deck:
					return
				print(f'Player {self.id} draws a card')
				self.hand.append(self.deck.pop())
			self.gamestate.events.append((30, action))

	def summon(self, _card):
		def action():
			print(f'{_card.name} summoned')
			card = deepcopy(_card)
			self.board.append(card)
			card.owner = self
			card.summon()
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

