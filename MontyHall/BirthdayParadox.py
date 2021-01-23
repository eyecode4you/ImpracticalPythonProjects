#BirthdayParadox.py - Probability of number of people in group having the same B-day
import random

people_in_group = int(input("How Many People in Group: "))
trials = 100000
success = 0 #Counter for B-Day matches
dup = 0 #Match duplicates (Self check values)

""" Execute Trials """
for i in range(trials):
	people = []
	for a in range(people_in_group):
		people.insert(a, a)
		
	""" Assign elements in people list to random day of year """
	for x in range(people_in_group):
		people[x] = random.randrange(0, 365)	
	for y in people:
		check = y #Value to check
		dup += 1 #Increment dup since 1st check is always a match
		for z in people:
			if check == z: #If match found
				success += 1
			else: #No match
				continue

success -= dup #Remove Self Matches
success = success/2 #Remove duplicate matches		
print("\nTrials:", trials)
print("Birthday Matches:", int(success))
res = (success / trials) * 100
print("\nProbability of Birthday Match with {} People Group: {} / {} = ~{:.2f}%".format(people_in_group, success, trials, res))
