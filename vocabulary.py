#!/usr/local/bin/python3

import random
import sys
import getopt
import os
import datetime
import time
from Config import *
from FileHandler import *
import operator
#from SpellChecker import checkFile

richtig=0
falsch = 0
voice = False
alleVarianten = False 
ignoreProblems = False
percentageOfProblemVokabel = 0.1
questionType = "mixed"
readQuestion = False
numberOfQuestions = 100
currentProblemVocabulary = []

# keeps track of vocabulyry asked
tracker = {}


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

	BG_BLUE = '\033[44m'
	BG_WHITE = "\033[47m"


def sayQuestion (language, word):
	#set default value if no language is provided
	if readQuestion:
		voiceSelector = "-v Anna "
		if language == "de":
			voiceSelector = "-v Daniel "
		text2Say="say " + voiceSelector + word

		os.system(text2Say) 	


def result( language, isKorrekt, answer, correctAnswer, question, problems ):

	#set default value if no language is provided
	voiceSelector = "-v Daniel "
	korrektText =" correct"


	if language == "en":
		voiceSelector = "-v Anna "
		korrektText = " richtig"
	
	text2Say="say " + voiceSelector + korrektText

	global richtig
	global falsch

	if isKorrekt:
		richtig = richtig + 1
		problems = removeProblem(language, problems ,question)
	else:
		text2Say="say " + voiceSelector + str(correctAnswer)
		falsch = falsch + 1

		# display problem info
		print(color.LIGHTBLUE + "	Richtig wäre gewesen: ",end="",flush=True)
		for ca in correctAnswer:
			print(color.RED + ca +color.END,end="",flush=True)
			if ca != correctAnswer[len(correctAnswer)-1]:
				print(" oder ",end="",flush=True)
			else:
				print(".")
	
		#print("\n")
		problem = { 'language' : language, 'question' :  question, 'correctAnswer' : correctAnswer, 'answer' :  answer, 'count' : 0 }
	
		# TOD CHANGE to HashMap approach
		problems = upsertProblem(language, problems ,problem)
	#print(text2Say)



	if voice and not(isKorrekt):
		os.system(text2Say) 
	return problems


def sortByTracker (voc):
	
	for entry in voc:
	
		if entry["en"][0] in tracker:
			entry["count"] = tracker[entry["en"][0]]
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

	print("================================ "+ questionMessage[type] + " ====================================")
	#print(vocabulary)
	count = 0
	global percentageOfProblemVokabel

	# default is english
	qLanguage = "en"
	problemCount = { 'en' : len(problems['en']), 'de' : len(problems['de'])}


	#print("Problem Count :" + str(problemCount))
	#print(problems)
	print("")
	if type == 'de':
		qLanguage = "de"

	for question in vocabulary:
		count = count + 1

		# randomize langauge each time
		if type == 'mixed':
			if random.choice([True, False]):
				qLanguage = "en"
			else:
				qLanguage = "de"

		# mix problems randomly in questions
		if random.random() < percentageOfProblemVokabel and problemCount[qLanguage] > 1:
			randomKey = random.randint(0, problemCount[qLanguage]-1)
			#print("YEAH %d" %(randomKey))
			#print(problems[qLanguage])
			#print(problems[qLanguage][randomKey])
			print("Problemvokabel:") #" %d" %(randomKey) )
			q = problems[qLanguage][randomKey]['question']
			a = problems[qLanguage][randomKey]['correctAnswer']	
			answerSize = 1
		else:
			# there is exactly one entry in the given array
			questionsVocabularySize = len(question[qLanguage])
			answerSize = len(question[answerLanguage4Question[qLanguage]])
			a = question[answerLanguage4Question[qLanguage]]
			#print(a)
			#print(questionsVocabularySize)
			if questionsVocabularySize == 1:
				q = question[qLanguage][0]
			else:
				randomKey = random.randint(0, questionsVocabularySize-1)
				#print(randomKey)
				q = question[qLanguage][randomKey]

		#print("Übersetzung für " + color.BOLD + q + color.END + "  : ", end="",flush=True)
		#print("Anzahl Antworten " + str(answerSize))
		sayQuestion(qLanguage, q)

		# ask all variants if enable via parameter
		loop = 1
		if alleVarianten:
			#print("ALLE VARAINTS" + str(answerSize))
			loop = answerSize

		variantDuplicateDetection = []		

		# loop over variants - answer (a) contains all variants
		for variantQuestionCounter in range(0,loop):

			#eingabe = sys.stdin.readline().strip("\r\n")
			if variantQuestionCounter > 0:
				frageText = "	weitere Übersetzung für " + color.BOLD + q + color.END + "  : "
			else:
				frageText = str(count) + ". Übersetzung für " + color.BOLD + q + color.END + " (" + str(answerSize) +") : "
				#frageText = "Übersetzung für " + color.BOLD + q + color.END + "  : "
			
			eingabe = input(frageText)
			
			# endlos schleife bis neue Vokabel
			while eingabe in variantDuplicateDetection:
				print(color.RED + "		netter Versuch ... hast du schonmal eingegeben."+ color.END)
				eingabe = input(frageText)


			variantDuplicateDetection.append(eingabe)
			#print ( eingabe + " == " + a )
			if eingabe in a:
				result(qLanguage, True, eingabe, a,q, problems)
			else:
				result(qLanguage, False, eingabe, a,q, problems)
				currentProblemVocabulary.append(question)

			

			#print(question['en'][0])
			keepTrackOf = question['en'][0]
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
				print("\nAnzahl der Fragen erreicht.")
				break

	return problems

def usage():
	print('Usage: ./vocabulary.py -i <inputfile> [-v] [-e] [-d] [-m] [-r] [-c n] [-h]')
	print('	-i <inputfile> :: name of the file containing the vocabulary')
	print('	-v             :: voice based results (say correct answer)')
#	print('	-v             :: voice based question (say question)')
	print('	-n             :: no problem vocabulary')
	print('	-h             :: prints this help message')
	print('	-f             :: asks foreign language words')
	print('	-d             :: asks german words')
	print('	-m             :: asks mixed')
	print('	-c <Anzahl>    :: number of words to ask')
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
	inputfile = ''
	count = 100
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
		elif opt in ("-v", "--voice"):
			voice = True
		elif opt in ("-f", "--foreign"):
			questionType = "en"
		elif opt in ("-d", "--deutsch"):
			questionType = "de"
		elif opt in ("-m", "--mixed"):
			questionType = "mixed"
		elif opt in ("-n", "--noProblemVocabulary"):
			ignoreProblems = True
		elif opt in ("-a", "--alle"):
			alleVarianten = True
		elif opt in ("-r", "--read"):
			readQuestion = True
		elif opt in ("-t", "--test"):
			testRuns()
			sys.exit()

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
	prozent = fehler / gesamt * 100
	schulprozent = prozent * 10 
	faktor = schulprozent // 75
	note = 1 + faktor * 0.5
	if note > 6:
		note = 6

	#print("Gesamt:%d Fehler:%d Prozent:%d Schulprozent:%d faktor:%d Note:%f" % (gesamt, fehler,prozent, schulprozent, faktor,note))
	return note

def main(argv):
	global tracker
	#print("argv: " + argv[0])
	fileName = parseParamter(argv)
	path = path, folder = os.path.split(fileName)
	file = os.path.basename(fileName)
	#print(path)
	#print(file)
	# read the complete problem vocabulary

	tracker = loadTrackerFile(path, file)

	if ( not ignoreProblems ):
		problems = readProblemFile(path, file)
	else:
		problems = { 'en' : [], 'de' : [] } 
	
	vocabulary = readFile(fileName)
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
	print(color.BOLD + "Ergebnis:" + color.END)
	print("============= Ergebnis ================")
	print()
	print(color.BOLD + "	Note 		: %1.1f" % (note) + color.END)
	#print(color.BOLD + "	Note (kor.) 	: %1.1f" % (noteKorr) + color.END)
	print()
	print("---------------------------------------")
	print(			   "	Dauer   : %d Minuten %d Sekunden" % (minuten, sekunden))
	print(			   "	Gesamt  :  " + str(gesamt))
	print(color.BOLD + color.GREEN + "	Richtig :  " + str(richtig) + color.END)
	print(color.BOLD + color.RED + "	Falsch  :  " + str(falsch) + color.END)
	print("=======================================")
#	print("	Dauer  : %2d"  + str(minuten) + " : " + str(sekunden))
	print()

	#print(problemVocabulary)
#	for problem in problemVocabulary:
#		print("%s -->  %s (%s)"%(problem['question'], problem['correctAnswer'] ,str(problem['count'])))
	if ( not ignoreProblems ):
		writeProblemFile(path,file, problems)

	# write tracker file
	writeTrackerFile(path, file + "_tracker", tracker)

	# write result to file
	with open(".result.log", "a") as logFile:#
		logFile.write(str(start.date()) + " : " + start.time().strftime("%H:%M:%S") + " : " + end.time().strftime("%H:%M:%S") + " : " + str(note) + " : " + str(duration) + " :" + user + " : " + str(richtig+falsch) + " : " + str(falsch)+ " : " + questionType + " : " + str(fileName) +  "\n")


	
	if ( note <= 1.5 ):
		print(color.GREEN + "  _________                              _____          __               ._."+ color.END)
		print(color.GREEN + " /   _____/__ ________   ___________    /  _  \   _____/  |_  ____   ____| |"+ color.END)
		print(color.GREEN + " \_____  \|  |  \____ \_/ __ \_  __ \  /  /_\  \ /    \   __\/  _ \ /    \ |"+ color.END)
		print(color.GREEN + " /        \  |  /  |_> >  ___/|  | \/ /    |    \   |  \  | (  <_> )   |  \|"+ color.END)
		print(color.GREEN + "/_______  /____/|   __/ \___  >__|    \____|__  /___|  /__|  \____/|___|  /_"+ color.END)
		print(color.GREEN + "        \/      |__|        \/                \/     \/                 \/\/"+ color.END)
	elif ( note <= 2 ):
		print(color.GREEN +"  ________        __       _____          __               ._."+ color.END)
		print(color.GREEN + " /  _____/ __ ___/  |_    /  _  \   _____/  |_  ____   ____| |"+ color.END)
		print(color.GREEN + "/   \  ___|  |  \   __\  /  /_\  \ /    \   __\/  _ \ /    \ |"+ color.END)
		print(color.GREEN + "\    \_\  \  |  /|  |   /    |    \   |  \  | (  <_> )   |  \|"+ color.END)
		print(color.GREEN + " \______  /____/ |__|   \____|__  /___|  /__|  \____/|___|  /_"+ color.END)
		print(color.GREEN + "        \/                      \/     \/                 \/\/"+ color.END)
	elif ( note <= 3 ):
		print(color.YELLOW +"__________.__         ._____.         .___                   ._."+ color.END)
		print(color.YELLOW +"\______   \  |   ____ |__\_ |__     __| _/___________    ____| |"+ color.END)
		print(color.YELLOW +" |    |  _/  | _/ __ \|  || __ \   / __ |\_  __ \__  \  /    \ |"+ color.END)
		print(color.YELLOW +" |    |   \  |_\  ___/|  || \_\ \ / /_/ | |  | \// __ \|   |  \|"+ color.END)
		print(color.YELLOW +" |______  /____/\___  >__||___  / \____ | |__|  (____  /___|  /_"+ color.END)
		print(color.YELLOW +"        \/          \/        \/       \/            \/     \/\/"+ color.END)
	elif ( note > 3 ):
		print(color.RED +" __      __       .__  __                                       .__                 ._."+ color.END)
		print(color.RED +"/  \    /  \ ____ |__|/  |_  ___________    _____ _____    ____ |  |__   ____   ____| |"+ color.END)
		print(color.RED +"\   \/\/   // __ \|  \   __\/ __ \_  __ \  /     \\__  \ _/ ___\|  |  \_/ __ \ /    \ |"+ color.END)
		print(color.RED +" \        /\  ___/|  ||  | \  ___/|  | \/ |  Y Y  \/ __ \\  \___|   Y  \  ___/|   |  \|"+ color.END)
		print(color.RED +"  \__/\  /  \___  >__||__|  \___  >__|    |__|_|  (____  /\___  >___|  /\___  >___|  /_"+ color.END)
		print(color.RED +"       \/       \/              \/              \/     \/     \/     \/     \/     \/\/"+ color.END)


### end of main 

### TEST PART ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### 
def testRuns():
  
    calcSchulnote(20,0)
   # calcSchulnote(20,1)
   # calcSchulnote(20,2)
   # calcSchulnote(20,3)
   # calcSchulnote(20,4)     
   # calcSchulnote(20,11)
   # calcSchulnote(20,15)
### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### 


### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### 

### start main from here
# Hier gehts wirklich los..

### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### 

os.system('clear')
print(color.BG_BLUE + color.WHITE)
print("____   ____     __          ___.          .__   __                .__                     ")
print("\   \ /   /___ |  | _______ \_ |__   ____ |  |_/  |_____________  |__| ____   ___________ ")
print(" \   Y   /  _ \|  |/ /\__  \ | __ \_/ __ \|  |\   __\_  __ \__  \ |  |/    \_/ __ \_  __ \\")
print("  \     (  <_> )    <  / __ \| \_\ \  ___/|  |_|  |  |  | \// __ \|  |   |  \  ___/|  | \/")
print("   \___/ \____/|__|_ \(____  /___  /\___  >____/__|  |__|  (____  /__|___|  /\___  >__| 2.0")
print("                    \/     \/    \/     \/                      \/        \/     \/       ")
# print("  ___.              _____          __                  _______________  ____ .________    ")
# print("  \_ |__ ___.__.   /  _  \   _____/  |_  ____   ____   \_____  \   _  \/_   ||   ____/    ")
# print("   | __ <   |  |  /  /_\  \ /    \   __\/  _ \ /    \   /  ____/  /_\  \|   ||____  \     ")
# print("   | \_\ \___  | /    |    \   |  \  | (  <_> )   |  \ /       \  \_/   \   |/       \\    ")
# print("   |___  / ____| \____|__  /___|  /__|  \____/|___|  / \_______ \_____  /___/______  /    ")
# print("       \/\/              \/     \/                 \/          \/     \/           \/     ")
print("                                                                                          ")
print(color.BLACK + color.BG_WHITE + "" + color.END)

if __name__ == "__main__":
   main(sys.argv[1:])
   #testRuns()

# TODO / IDEAS
# - Parameter -d : deutsche Wörter fragen
# - Parameter -e : englische Wörter fragen
# - Parameter -m : mixed (deutsch / english)
# - Schulnoten geben
#		- a googlen wie die Regeln für die Schulnoten bei Vokabeltest sind
#		- regeln implementieren
# - kleine Ninjas reinmachen (Cole) - Idee von Papa Unicode Zeichen suchen
# - Fortschritt / Highscore speichern (Gamification)


