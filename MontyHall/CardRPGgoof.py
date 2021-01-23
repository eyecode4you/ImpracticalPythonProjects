import random #used to simulate die roll - used for attacks

class Dwarf(object):
	
	def __init__(self, name):
		"Constructor - Define class stats"
		self.name = name
		self.attack = 3
		self.defend = 4
		self.hp = 5
		
	def talk(self):
		print("I'll cut you in half!!!")
		
player = Dwarf("Siegfreid")
print("Dwarf name = {}".format(player.name))
print("Player attack strength = {}".format(player.attack))
print("\n{} says:".format(player.name))
player.talk()


class Elf(object):
	def __init__(self, name):
		self.name = name
		self.attack = 4
		self.defend = 4
		self.hp = 4
		
enemy = Elf("Thalamor")
print("\nElf name = {}".format(enemy.name))
print("Enemy HP = {}".format(enemy.hp))

player_attack_roll = random.randrange(1, player.attack + 1)
print("\nPlayer attack roll = {}".format(player_attack_roll))

enemy_defend_roll = random.randrange(1, enemy.defend + 1)
print("Enemy defend roll = {}".format(enemy_defend_roll))

damage = player_attack_roll - enemy_defend_roll
if damage > 0:
	enemy.hp -= damage
	
print("\nEnemy HP = {}".format(enemy.hp))
