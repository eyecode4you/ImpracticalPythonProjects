import random

#Prompt user to enter number of times to run simulation or defaultv
def user_prompt(prompt, default=None):
	"""Allow use of default values in input"""
	prompt = "{} [{}]: ".format(prompt, default)
	response = input(prompt)
	if not response and default:
		return default
	else:
		return response
		
#Input number of times to run simulation
num_runs = int(user_prompt("Input number of runs", "20000"))

#Assign counters for ways to win
first_choice_wins = 0
pick_change_wins = 0
doors = ['a', 'b', 'c']

#Run MCS
for i in range(num_runs):
	winner = random.choice(doors)
	pick = random.choice(doors)
	
	if pick == winner:
		first_choice_wins += 1
	else:
		pick_change_wins += 1
		
print("Wins with original pick: {}".format(first_choice_wins))
print("Wins with changed pick: {}".format(pick_change_wins))
print("Prob of win with initial guess: {}".format(first_choice_wins/num_runs))
print("Prob of win with by switching: {}".format(pick_change_wins/num_runs))
