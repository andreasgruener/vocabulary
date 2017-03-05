#!/usr/local/bin/python3

import random
import sys
import getopt
import os
import datetime
import time
from FileHandler import read_file, write_vocabulary_test
import operator
#from SpellChecker import checkFile

width = 68
count = 12

GENUS = ["m.", "f.", "n."]
KASUS = ["Akk.", "Gen."]

SINGPL = ["Sg.",  "Pl."]
PERSON = ["1. Pers",  "2. Pers", "3. Pers"]


# keeps track of vocabulyry asked
tracker = {}




def printTest(path, file, vocabulary, count):
	uniqueName = str(datetime.datetime.now())
	uniqueName = time.strftime("%Y-%m-%d_%H-%M")
	fullName = path + "/" + file
	printDocument = ""

	printDocument = printDocument + printHeader(fullName, uniqueName)	
	testedVocabulary = []

	vocabularySize = len(vocabulary)
	for i in range(0,count):
		#print(" ")
		#print("########")
		#print(testedVocabulary)
		randomKey = random.randint(0, vocabularySize-1)
		#print(randomKey)
		v = vocabulary[randomKey]
		#	print(v)
		#print(v)
		cnt = 0
		while v in testedVocabulary:
			cnt = cnt + 1 
			randomKey = random.randint(0, vocabularySize-1)
			v = vocabulary[randomKey]
			#	print(v)
			if ( cnt > 10):
				break


		foreign = v['en'][0]
		testedVocabulary.append(v)
		
		if len(v) > 2 and v['type'] == 'S':
			printDocument = printDocument + printNoun(foreign)

		elif len(v) > 2 and  v['type'] == 'V':
			printDocument = printDocument + printVerb(foreign)
		elif len(v) > 2 and  v['type'] == 'A':
			printDocument = printDocument + printAdjektiv(foreign)
		else:
			printDocument = printDocument + printDefault(foreign)

	printDocument = printDocument + printFooter()
	print(printDocument)
	write_vocabulary_test(path+"/Vokabeltest"+uniqueName + ".txt",printDocument)

def printHeader(fileName, uniqueName):
	global width
	buffer = ""
	buffer = appendLine(buffer, addText("", "=", width))
	buffer = appendLine(buffer, " Vokabeldatei : " + fileName)
	buffer = appendLine(buffer, " Erzeugt am   : " + uniqueName)
	buffer = appendLine(buffer, addText("", "=", width))
	return buffer

def printFooter():
	global width
	buffer = ""
	buffer = appendLine(buffer, addText("", "-", width))
	buffer = buffer + " Viel Erfolg!"
	
	return buffer

def printDefault(foreign):
	return printGeneric(foreign,"")

def printNoun(foreign):
	fall = KASUS[random.randint(0, len(KASUS)-1)]
	s = SINGPL[random.randint(0, len(SINGPL)-1)]
	return printGeneric(foreign ,"  "  + fall+ " " + s)


def printAdjektiv(foreign):
	genus = GENUS[random.randint(0, 1)]
	fall = KASUS[random.randint(0, len(KASUS)-1)]
	s = SINGPL[random.randint(0, len(SINGPL)-1)]
	return printGeneric(foreign ,"  " + genus + " " + fall+ " " + s)


def printVerb(foreign):
	person = PERSON[random.randint(0, len(PERSON)-1)]
	s = SINGPL[random.randint(0, len(SINGPL)-1)]
	return printGeneric(foreign, "  " + person + " " + s )


def printGeneric(question, zusatz):
	global width
	posOfColon = 30

	question = question + " : "
	spaces = posOfColon - len(question)
	spacesZusatz = posOfColon - len(zusatz)
	
	buffer = ""
	buffer = appendLine(buffer, addText("", "-", width))
	buffer = appendLine(buffer, addText("", " ", posOfColon) + " | ")
	buffer = appendLine(buffer, addText(question, " ", spaces) + " | ")
	buffer = appendLine(buffer, addText(zusatz, " ", spacesZusatz) + " | ")
	return buffer

# def printGeneric(question):
# 	global width
# 	posOfColon = 30

# 	question = question + " : "
# 	length = len(question)
# 	spaces = posOfColon - length
	
# 	buffer = ""
# 	buffer = appendLine(buffer, addText("", "-", width))
# 	buffer = appendLine(buffer, addText("", " ", posOfColon) + " | ")
# 	buffer = appendLine(buffer, addText(question, " ", spaces) + " | ")
# 	buffer = appendLine(buffer, addText("", " ", posOfColon) + " | ")
# 	return buffer



def addText(orig, character, count):
	spacedText = orig
	for sp in range(0,count):
		spacedText = spacedText + character
	return spacedText

def appendLine(buffer, text):
	return buffer + text + "\n"

def usage():
	print('Usage: ./generateLatinTest.py -i <inputfile> [-c n] [-h]')
	print('	-i <inputfile> :: name of the file containing the vocabulary')
	print('	-h             :: prints this help message')

	print('	-c <Anzahl>    :: number of words to ask')
	print()
	print('Example:')
	print('	./generateLatinTest.py -i voc.csv -v')



def parseParamter(argv):
	global voice
	global ignoreProblems
	global alleVarianten
	global readQuestion
	global questionType
	global numberOfQuestions
	inputfile = ''
	global count
	try:
	  opts, args = getopt.getopt(argv,"hvdanrmfc:i:",["help","voice","deutsch","alle", "noProblemVocabulary","read","mixed","foreign","count=","inputFile="])
	except getopt.GetoptError:
		usage()
		sys.exit(2)
	for opt, arg in opts:
		if opt == '-h':
			usage()
			sys.exit()
		elif opt in ("-i", "--inputFile"):
			inputfile = arg
		elif opt in ("-c", "--count"):
			count = arg
		

	if inputfile == '':
		print()
		print("You need to provide a input file with the vocabulary.")
		usage()
		sys.exit(3)
	# set number of questions
	numberOfQuestions = int(count)
	print("Es werden " + str(numberOfQuestions) + " Vokabeln abgefragt.")
	# print("Vocabulary file loading ", inputfile)
	# print("Output file is  " + outputfile)
	return inputfile



def main(argv):
	
	global tracker
	#print("argv: " + argv[0])
	fileName = parseParamter(argv)
	path = path, folder = os.path.split(fileName)
	file = os.path.basename(fileName)
	print(path)

	vocabulary = read_file(fileName)
	random.shuffle(vocabulary)

	printTest(path,file, vocabulary, int(count))	


if __name__ == "__main__":
	main(sys.argv[1:])


