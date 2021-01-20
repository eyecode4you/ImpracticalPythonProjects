#Display letters in a sentence represented as a bar chart (Letter Freq.)
import pprint
from collections import defaultdict

def main():
	ALPHABET = 'abcdefghijklmnopqrstuvwxyz'

	usrIn = input("Enter some text:\n")
		
	mapped = defaultdict(list)
	for i in usrIn: #Letters
		i = i.lower()
		if i in ALPHABET:
			mapped[i].append(i) #Construct + Map Key Values
				
	print("\n\nLETTER FREQUENCY:\n^^^^^^^^^^^^^^^^^")
	pprint.pprint(mapped, width=110)
		
if __name__ == '__main__':
	main()
