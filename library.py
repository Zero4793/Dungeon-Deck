from card import *
from copy import deepcopy

def pickDeck(p):
	deck = []

	goblin = Summon(p,'Goblin', 1, 1)
	deck.append(goblin)

	hobgoblin = Summon(p,'Hobgoblin', 4, 4)
	hobgoblin.onAttack.append(lambda this, _: this.buff(1,0))
	hobgoblin.onPlay.append(lambda this: this.owner.summon(goblin))
	hobgoblin.onPlay.append(lambda this: this.owner.summon(goblin))
	deck.append(hobgoblin)

	slime = Summon(p,'Slime', 1, 1)
	deck.append(slime)

	megaslime = Summon(p,'Mega Slime', 4, 4)
	megaslime.onHurt.append(lambda this, _: this.owner.summon(slime))
	deck.append(megaslime)

	ultraslime = Summon(p,'Ultra Slime', 6, 6)
	ultraslime.onHurt.append(lambda this, _: this.owner.summon(megaslime))
	deck.append(ultraslime)

	barbarian = Summon(p,'Barbarian', 5, 5)
	barbarian.onHurt.append(lambda this, _: this.untap())
	deck.append(barbarian)

	rattlegore = Summon(p,'Rattle Gore', 6, 6)
	rattlegore.onDeath.append(lambda this: this.summon() if this.maxhp > 1 else None)
	rattlegore.onDeath.append(lambda this: this.buff(-1,-1) if this.maxhp > 1 else None)
	deck.append(rattlegore)

	mage = Summon(p,'Mage', 1, 1)
	mage.onPlay.append(lambda this: this.owner.draw(1))
	deck.append(mage)

	battlecry = Spell(p,'Battle Cry')
	battlecry.onCast.append(lambda this: [card.buff(1,1) for card in this.owner.board])
	deck.append(battlecry)

	heal = Spell(p,'Heal')
	heal.onCast.append(lambda this: [card.heal(1) for card in this.owner.board if card.hp < card.maxhp])
	deck.append(heal)

	bomb = Summon(p,'Bomb', 1, 1)
	bomb.onDeath.append(lambda this: [card.takeDamage(1) for card in this.owner.opp.board])
	deck.append(bomb)

	factory = Summon(p,'Factory', 0, 6)
	factory.onTurnStart.append(lambda this: this.owner.summon(bomb))
	deck.append(factory)

	clusterbomb = Summon(p,'Cluster Bomb', 0, 6)
	clusterbomb.onHurt.append(lambda this, _: this.owner.summon(bomb))
	deck.append(clusterbomb)

	boar = Summon(p,'Boar', 1, 1)
	boar.onDefend.append(lambda this, _: this.buff(1,0))
	deck.append(boar)

	cleric = Summon(p,'Cleric', 1, 1)
	cleric.onTurnEnd.append(lambda this: [card.heal(1) for card in this.owner.board if card.hp < card.maxhp])
	deck.append(cleric)

	carnivorouscube = Summon(p,'Carnivorous Cube', 4, 6)
	carnivorouscube.onPlay.append(lambda this: this.store(0) if this.owner.board[0].name != 'Carnivorous Cube' else None)
	carnivorouscube.onDeath.append(lambda this: this.owner.summon(this.stored) if this.stored else None)
	carnivorouscube.onDeath.append(lambda this: this.owner.summon(this.stored) if this.stored else None)
	deck.append(carnivorouscube)
	
	vampire = Summon(p,'Vampire', 1, 5)
	vampire.onPlay.append(lambda this: [card.takeDamage(1) for card in this.owner.opp.board])
	vampire.onPlay.append(lambda this: [card.heal(2) for card in this.owner.board if card.hp < card.maxhp])
	vampire.onHurt.append(lambda this, _: this.heal(1))
	deck.append(vampire)

	cannibal = Summon(p, 'Forced Canablisim', 1, 6)
	cannibal.onAttack.append(lambda this, _: this.takeDamage(1))
	cannibal.onAttack.append(lambda this, _: [card.heal(1) for card in this.owner.board if card.hp < card.maxhp and card != this])
	deck.append(cannibal)
	return deck
