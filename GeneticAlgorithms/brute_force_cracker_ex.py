#Brute_force_cracker_ex.py
"""Brute Force a Combination"""
import time
from itertools import product

start_time = time.time() #Record time taken

combo = (9,9,7,6,5,4,5) #Time to crack is longer upon increase

#use cartesian product to generate permutations with repetition
for perm in product([0, 1, 2, 3, 4, 5, 6, 7, 8, 9], repeat=len(combo)):
	if perm == combo:
		print("Cracked!: {} {}".format(combo, perm))
		
end_time = time.time()
print("\nRuntime: {} seconds".format(end_time - start_time))
