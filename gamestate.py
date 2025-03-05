from player import Player
from card import *
from copy import deepcopy
import library
import random
from collections import deque
import pygame

class Gamestate:
	def __init__(self):
		self.events = deque()
		self.players = [Player(self, 0), Player(self, 1)]
		self.players[0].opp = self.players[1]
		self.players[1].opp = self.players[0]
		for player in self.players:
			player.deck = library.pickDeck(player)
			random.shuffle(player.deck)
			# [player.hand.append(player.deck.pop()) for _ in range(3)]
			player.draw(3)
		self.time = 0
		self.turn = 0
		self.win = None

	def display(self):
		for player in self.players:
			print(player)
		print('-'*50)

	def render(self, screen):
		for player in self.players:
			player.render(screen)
		width,height = screen.get_size()
		self.mouseTarget(screen,(width//2, height))

	def process(self):
		if self.time>0:
			self.time -=1
			return
		if not self.events:
			return
		self.time, action = self.events.popleft()
		action()

	def getPlayers(self) -> tuple[Player,Player]:
		return (self.players[self.turn], self.players[(self.turn+1)%2])
	
	def legalMoves(self) -> list[tuple]:
		p,o = self.getPlayers()
		actions = set()
		actions.add(('end turn',)) # comma makes sure its tuple, else python removes () making it a string

		# play cards
		for A in p.hand:
			# if cant afford: continue
			if isinstance(A,Spell):
				actions.add(('cast',A))
			else:
				for i in range(len(p.board)+1):
					actions.add(('play',A,i))
		# attack
		for A in p.board:
			if A.tapped: continue
			for B in o.board:
				# if cant reach (cover): continue
				actions.add(('attack',A,B))
			if len(o.board) == 0:
				actions.add(('attack-face',A,o))

		return list(actions)

	def update(self) -> 'Gamestate':
		next = deepcopy(self)

		p = next.players[next.turn]
		action = p.chooseAction(next)
		print(f'Player {next.turn} takes action: {[str(_) for _ in action]}')

		next.takeAction(action)
		return next
	
	def takeAction(self,action):
		p,o = self.getPlayers()

		if action[0] == 'end turn':
			self.turn = (self.turn+1)%2
			p.endTurn()
			o.startTurn()
		elif action[0] == 'play':
			action[1].play(action[2]) # card play at pos
		elif action[0] == 'cast':
			action[1].cast() # card cast
		elif action[0] == 'attack':
			action[1].attack(action[2]) # card atk foe
		elif action[0] == 'attack-face':
			action[1].attackFace(action[2]) # card atk player

	def mouseTarget(self, screen, start):
		mouse = pygame.Vector2(pygame.mouse.get_pos())
		start_pos = pygame.Vector2(start)
		end_pos = mouse

		distance = start_pos.distance_to(end_pos)
		midpoint = (start_pos + end_pos)/2
		cx,cy = .75,.5 #curvature amounts
		control_offset = pygame.Vector2((start_pos.x-mouse.x)*cx, -distance*cy)
		control_point = midpoint + control_offset

		segments = 36
		for t in (i / segments for i in range(segments + 1)):
			x = (1 - t)**2 * start_pos.x + 2 * (1 - t) * t * control_point.x + t**2 * end_pos.x
			y = (1 - t)**2 * start_pos.y + 2 * (1 - t) * t * control_point.y + t**2 * end_pos.y
			pygame.draw.circle(screen, (200, 200, 200), (int(x), int(y)), 5)
			# velocity