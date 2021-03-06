#!/usr/local/bin/python3

import random
import sys
import getopt
import os
import datetime
import time

from vocabulary.Config import Color, QUESTION_TEXT, ANSWER_LANGUAGE_4_QUESTION,NOTIFICATION_SMTP_RCPT,NOTIFICATION_SMTP_SERVER,NOTIFICATION_SMTP_USER,NOTIFICATION_SMTP_PWD,NOTIFICATION_SMTP_FROM
from vocabulary.util.FileHandler import read_file, write_problem_file, write_tracker_file
from vocabulary.util.FileHandler import load_tracker_file, read_problem_file, upsert_problem, remove_problem
import operator
from vocabulary.util.Mail import sendInfoMail
from vocabulary.util.SpellChecker import check_file
from vocabulary.util.Diff import show_diff
from vocabulary.util.MqttClient import publishResult
from vocabulary.util.ASCIIArt import ASCII_VOKABELTRAINER, ASCII_RISING_STAR, ASCII_YOU_ROCK, ASCII_KEEP_WORKING, ASCII_DONT_GIVE_UP

richtig = 0
falsch = 0
voice = False
alleVarianten = False
ignoreProblems = False
detectDuplicates = True
percentageOfProblemVokabel = 0.1
questionType = "mixed"
readQuestion = False
numberOfQuestions = 100
currentProblemVocabulary = []
richtigeVokabeln = []
falscheVokabeln = []


# keeps track of vocabulyry asked
tracker = {}


# probably mac only
def sayQuestion(language, word):
	#set default value if no language is provided
	if readQuestion:
		voiceSelector = "-v Anna "
		if language == "source":
			voiceSelector = "-v Daniel "
		text2Say = "say " + voiceSelector + word

		os.system(text2Say)

def say(language, word):
	#set default value if no language is provided
	voiceSelector = "-v Anna "
	if language == "english":
		voiceSelector = "-v Daniel "
	text2Say = "say " + voiceSelector + word

	os.system(text2Say)


def result(language, isKorrekt, answer, correctAnswer, question, problems, frageText):

	#set default value if no language is provided
	voiceSelector = "-v Daniel "
	korrektText = " correct"

	asked = { 'language' : language, 'question' :  question, 'correctAnswer' : correctAnswer, 'answer' :  answer }
	

	if language == "translation":
		voiceSelector = "-v Anna "
		korrektText = " richtig"

	text2Say = "say " + voiceSelector + korrektText

	global richtig
	global falsch

	if isKorrekt:
		richtig = richtig + 1
		problems = remove_problem(language, problems, question)
		richtigeVokabeln.append(asked)
	else:
		text2Say = "say " + voiceSelector + str(correctAnswer)
		falsch = falsch + 1
		falscheVokabeln.append(asked)

		length = len(frageText) + len(answer)
		moveString = "\033[{}C\033[1A".format(length) # \033[1C (one Column right) \033[1A (one row up)

		# display problem info
		print(moveString + Color.RED + " --> "+Color.END,end="",flush=True)
		for ca in correctAnswer:
			print(Color.RED + ca +Color.END,end="",flush=True)
			if ca != correctAnswer[len(correctAnswer)-1]:
				print(" oder ",end="",flush=True)

		if len(correctAnswer) == 1:
			diffed_result = show_diff(answer, correctAnswer[0])
			print(Color.DARKCYAN +" Unterschied: >" + Color.END + diffed_result + Color.DARKCYAN +"<" + Color.END,end="",flush=True)

		print("",flush=True)

		#print("\n")
		problem = { 'language' : language, 'question' :  question, 'correctAnswer' : correctAnswer, 'answer' :  answer, 'count' : 0 }
	
		# TOD CHANGE to HashMap approach
		problems = upsert_problem(language, problems ,problem)
	#print(text2Say)



	if voice and not(isKorrekt):
		os.system(text2Say) 
	return problems


def sortByTracker (voc):
	
	for entry in voc:
	
		if entry["translation"][0] in tracker:
			entry["count"] = tracker[entry["translation"][0]]
		else: 
			entry["count"] = 0
			
	voc_sorted = sorted(voc, key=lambda x: x["count"], reverse=False)
	#voc_sorted = sorted(voc.items(), key=operator.itemgetter(1), reverse=False)	
	#print("SORTED")
	#print(voc_sorted)

	return voc_sorted

def runTest( vocabulary , type, problems):

	global alleVarianten
	global numberOfQuestions
	global currentProblemVocabulary

	print("================================ "+ QUESTION_TEXT[type] + " ====================================")
	#print(vocabulary)
	count = 0
	global percentageOfProblemVokabel

	# default is english
	qLanguage = "translation"
	problemCount = { 'translation' : len(problems['translation']), 'source' : len(problems['source'])}


	#print("Problem Count :" + str(problemCount))
	#print(problems)
	print("")
	if type == 'source':
		qLanguage = "source"

	for question in vocabulary:
		count = count + 1
		#print(question)
		# randomize langauge each time
		if type == 'mixed':
			if random.choice([True, False]):
				qLanguage = "translation"
			else:
				qLanguage = "source"

		# mix problems randomly in questions
		if random.random() < percentageOfProblemVokabel and problemCount[qLanguage] > 1:
			randomKey = random.randint(0, problemCount[qLanguage]-1)
			#print("YEAH %d" %(randomKey))
			#print(problems[qLanguage])
			#print(problems[qLanguage][randomKey])
			print("Problemvokabel:") #" %d" %(randomKey) )
			q = problems[qLanguage][randomKey]['question']
			a = problems[qLanguage][randomKey]['correctAnswer']	
			#a_genetiv = problems[qLanguage][randomKey]['genetiv']
			#a_kasus = problems[qLanguage][randomKey]['genetiv']
			answerSize = 1
		else:
			# there is exactly one entry in the given array
			questionsVocabularySize = len(question[qLanguage])
			answerSize = len(question[ANSWER_LANGUAGE_4_QUESTION[qLanguage]])
			a = question[ANSWER_LANGUAGE_4_QUESTION[qLanguage]]
			#a_genetiv = question['genetiv']
			#a_kasus = question['genetiv']
			#print(a)
			#print(str(questionsVocabularySize))
			if questionsVocabularySize == 1:
				q = question[qLanguage][0]
			else:
				randomKey = random.randint(0, questionsVocabularySize-1)
				#print(randomKey)
				q = question[qLanguage][randomKey]

		#print("Frage >> " + str(question[qLanguage]))
		#print("Übersetzung für " + Color.BOLD + q + Color.END + "  : ", end="",flush=True)
		#print("Anzahl Antworten " + str(answerSize))
		sayQuestion(qLanguage, q)

		# ask all variants if enable via parameter
		loop = 1
		if alleVarianten:
			print("ALLE VARAINTS" + str(answerSize))
			loop = answerSize

		variantDuplicateDetection = []

		# loop over variants - answer (a) contains all variants
		for variantQuestionCounter in range(0,loop):

			#eingabe = sys.stdin.readline().strip("\r\n")
			if variantQuestionCounter > 0:
				frageText = "	weitere Übersetzung für " + Color.BOLD + q + Color.END + "  : "
			else:
				frageText = str(count) + ". " + Color.BOLD + q + Color.END + " (" + str(answerSize) +") : "
				#frageText = "Übersetzung für " + Color.BOLD + q + Color.END + "  : "
			
			eingabe = input(frageText)

			# endlos schleife bis neue Vokabel
			if detectDuplicates:
				while eingabe in variantDuplicateDetection :
					print(Color.RED + "		netter Versuch ... hast du schonmal eingegeben."+ Color.END)
					eingabe = input(frageText)


			variantDuplicateDetection.append(eingabe)
			#print ( eingabe + " == " + a )
			if eingabe in a:
				result(qLanguage, True, eingabe, a,q, problems, frageText)
			else:
				result(qLanguage, False, eingabe, a,q, problems, frageText)
				currentProblemVocabulary.append(question)

			

			#print(question['translation'][0])
			keepTrackOf = question['translation'][0]
			if ( keepTrackOf in tracker ):
				cnt = int(tracker[keepTrackOf])
				tracker[keepTrackOf] = cnt + 1
			else:
				tracker[keepTrackOf] = 1
			#print(tracker)
			#print("Anzahl Antworten=" + str(answerSize) + " Schleife=" + str(loop) + "  Aktuelle Frage=" + str(variantQuestionCounter))
			#if loop > variantQuestionCounter+1:
			#		print("   weitere Übersetzung : ")

		if count >= numberOfQuestions:
				print("\nAnzahl der eingestellen Fragen ist erreicht.")
				input(Color.BLUE + " Return / Enter für weiter ..." + Color.END)
				break

	return problems

def usage():
	print('Usage: ./vocabulary.py -i <inputfile> [-v] [-x] [-e] [-d] [-m] [-r] [-c n] [-h]')
	print('	-i <inputfile> :: name of the file containing the vocabulary')
	print('	-v             :: voice based results (say correct answer)')
#	print('	-v             :: voice based question (say question)')
	print('	-n             :: no problem vocabulary')
	print('	-h             :: prints this help message')
	print('	-f             :: asks foreign language words')
	print('	-d             :: asks german words')
	print('	-m             :: asks mixed')
	print(' -e 			   :: sends result-email to given address') # TODO - it's always on right now
	print('	-c <Anzahl>    :: number of words to ask')
	print('	-x    		   :: do not check duplicates')
	print('	-a             :: all variants are asked')
	print()
	print('Example:')
	print('	./vocabulary.py -i voc.csv -v')



def parseParamter(argv):
	global voice
	global ignoreProblems
	global alleVarianten
	global readQuestion
	global questionType
	global numberOfQuestions
	global detectDuplicates
	inputfile = ''
	count = 100
	try:
	  opts, args = getopt.getopt(argv,"hvdaxnrmfc:i:",["help","voice","deutsch","alle", "allow duplicates", "noProblemVocabulary","read","mixed","foreign","count=","inputFile="])
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
		elif opt in ("-v", "--voice"):
			voice = True
		elif opt in ("-f", "--foreign"):
			questionType = "translation"
		elif opt in ("-d", "--deutsch"):
			questionType = "source"
		elif opt in ("-m", "--mixed"):
			questionType = "mixed"
		elif opt in ("-n", "--noProblemVocabulary"):
			ignoreProblems = True
		elif opt in ("-a", "--alle"):
			alleVarianten = True
		elif opt in ("-x", "--allow duplicates"):
			detectDuplicates = False
		elif opt in ("-r", "--read"):
			readQuestion = True
		elif opt in ("-t", "--test"):
			testRuns()
			sys.exit()

	if inputfile == '':
		print()
		print("V2.0.  You need to provide a input file with the vocabulary.")
		usage()
		sys.exit(3)
	# set number of questions
	numberOfQuestions = int(count)
	print("Es werden " + str(numberOfQuestions) + " Vokabeln abgefragt.")
	# print("Vocabulary file loading ", inputfile)
	# print("Output file is  " + outputfile)
	return inputfile


def ask4Korrektur():
	print("Möchtest Du die Anzahl der Fehler senken (bspw. vertippt):")
	eingabe = sys.stdin.readline().strip("\r\n")
	korrekturAnzahl = 0
	try:
		korrekturAnzahl = int(eingabe)
	except ValueError:
		print("not a number")
	return korrekturAnzahl

def calcSchulnoteKorrektur(gesamt, fehler, korrekturAnzahl):
	if gesamt == 0:
		return 0
	fehler = fehler - korrekturAnzahl
	if fehler < 0:
		fehler = 0
	prozent = fehler / gesamt * 100
	schulprozent = prozent * 10 
	faktor = schulprozent // 75
	note = 1 + faktor * 0.5
	if note > 6:
		note = 6

	#print("Gesamt:%d Fehler:%d Prozent:%d Schulprozent:%d faktor:%d Note:%f" % (gesamt, fehler,prozent, schulprozent, faktor,note))
	return note


def calcSchulnote(gesamt, fehler):
	if gesamt == 0:
		return 6
	prozent = fehler / gesamt * 100
	schulprozent = prozent * 10 
	faktor = schulprozent // 75
	note = 1 + faktor * 0.5
	if note > 6:
		note = 6

	#print("Gesamt:%d Fehler:%d Prozent:%d Schulprozent:%d faktor:%d Note:%f" % (gesamt, fehler,prozent, schulprozent, faktor,note))
	return note

def startTest(argv):


#	sendInfoMail("datum", "start", "ende", "6", "1h", "user", "27", "12", "frage_art", "vokabel_datei")
	language = "Englisch"
	global tracker
	#print("argv: " + argv[0])
	fileName = parseParamter(argv)
	path = path, folder = os.path.split(fileName)
	file = os.path.basename(fileName)
	if fileName.startswith("englis"):
		check_file(fileName)
	else:
		language = "Latein"

	#print(path)
	#print(file)
	# read the complete problem vocabulary

	tracker = load_tracker_file(path, file)

	if ( not ignoreProblems ):
		problems = read_problem_file(path, file)
	else:
		problems = { 'translation' : [], 'source' : [] } 
	
	vocabulary = read_file(fileName)
	#print(vocabulary)
	#errors = checkFile(fileName)

	random.shuffle(vocabulary)

	# sorts by tracked questions
	vocabulary = sortByTracker(vocabulary)

	# measure time
	startTime = time.time()
	start = datetime.datetime.now()

	# Vokabelanfrage
	problems = runTest(vocabulary, questionType, problems)
	#print(problems)

	if len(currentProblemVocabulary) > 0 :
		print()
		print(chr(27) + "[2J") # clear screen
		print("---------------------------------------------------------------------")
		print("Die falsch beantworteten " + str(len(currentProblemVocabulary)) + " Vokabeln werden nun nochmals geprüft:")
		print("----------------------------------------------------------------------")
		print()
		problems = runTest(list(currentProblemVocabulary), questionType, problems )
		
	#anzahlKorrektur = ask4Korrektur()
	anzahlKorrektur = 0

	endTime = time.time()
	end = datetime.datetime.now()

#	print (" " + str(endTime) + " - " + str(startTime))
	

	user = os.getlogin()	
	gesamt = richtig+falsch
	duration = round ( ( endTime - startTime) , 0)
	minuten = round ( ( endTime - startTime) / 60  , 0)
	sekunden = round ( ( endTime - startTime) % 60  , 0)
	noteKorr = calcSchulnoteKorrektur(gesamt, falsch, anzahlKorrektur)
	note = calcSchulnote(gesamt, falsch)

	print()
	print(Color.BOLD + "Ergebnis:" + Color.END)
	print("============= Ergebnis ================")
	print()
	print(Color.BOLD + "	Note 		: %1.1f" % (note) + Color.END)
	#print(Color.BOLD + "	Note (kor.) 	: %1.1f" % (noteKorr) + Color.END)
	print()
	print("---------------------------------------")
	print(			   "	Dauer   : %d Minuten %d Sekunden" % (minuten, sekunden))
	print(			   "	Gesamt  :  " + str(gesamt))
	print(Color.BOLD + Color.GREEN + "	Richtig :  " + str(richtig) + Color.END)
	print(Color.BOLD + Color.RED + "	Falsch  :  " + str(falsch) + Color.END)
	print("=======================================")
#	print("	Dauer  : %2d"  + str(minuten) + " : " + str(sekunden))
	print()

	#print(problemVocabulary)
#	for problem in problemVocabulary:
#		print("%s -->  %s (%s)"%(problem['question'], problem['correctAnswer'] ,str(problem['count'])))
	if ( not ignoreProblems ):
		write_problem_file(path,file, problems)

	# write tracker file
	write_tracker_file(path, file + "_tracker", tracker)

	# write result to file
	with open(".result.log", "a") as logFile:#
		logFile.write(str(start.date()) + " : " + start.time().strftime("%H:%M:%S") + " : " + end.time().strftime("%H:%M:%S") + " : " + str(note) + " : " + str(duration) + " :" + user + " : " + str(richtig+falsch) + " : " + str(falsch)+ " : " + questionType + " : " + str(fileName) +  "\n")

	publishResult(user, language,"Vokabeln",questionType, file,  note, duration, gesamt, falsch)
	sendInfoMail(str(start.date()),start.time().strftime("%H:%M:%S"), end.time().strftime("%H:%M:%S"),str(note),str(duration),user ,str(richtig+falsch),str(falsch),questionType,str(fileName), richtigeVokabeln, falscheVokabeln)

	

	if ( note <= 1.5 ):
		say("english", user+" you rock, really")
		print(Color.GREEN + Color.BOLD+ ASCII_YOU_ROCK + Color.END)
	elif ( note <= 2 ):
		say("english", "good work"+ user)
		print(Color.GREEN + ASCII_RISING_STAR + Color.END)
	elif ( note <= 3 ):
		say("english", "keep on working "+ user)
		print(Color.YELLOW +ASCII_KEEP_WORKING+ Color.END)
	elif ( note > 3 ):
		say("english", "there is room for improvement "+ user)
		print(Color.RED +ASCII_DONT_GIVE_UP+ Color.END)

os.system('clear')
print(Color.BG_BLUE + Color.WHITE+ ASCII_VOKABELTRAINER +Color.BLACK + Color.BG_WHITE + "" + Color.END)

if __name__ == "__main__":
	startTest(sys.argv[1:])
