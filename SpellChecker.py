#!/usr/local/bin/python3
# -*- coding: utf-8 -*-
"""Spellchecker for Vocabulary
reads and writes files
"""


import getopt
import sys
import enchant
from enchant.tokenize import get_tokenizer
from Config import Color

from FileHandler import read_file

# use british english
LANGUAGE = "en_GB"


def check_file(fileName):
	dictonary = enchant.Dict(LANGUAGE)
	vocabulary = read_file(fileName)

	line_counter = 1
	error_counter = 0
	for line in vocabulary:
		#print(questions)
		#all_is_good = True
		error_line = {"line" : line_counter, "question" : line['translation'], "words" : []}
		line_counter = line_counter+1
		for question in line['translation']:
			tknzr = get_tokenizer(LANGUAGE)
			#tknzr(question)
			#words = question.split(" ")
			for (word, pos) in tknzr(question):
				if dictonary.check(word) != True:
					#all_is_good = False
					error_counter = error_counter+1
					error_line["words"].append(word)
					#print(word)
					#print("\t--> " + color.RED + question +color.END,flush=True)
					print("%i : %s in (%s)"%(error_line["line"], word, error_line["question"]))
		#if allgood != True:
		#	print("%i : %s in (%s)"%(errorLine["line"], errorLine["words"], errorLine["question"]))
			#print(errorLine)
			#line = errorLine["line"]
			#print("%i :"%(line))
	#print(color.RED)
	#print("%i Fehler gefunden"%(lineCnt))
	print(Color.RED +  "--> " + str(error_counter) +
							" Rechtschreibfehler in der Vokabeldatei gefunden!" + Color.END, flush=True)
	return len(error_line)


def parse_paramter(argv):
	""" parse parameters from command line using getotps
	"""
	inputfile = ''
	try:
		opts, args = getopt.getopt(argv, "i:", ["inputFile="])
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
	fileName = parse_paramter(argv)
	check_file(fileName)

if __name__ == "__main__":
   main(sys.argv[1:])
