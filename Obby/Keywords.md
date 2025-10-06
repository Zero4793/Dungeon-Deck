# Targeting
target
this/other
any/all/it/the
ally/enemy
you/your = ally player
them/their = enemy player
player
[[Summon]]
# Types
fungi
flora
fauna
	mammal
	avian
	dinosaur
sapient
	human
undead
	zombie
	skeleton
	spirit
[[Spell]]
arcane
flame
nature
divine
necro
gear
	weapon
	armour
	staff
###### Decided
* [[Minion]]
* [[Spell]]
###### Uncertain
* [[Item]]
* [[Titan]]
* Structure
* Vehicle
* Enchantment *persisting spells. dont require sustain*
* Equipment/Equipable/Item/Tool *can be weapons, activated spells (hero powers), or magic items that grant passive abilites*
	* Weapon *Not have HP, just ATK DEF ARM*
	* Spell/Power *can any spell be put in equip slot to be used again?*
	* Magic Item *passive abilities*
* Dungeon/meta
# Damage Types
Damage can be explicitly clarified with type eg 'Deal 1 Arcane'. If not they can inherit the type of the Spell or Minion dealing the Damage. A Flame Minions attacks deal Flame dmg.
[[Flame]]
[[Arcane]]
[[Lifesteal]]
# Passives
[[Ranged]]
[[Pierce]]
[[Fatal]]
[[Cover|Covered]]
[[Shield]]
[[Charge]]
[[Parry]](x)
[[Tough]](x)
[[Rampage]]
[[ward]](cost)
[[sustain]](cost)
# Triggers
*Common/simple/staple triggers are in the form onTrigger*
[[onPlay]]:
[[onSpawn]]:
[[onAttack]]:
[[onKill]]:
[[onOverkill]]:
[[onDefend]]:
[[onHurt]]:
[[onSurvive]]:
[[onDeath]]:
[[onTurnStart]]:
[[onTurnEnd]]:
onTap:
onUntap:
Invoked:
*Rare/complex triggers use when*
[[when]](trigger):
*Passive/conditional triggers use while*
[[while]](trigger):
# Actions
target gains X
gain X
deal target # (type)
[[Heal]] target # 
[[spawn]] target
[[play]] target
[[cast]] [[Spell]] at target
[[recruit]] target
[[Raise]] target
[[draw]] #
[[discard]] #
[[invoke]]:
# Structural
[[for/per]](x): *repeat effect x times*
[[forEach]](target): *repeat for all instances of target. also able to effect target via this keyword?*
