"""	Random Name Generator
	Takes in names from txt files & generates random names per iteration
	EyeCode4You - Do what you like with this file!"""
from random import sample
def main():
	print("This program will generate silly random names:\n")
	firstName = set()
	lastName = set()
	with open('names.txt', 'r') as f:
		#first & last names in txt file are sep by INTERMISSION
		names = f.read().split("INTERMISSION")
		for i in names[0].split():
			firstName.add(i)
		for i in names[1].split():
			lastName.add(i)
	while True:
		for x in range(10): #Gen 10 names
			nameOne = str(sample(firstName, k=1)).strip('[\']')
			nameTwo = str(sample(lastName, k=1)).strip('[\']')
			print(f"{nameOne} {nameTwo}")
		mo = input("\nMOAR? (Press enter to continue or n to quit.)\n")
		if mo.lower() == 'n':
			break	
	return 0
if __name__ == '__main__':
	main()
