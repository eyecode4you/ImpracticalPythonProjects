#safe_cracker.py

import time
from random import randint, randrange

def fitness(combo, attempt):#takes true combination (code) and attempted one
	"""Compare items in two lists and count no. of matches"""
	grade = 0
	for i, j in zip(combo, attempt):
		if i == j:
			grade += 1
	return grade
	
def main():
	"""Use hill-climbing algorithm to solve lock combination"""
	combination = "6822456"
	print("Combination: {}".format(combination))
	#Convert combination to list
	combo = [int(i) for i in combination]
	
	#generate guess & grade fitness
	best_attempt = [0] * len(combo)#list of 0s equal to combination length
	best_attempt_grade = fitness(combo, best_attempt)
	
	count = 0#count how many attempts to crack code
	
	#evolve guess
	while best_attempt != combo:
		#crossover
		next_try = best_attempt[:]#copy best_attempt to next_try
		
		#mutate
		lock_wheel = randrange(0, len(combo))
		next_try[lock_wheel] = randint(0, 9)
		
		#grade & select
		next_try_grade = fitness(combo, next_try)
		if next_try_grade > best_attempt_grade:
			best_attempt = next_try[:]
			best_attempt_grade = next_try_grade
		print(next_try, best_attempt)
		count += 1
		
	print()
	print("Cracked!: {}".format(best_attempt), end=' ')
	print("In {} tries!".format(count))

if __name__ == "__main__":
	start_time = time.time()
	main()
	end_time = time.time()
	duration = end_time - start_time
	print("\nRuntime: {} seconds".format(duration))
