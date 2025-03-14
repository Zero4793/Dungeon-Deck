import pygame
from button import Button

class Card:
	def __init__(self, _owner, _name):
		self.owner = _owner
		self.name = _name
		self.pos = pygame.Vector2(0,0)
		self.button = Button(self.owner.gamestate, (0,0), (100,150), None, ((200,200,200), (150,150,150), (100,100,100), (0,0,0)))

	def __str__(self) -> str:
		return self.name
	
	def displayCard(self, screen, x, y, hide, smooth=1):
		if smooth:
			self.pos += (pygame.Vector2(x,y)-self.pos)/smooth
			self.button.pos += (pygame.Vector2(x,y)-self.button.pos)/smooth
			# self.button.pos = self.pos
		width, height = 100, 150
		pygame.draw.rect(screen, (200,200,200), (self.pos.x, self.pos.y, width, height))
		pygame.draw.rect(screen, (150,150,150), (self.pos.x, self.pos.y, width, height), 5)
		if hide: return
		write = self.owner.gamestate.write
		write(screen, self.name, (self.pos.x+7, self.pos.y+5), 15, (0,0,0))

class Spell(Card):
	def __init__(self, _owner, _name):
		super().__init__(_owner, _name)

		# triggers
		self.onCast = []

	def cast(self):
		self.owner.hand.remove(self)
		for fn in self.onCast:
			fn(self)
		self.owner.graveyard.append(self)

class Summon(Card):
	def __init__(self, _owner, _name, _atk=0, _hp=0):
		super().__init__(_owner, _name)
		self.dead = False
		self.atk = _atk
		self.hp = _hp
		self.maxhp = _hp
		self.tapped = True

		self.stored = None

		# triggers
		self.onPlay = []
		self.onSummon = []
		self.onDeath = []
		self.onKill = []
		self.onAttack = []
		self.onDefend = []
		self.onDamage = []
		self.onHurt = []
		self.onTap = []
		self.onUntap = []
		self.onTurnStart = []
		self.onTurnEnd = []
		self.onHeal = []
		self.onBuff = []

	def __str__(self) -> str:
		t = '💤 ' if self.tapped else '💪 '
		return f'{t}{self.name} {self.atk}/{self.hp}'

	def displayCard(self, screen, x, y, hide, smooth=1):
		super().displayCard(screen, x, y, hide, smooth)
		if hide: return
		pygame.draw.rect(screen, (100,100,150), (self.pos.x+5, self.pos.y+120, 25, 25))
		pygame.draw.rect(screen, (150,100,100), (self.pos.x+70, self.pos.y+120, 25, 25))
		write = self.owner.gamestate.write
		write(screen, f"{f'{self.atk}'}", (self.pos.x+10, self.pos.y+125), 15, (0,0,0))
		write(screen, f"{f'{self.hp}':>7}", (self.pos.x+63, self.pos.y+125), 15, (0,0,0))

	def displayToken(self, screen, x, y, smooth=1):
		if smooth:
			self.pos += (pygame.Vector2(x,y)-self.pos)/smooth
		col = (200,200,200)
		if self.tapped:
			col = (100,100,100)
		elif self.dead: #dead not working properly? fix its logic
			col = (200,100,100)
		pygame.draw.rect(screen, col, (self.pos.x, self.pos.y, 100, 100))
		pygame.draw.rect(screen, (150,150,150), (self.pos.x, self.pos.y, 100, 100), 5)
		write = self.owner.gamestate.write
		write(screen, self.name, (self.pos.x+7, self.pos.y+5), 15, (0,0,0))
		pygame.draw.rect(screen, (100,100,150), (self.pos.x+5, self.pos.y+70, 25, 25))
		pygame.draw.rect(screen, (150,100,100), (self.pos.x+70, self.pos.y+70, 25, 25))
		write(screen, f"{f'{self.atk}'}", (self.pos.x+10, self.pos.y+75), 15, (0,0,0))
		write(screen, f"{f'{self.hp}\{self.maxhp}':>7}", (self.pos.x+63, self.pos.y+75), 15, (0,0,0))

	### Actions

	def play(self, pos):
		def action():
			print(f'{self.name} played')
			self.owner.hand.remove(self)
			self.owner.board.insert(pos, self)
			for fn in self.onPlay:
				fn(self)
			self.summon()
		self.owner.gamestate.events.append((30, action))

	def summon(self):
		self.tapped = True
		self.dead = False
		self.hp = self.maxhp
		for fn in self.onSummon:
			fn(self)

	def attack(self, foe):
		def action():
			print(f'{self.name} attacks {foe.name}')
			for fn in self.onAttack:
				fn(self, foe)
			for fn in foe.onDefend:
				fn(foe, self)
			self.tap()
			foe.takeDamage(self.atk)
			self.takeDamage(foe.atk)
		self.owner.gamestate.events.append((120, action))

	def attackFace(self, player):
		def action():
			print(f'{self.name} attacks Player {player.id}')
			for fn in self.onAttack:
				fn(self, player)
			self.tap()
			player.life -= self.atk
			if player.life <= 0:
				player.gamestate.win = 1 - player.id
		self.owner.gamestate.events.append((120, action))

	def takeDamage(self, dmg):
		def action():
			print(f'{self.name} takes {dmg} damage')
			self.hp = self.hp - dmg
			if self.dead: return # once dead still let hp go negative (fun) but dont trigger any further actions (onHurt or die)
			for fn in self.onHurt:
				fn(self, dmg)
			if self.hp <= 0:
				self.die()
		self.owner.gamestate.events.append((60, action))

	def die(self):
		print(f'{self.name} died')
		self.dead = True
		for fn in self.onDeath:
			fn(self)
		def action():
			if not self.dead: return
			self.hp=0
			if self in self.owner.board:
				print(f'-{self.name}')
				self.owner.board.remove(self)
				self.owner.graveyard.append(self)
			else:
				print(f'ERR: {self.name} is already removed from the board')
		self.owner.gamestate.events.append((120, action))

	def tap(self):
		def action():
			print(f'{self.name} tapped')
			self.tapped = True
			for fn in self.onTap:
				fn(self)
		self.owner.gamestate.events.append((5, action))

	def untap(self):
		def action():
			print(f'{self.name} untapped')
			self.tapped = False
			for fn in self.onUntap:
				fn(self)
		self.owner.gamestate.events.append((5, action))

	def turnStart(self):
		self.untap()
		for fn in self.onTurnStart:
			fn(self)

	def turnEnd(self):
		for fn in self.onTurnEnd:
			fn(self)
	
	def heal(self, hp):
		def action():
			print(f'{self.name} healed {hp}')
			self.hp = min(self.hp + hp, self.maxhp)
			for fn in self.onHeal:
				fn(self)
		self.owner.gamestate.events.append((30, action))

	def buff(self, atk, hp):
		def action():
			print(f'{self.name} gains {atk}/{hp}')
			self.atk += atk
			self.hp += hp
			self.maxhp += hp
			for fn in self.onBuff:
				fn(self)
		self.owner.gamestate.events.append((30, action))

	def store(self, pos):
		def action():
			card = self.owner.board[pos]
			print(f'{self.name} kills and stores {card.name}')
			self.stored = card
			card.die()
		self.owner.gamestate.events.append((30, action))