import os
import ast
from Config import *
import operator

def readFile( name ):

	vocabulary = []
	f = open( name, 'r' )
	rows = f.readlines()

	for row in rows:
		try:
			translation = row.split(";")

			enTranslations = translation[0].strip().split(":")

			deTranslations = translation[1].strip().split(":")

			# check for vocabulary type
			if len(translation) > 2:
				vocabularyType = translation[2].strip()
				dict = { 'en' : enTranslations, 'de' : deTranslations, "type" : vocabularyType }
			else:
				dict = { 'en' : enTranslations, 'de' : deTranslations }

			#print(dict)
			vocabulary.append(dict)
		except IndexError:
		 	print("Fehler in der Vokabeldatei in folgendem Eintrag, bitte korrigieren:")
		 	print(" >>>> " +  row)

	return vocabulary

def removeProblem(language, pv, question):
	problemList = pv[language]
	#print(pv)
	for p in problemList:
	#	print("%s == %s : %d"%(p['question'] ,question, p['count']))
		if p['question'] == question:
			p['count'] = p['count'] - 1
			#print(p)
			problemList.remove(p)
			if p['count'] > 0: # in case count is not good enough add again
				problemList.append(p)
			pv[language]=problemList
			return pv
	return pv



def upsertProblem(language, pv, problem):
	problemList = pv[language]
	#print(pv)
	for p in problemList:
		#print(p)
		#print("%s == %s : %d"%(p['question'] ,problem['question'], p['count']))
		if p['question'] == problem['question']:
			problem['count'] = p['count'] + 1
			#print(p)
			problemList.remove(p)
			problemList.append(problem)
			pv[language]=problemList
			return pv
	
	problemList.append(problem)
	return pv

#
# default name of problem file (hide with .)
#
def getProblemFileName ( path, name ):
	return path + "/." + name + "_problemVocabularyFile"

def readProblemFile( path, name ):
	
	pvFull = { 'en' : [], 'de' : [] } 
	if os.path.isfile(getProblemFileName(path, name)) == False:
		print("No Problem File exists.")
		return pvFull
	# read existing file	
	f = open( getProblemFileName(path, name), 'r' )
	rows = f.readlines()

	for row in rows:
		problemRow = row.split(";")

		language = problemRow[0].strip()
		question = problemRow[1].strip()
		correctAnswer =  ast.literal_eval(problemRow[2].strip())
		answer = problemRow[3].strip()
		count = int(problemRow[4].strip())

		#print("%s %s %s - %s - %d"% (language, question, correctAnswer, answer, count))

		problem = { 'language' : language, 'question' :  question, 'correctAnswer' : correctAnswer, 'answer' :  answer, 'count' : count }

		#print("	Checking " + language + " / " + question + " count: " + str(count))

		#print("	- >" + pvFull[languageKey] +"<")
		
		problemList = pvFull[language]
		# print("	- >" + problemList[wordKey]  +"<") 
		# first check if the languag exists
		#if problemList[wordKey] = "":
		problemList.append(problem)

		#print(problem)
		problemVocabulary.append(problem)

	print("In der Abfrage werden %i Problemvokabel berücksichtigt." % (len(problemVocabulary)))
	return pvFull


def writeProblemFile( path, name, pv ):
	# write problem file 
	with open(getProblemFileName(path, name), "w") as problemFile:
		for language in supportedLanguages:
			for problem in pv[language]:
				problemFile.write(problem['language'] + ";" + problem['question'] + ";" + str(problem['correctAnswer']) + ";" + problem['answer'] + ";" + str(problem['count'])+ "\n")

	print("Problemdatei ergänzt: " + getProblemFileName(path, name))

#
# default name of tracker file (hide with .)
#
def getTrackerFileName ( path, name ):
	return path + "/." + name + "_tracker"



def writeTrackerFile( path, name, tracker):
	
	#tracker_sorted = sorted(tracker.items(), key=operator.itemgetter(1), reverse=False)	
	with open(getTrackerFileName(path, name), "w") as problemFile:
		#pickle.dump(tracker, problemFile)
		problemFile.write(str(tracker))

		print("Trackerdatei ergänzt: " + getProblemFileName(path, name))



def loadTrackerFile( path,name ):
	tracker = { } 
	if os.path.isfile(getTrackerFileName(path, name)) == False:
		print("No Tracker File exists.")
		return tracker
	# read existing file	
	try:
		trackerString = open( getTrackerFileName(path, name), 'r' ).read()
		tracker = eval(trackerString)
		#print(tracker)
	except:
		print("Could not read tracker file")
	return tracker




def writeVocabularyTest( fileName, buffer):
	# write problem file 
	with open(fileName, "w") as vocTestFile:
		vocTestFile.write(buffer)

	print("Testdatei erzeugt: " + fileName)



