import pygame

class Card:
	def __init__(self, _owner, _name):
		self.owner = _owner
		self.name = _name

	def __str__(self) -> str:
		return self.name
	
	def render(self, screen, pos, size=100):
		x, y = pos
		height = size
		width = size

		# Set up font
		pygame.font.init()
		font = pygame.font.SysFont('Arial', 20)

		# Draw the rectangle
		pygame.draw.rect(screen, (200, 200, 200), (x, y, width, height))  # White background
		pygame.draw.rect(screen, (0, 0, 0), (x, y, width, height), 2)  # Black border

		# Render the card name at the top
		name_text = font.render(self.name, True, (0, 0, 0))  # Black text
		screen.blit(name_text, (x+5, y+5))

class Spell(Card):
	def __init__(self, _owner, _name):
		self.owner = _owner
		self.name = _name

		# triggers
		self.onCast = []

	def cast(self):
		self.owner.hand.remove(self)
		for fn in self.onCast:
			fn(self)
		self.owner.graveyard.append(self)

class Summon(Card):
	def __init__(self, _owner, _name, _atk=0, _hp=0):
		self.owner = _owner
		self.name = _name
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

	def render(self, screen, pos, size=100):
		x, y = pos
		height = size
		width = size

		# Set up font
		pygame.font.init()
		font = pygame.font.SysFont('Arial', 20)

		# Draw the rectangle
		fill = (200, 200, 200)
		if self.tapped:
			fill = (150, 150, 150)
		if self.dead:
			fill = (200, 100, 100)
		pygame.draw.rect(screen, fill, (x, y, width, height))  # background
		pygame.draw.rect(screen, (0), (x, y, width, height), 2)  # border

		# Render the card name at the top
		name_text = font.render(self.name, True, (0, 0, 0))  # Black text
		screen.blit(name_text, (x+5, y+5))

		# Render the card stats at the bottom
		stats_text = font.render(f'{self.atk}/{self.hp}', True, (0, 0, 0))  # Black text
		screen.blit(stats_text, (x+5, y+height-25))

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