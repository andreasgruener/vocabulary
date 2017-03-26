#!/usr/local/bin/python3
"""
Test fpr FileHandler
"""
import sys
import os

# start the Test from main source directory like ./test/TestFileHandler.py
sys.path.append(os.path.abspath("."))
from FileHandler import read_file


def main(argv):
	"""
	Main Class
	"""
	print("Starting FileHandler Test with example vocabulary")
	print(argv)
	vocabularyJSON = read_file("example/example-voc.csv")
	print(vocabularyJSON)

# main starter
if __name__ == "__main__":
	main(sys.argv[1:])
    # testRuns()
