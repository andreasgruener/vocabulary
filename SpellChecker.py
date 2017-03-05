#!/usr/local/bin/python3

import enchant
from enchant.tokenize import get_tokenizer
import sys
import getopt
from FileHandler import *

LANGUAGE="en_GB"

class color:
	PURPLE = '\033[95m'
	CYAN = '\033[96m'
	BLACK = '\033[0;30m'
	WHITE = '\033[0;37m'
	DARKCYAN = '\033[36m'
	BLUE = '\033[94m'
	LIGHTBLUE = '\033[34m'
	GREEN = '\033[92m'
	YELLOW = '\033[93m'
	RED = '\033[91m'
	BOLD = '\033[1m'
	UNDERLINE = '\033[4m'
	END = '\033[0m'

def checkFile(fileName):
	dictonary = enchant.Dict(LANGUAGE)
	vocabulary = readFile(fileName)

	lineCnt = 1
	errorCnt = 0
	for line in vocabulary:
		#print(questions)
		allgood = True
		errorLine = { "line" : lineCnt, "question" : line['en'], "words" : []}
		lineCnt=lineCnt+1
		for question in line['en']:
			tknzr = get_tokenizer(LANGUAGE)
			#tknzr(question)
			#words = question.split(" ")
			for (word,pos) in tknzr(question):
				if dictonary.check(word) != True:
					allgood = False
					errorCnt=errorCnt+1
					errorLine["words"].append(word)
					#print(word)
					#print("\t--> " + color.RED + question +color.END,flush=True)
					print("%i : %s in (%s)"%(errorLine["line"], word, errorLine["question"]))
		#if allgood != True:
		#	print("%i : %s in (%s)"%(errorLine["line"], errorLine["words"], errorLine["question"]))
			#print(errorLine)
			#line = errorLine["line"]
			#print("%i :"%(line))
	#print(color.RED)
	#print("%i Fehler gefunden"%(lineCnt))
	print(color.RED +  "--> " + str(errorCnt) + " Rechtschreibfehler in der Vokabeldatei gefunden!" + color.END,flush=True)
	return len(errorLine)


def parseParamter(argv):
	global voice
	global readQuestion
	global questionType
	global numberOfQuestions
	inputfile = ''
	count = 20
	try:
	  opts, args = getopt.getopt(argv,"i:",["inputFile="])
	except getopt.GetoptError:
		usage()
		sys.exit(2)
	for opt, arg in opts:
		if opt in ("-i", "--inputFile"):
			inputfile = arg
		

	if inputfile == '':
		print()
		print("You need to provide a input file with the vocabulary.")
		usage()
		sys.exit(3)
	return inputfile

def usage():
	print('Usage: ./vocabulary.py -i <inputfile>')
	print('	-i <inputfile> :: name of the file containing the vocabulary')
	print()
	print('Example:')
	print('	./SpellChecker.py -i voc.csv -v')

def main(argv):
	#print("argv: " + argv[0])
	fileName = parseParamter(argv)
	checkFile(fileName)

if __name__ == "__main__":
   main(sys.argv[1:])
