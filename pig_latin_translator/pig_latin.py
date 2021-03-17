"""	Pig Latin Translator 
	EyeCode4You - Do what you like with this file!
"""
import sys
def main():
	"""This program will take text and translate it to pig latin"""
	VOWELS = 'aeiouy'
	while True:
		text = input("Please enter text to translate: ").split()
		for word in text:
			if word[0] in VOWELS:
				pig_latin = word + 'way'
			else:
				pig_latin = word[1:] + word[0] + 'ay'
			print(f'{pig_latin}', end=' ')
		try_again = input("\nConvert Again? (Enter or n to exit)\n")
		if try_again.lower() == "n":
			sys.exit()
if __name__ == '__main__':
	main()
