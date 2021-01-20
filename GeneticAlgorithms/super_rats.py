#super_rats.py
import time, random, statistics

#CONSTANTS (weight in grams)
GOAL = 50000
NUM_RATS = 20
INI_MIN_WT = 200
INI_MAX_WT = 600
INI_MODE_WT = 300
MUTATE_ODDS = 0.1
MUTATE_MIN = 0.5
MUTATE_MAX = 1.2
LITTER_SIZE = 8
LITTERS_PER_YEAR = 10
GENERATION_LIMIT = 500

#Ensure even-no. of rats for breeding pairs
if NUM_RATS % 2 != 0:
	NUM_RATS += 1
	
def populate(num_rats, min_wt, max_wt, mode_wt):
	"""Initialize a population with a triangular distro of weights"""
	return [int(random.triangular(min_wt, max_wt, mode_wt))\
			for i in range(num_rats)]
			
def fitness(population, goal):
	"""Measure population fitness based on an attribute mean vs target"""
	ave = statistics.mean(population)
	return ave / goal
	
def select(population, to_retain): # to_retain = NUM_RATS
	"""Cull a population to retain only a specified no. of members"""
	sorted_population = sorted(population)
	to_retain_by_sex = to_retain // 2 #floor division ensures result is whole number 
	members_per_sex = len(sorted_population) // 2
	
	females = sorted_population[:members_per_sex]
	males = sorted_population[members_per_sex:]
	
	selected_females = females[-to_retain_by_sex:]
	selected_males = males[-to_retain_by_sex:]
	
	return selected_males, selected_females

def breed(males, females, litter_size):
	"""Crossover genes among members (weights) of population"""
	random.shuffle(males)
	random.shuffle(females)
	children = []
	for male, female in zip(males, females):
		for child in range(litter_size):
			child = random.randint(female, male)
			children.append(child)
	return children
	
def mutate(children, mutate_odds, mutate_min, mutate_max):
	"""Randomly alter rat weights using input odds & fractional changes"""
	for index, rat in enumerate(children):
		if mutate_odds >= random.random():
			children[index] = round(rat * random.uniform(mutate_min, mutate_max))
	return children
	
def main():
	"""Initialize population, select, breed, mutate, and display results"""
	generations = 0
	parents = populate(NUM_RATS, INI_MIN_WT, INI_MAX_WT, INI_MODE_WT)
	print("Initial population weights: {}".format(parents))
	popl_fitness = fitness(parents, GOAL)
	print("Initial population fitness: {}".format(popl_fitness))
	print("Number to retain: {}".format(NUM_RATS))
	
	ave_wt = []#average weight
	
	while popl_fitness < 1 and generations < GENERATION_LIMIT:
		selected_males, selected_females = select(parents, NUM_RATS)
		children = breed(selected_males, selected_females, LITTER_SIZE)
		children = mutate(children, MUTATE_ODDS, MUTATE_MIN, MUTATE_MAX)
		parents = selected_males + selected_females + children
		popl_fitness = fitness(parents, GOAL)
		print("Generation {} fitness: {:.4f}".format(generations, popl_fitness))
		ave_wt.append(int(statistics.mean(parents)))
		generations += 1
	print("Average weight per generation: {}".format(ave_wt))
	print("\nNo. of generations: {}".format(generations))
	print("No. of years: {}".format(int(generations / LITTERS_PER_YEAR)))
	
if __name__ == "__main__":
	start_time = time.time()
	main()
	end_time = time.time()
	duration = end_time - start_time
	print("\nRuntime for this program was {} seconds".format(duration))
	
