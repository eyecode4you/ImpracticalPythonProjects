from random import randint
trials = 100000 #Times to compute
success = 0

for trial in range(trials):
	faces = set() #Non-repeated elements
	
	for rolls in range(6): #Roll 6 times
		roll = randint(1,6) #Random num between 1 - 6
		faces.add(roll) #Add result to set
		
	#If 6 different numbers (Each number is unique as we're using a set)
	if len(faces) == 6:
		success += 1

print("Trials =", trials)	
print("Successes =", success)
print("Probability of success = {} / {} = {}".format(success, trials, 
success/trials))
