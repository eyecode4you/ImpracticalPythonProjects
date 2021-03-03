"""	Random Name Generator
	Takes in Firstnames & Lastnames from .txt files & generates 10
	random names per iteration
	EyeCode4You - Do what you like with this file!"""
import random #Used to get random samples from name sets

def main():
	print("This program will generate silly random names:\n")
	
	firstName = set()
	with open("1stnames.txt", "r") as f:
		names = f.read().split()
		for i in names:
			firstName.add(i)
	
	lastName = set()
	with open("2ndnames.txt", "r") as f:
		names = f.read().split()
		for i in names:
			lastName.add(i)
	
	while True:
		for x in range(10): #Gen 10 names
			nameOne = str(random.sample(firstName, k=1)).strip('[\']')
			nameTwo = str(random.sample(lastName, k=1)).strip('[\']')
			print(f"{nameOne} {nameTwo}")
		
		mo = input("\nMOAR? (Press enter to continue or n to quit.)\n")
		if mo.lower() == 'n':
			break	
	return 0

if __name__ == '__main__':
	main()
