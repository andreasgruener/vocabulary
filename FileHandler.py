# -*- coding: utf-8 -*-
"""Filehandler for Vocabulary
reads and writes files
"""

import os
import ast
from Config import LIST_OF_PROBLEM_VOCABULARY, SUPPORTED_LANGUAGES

def read_file(name):
	"""
	read a file
	; separates the entries TRANSLATION;SOURCE;[TYPE]
	: separates multiple options in TRANSLATION or SOURCE
	, separates word, genetiv, genus (e.g. latin dominus,domini,m)
	"""
	vocabulary = []
	filehandle = open(name, 'r')
	rows = filehandle.readlines()

	for row in rows:
		try:
			translation = row.split(";")

			# parse multiple options in the foreign langauge
			lang_translations = translation[0].strip().split(":")
			# parse multiple options in your language
			lange_source = translation[1].strip().split(":")
		#	print(lange_source)
			if len(lange_source[0]) < 2:
				print("Fehler in Datei: Leere oder zu kurze Vokabel. >" + lange_source[0] +  "< Beende lesen der Datei. Datei korrigieren")
				return []
			initial_dictionary = {'translation' : lang_translations, 'source' : lange_source}

			#check if we have genetiv and genus
			for translation_row in lang_translations:
				#print(translation_row)
				full_stack = translation_row.split(",")
				if len(full_stack) == 2:
					print("Error parsing Genetiv, Genus - missing one entry" + str(translation))
				elif len(full_stack) == 3:
					initial_dictionary["translation"] = [full_stack[0]]
					#print(full_stack[0])
					initial_dictionary["genetiv"] = str(full_stack[1])
					initial_dictionary["genus"] = str(full_stack[2])
				#else:
					#print("no genetiv, genus")

			# check for vocabulary type
			if len(translation) > 2:
				vocabulary_type = translation[2].strip()
				initial_dictionary["type"] = vocabulary_type


			#print(dict)
			vocabulary.append(initial_dictionary)
		except IndexError:
			print("Fehler in der Vokabeldatei in folgendem Eintrag, bitte korrigieren:")
			print(" >>>> " +  row)

	return vocabulary


def remove_problem(language, problem_vocabulary, question):
	"""remove a problem from the problem problem_list
	"""
	problem_list = problem_vocabulary[language]
	#print(pv)
	for problem in problem_list:
	#	print("%s == %s : %d"%(p['question'] ,question, p['count']))
		if problem['question'] == question:
			problem['count'] = problem['count'] - 1
			#print(p)
			problem_list.remove(problem)
			if problem['count'] > 0: # in case count is not good enough add again
				problem_list.append(problem)
			problem_vocabulary[language] = problem_list
			return problem_vocabulary
	return problem_vocabulary



def upsert_problem(language, problem_vocabulary, problem):
	"""upsert a problem into the  problem_list
	"""
	problem_list = problem_vocabulary[language]
	#print(problem_list)
	for problem in problem_list:
		print(problem)

		#print("%s == %s : %d"%(['question'] ,problem['question'], p['count']))
		if problem['question'] == problem['question']:
			problem['count'] = problem['count'] + 1
			#print(problem_list)
			problem_list.remove(problem)
			problem_list.append(problem)
			#print(problem_list)
			problem_vocabulary[language] = problem_list
			return problem_vocabulary

	problem_list.append(problem)
	return problem_vocabulary


def get_problem_filename(path, name):
	"""	 default name of problem file (hide with .)
	"""
	return path + "/." + name + "_problemVocabularyFile"

def read_problem_file(path, name):
	""" read the problem file from disk
	"""
	pv_full = {'translation' : [], 'source' : []}
	if os.path.isfile(get_problem_filename(path, name)) is False:
		print("No Problem File exists.")
		return pv_full
	# read existing file
	problem_filehandle = open(get_problem_filename(path, name), 'r')
	rows = problem_filehandle.readlines()

	for row in rows:
		problem_row = row.split(";")

		language = problem_row[0].strip()
		question = problem_row[1].strip()
		correct_answer = ast.literal_eval(problem_row[2].strip())
		answer = problem_row[3].strip()
		count = int(problem_row[4].strip())

		#print("%s %s %s - %s - %d"% (language, question, correctAnswer, answer, count))

		problem = {'language' : language, 'question' :  question, 'correctAnswer' : correct_answer, 'answer' :  answer, 'count' : count}

		#print("	Checking " + language + " / " + question + " count: " + str(count))

		#print("	- >" + pvFull[languageKey] +"<")
		#print(problem)
		#print(language)
		# legacy stuff
		if language == 'en':
			language = 'translation'
		if language == 'de':
			language = 'source'

		problem_list = pv_full[language]
		# print("	- >" + problemList[wordKey]  +"<")
		# first check if the languag exists
		#if problemList[wordKey] = "":
		problem_list.append(problem)

		#print(problem)
		LIST_OF_PROBLEM_VOCABULARY.append(problem)

	print("In der Abfrage werden %i Problemvokabel berücksichtigt." % (len(LIST_OF_PROBLEM_VOCABULARY)))
	return pv_full


def write_problem_file(path, name, problem_vocabulary):
	""" write problem file
	"""
	with open(get_problem_filename(path, name), "w") as problem_file:
		for language in SUPPORTED_LANGUAGES:
			for problem in problem_vocabulary[language]:
				problem_file.write(problem['language'] + ";" + problem['question'] + ";" + str(problem['correctAnswer']) + ";" + problem['answer'] + ";" + str(problem['count'])+ "\n")

	print("Problemdatei ergänzt: " + get_problem_filename(path, name))

#
# default name of tracker file (hide with .)
#
def get_tracker_filename(path, name):
	"""
	default name for tracker file
	"""
	return path + "/." + name + "_tracker"

def write_tracker_file(path, name, tracker):
	"""save tracker file with new information
	"""
	#tracker_sorted = sorted(tracker.items(), key=operator.itemgetter(1), reverse=False)
	with open(get_tracker_filename(path, name), "w") as problem_file:
		#pickle.dump(tracker, problemFile)
		problem_file.write(str(tracker))

		print("Trackerdatei ergänzt: " + get_problem_filename(path, name))



def load_tracker_file(path, name):
	"""read tracker file from disk
	"""
	tracker = {}
	if os.path.isfile(get_tracker_filename(path, name)) is False:
		print("No Tracker File exists.")
		return tracker
	# read existing file
	try:
		tracker_string = open(get_tracker_filename(path, name), 'r').read()
		tracker = eval(tracker_string)
		#print(tracker)
	except:
		print("Could not read tracker file")
	return tracker




def write_vocabulary_test(file_name, buffer):
	"""generates a vocabulary test as CSV file copy to file editor looks nice ;-)
	"""
	# write problem file
	with open(file_name, "w") as vocabulary_test_filehandle:
		vocabulary_test_filehandle.write(buffer)

	print("Testdatei erzeugt: " + file_name)



