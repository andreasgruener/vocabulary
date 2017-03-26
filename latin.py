#!/usr/local/bin/python3

import random
import sys
import getopt
import os
import datetime
import time
from Config import Color, QUESTION_TEXT, ANSWER_LANGUAGE_4_QUESTION
from FileHandler import read_file, write_problem_file, write_tracker_file
from FileHandler import load_tracker_file, read_problem_file, upsert_problem, remove_problem
import operator
#from SpellChecker import checkFile

richtig = 0
falsch = 0
voice = False
alleVarianten = False
ignoreProblems = True
percentageOfProblemVokabel = 0.1
questionType = "translation"
readQuestion = False
numberOfQuestions = 100
currentProblemVocabulary = []

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


def result(language, isKorrekt, answer, correctAnswer, question, problems):

	#set default value if no language is provided
	voiceSelector = "-v Daniel "
	korrektText = " correct"


	if language == "translation":
		voiceSelector = "-v Anna "
		korrektText = " richtig"

	text2Say = "say " + voiceSelector + korrektText

	global richtig
	global falsch

	if isKorrekt:
		richtig = richtig + 1
		problems = remove_problem(language, problems, question)
	else:
		text2Say = "say " + voiceSelector + str(correctAnswer)
		falsch = falsch + 1

		# display problem info
		print(Color.LIGHTBLUE + "	Richtig wäre gewesen: ",end="",flush=True)
		for ca in correctAnswer:
			print(Color.RED + ca +Color.END,end="",flush=True)
			if ca != correctAnswer[len(correctAnswer)-1]:
				print(" oder ",end="",flush=True)
			else:
				print(".")
	
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

	# default is latin (other way round not useful)
	# there is alway one single latin word
	qLanguage = "translation"
	problemCount = { 'translation' : len(problems['translation']), 'source' : len(problems['source'])}


	for question in vocabulary:
		wrongAnswer = False
		count = count + 1
		#print("question:")
		#print(question)

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
			q = question[qLanguage][0]
			answerSize = len(question["source"])
			a = question["source"] # is an array



		#print("Frage >> " + str(question[qLanguage]))
		#print("Übersetzung für " + Color.BOLD + q + Color.END + "  : ", end="",flush=True)
		#print("Anzahl Antworten " + str(answerSize))
		sayQuestion(qLanguage, q)

		# ask all variants if enable via parameter
		loop = 1
		if alleVarianten:
			#print("ALLE VARAINTS" + str(answerSize))
			loop = answerSize

		variantDuplicateDetection = []
		print(Color.BOLD + q + Color.END)
		# first ask genetiv genus
		if "genetiv" in question:
			frageText = " " + str(count) + ". Genetiv für " + Color.BOLD + q + Color.END + " : "
			eingabe = input(frageText)
			if eingabe == question['genetiv']:
				result(qLanguage, True, eingabe, [question['genetiv']],q, problems)
			else:
				result(qLanguage, False, eingabe, [question['genetiv']],q, problems)
				#currentProblemVocabulary.append(question)
				wrongAnswer = True

		# second ask genus 
		if "genus" in question:
			frageText = " " + str(count) + ". Genus für " + Color.BOLD + q + Color.END + " : "
			eingabe = input(frageText)
			if eingabe == question['genus']:
				result(qLanguage, True, eingabe, [question['genus']],q, problems)
			else:
				result(qLanguage, False, eingabe, [question['genus']],q, problems)
				#currentProblemVocabulary.append(question)
				wrongAnswer = True


		# loop over variants - answer (a) contains all variants
		for variantQuestionCounter in range(0,loop):

			#eingabe = sys.stdin.readline().strip("\r\n")
			if variantQuestionCounter > 0:
				frageText = "	weitere Übersetzung für " + Color.BOLD + q + Color.END + "  : "
			else:
				frageText = " " + str(count) + ". Übersetzung für " + Color.BOLD + q + Color.END + " (" + str(answerSize) +") : "
				#frageText = "Übersetzung für " + Color.BOLD + q + Color.END + "  : "
			
			eingabe = input(frageText)
			
			# endlos schleife bis neue Vokabel
			while eingabe in variantDuplicateDetection:
				print(Color.RED + "		netter Versuch ... hast du schonmal eingegeben."+ Color.END)
				eingabe = input(frageText)


			variantDuplicateDetection.append(eingabe)
			#print ( eingabe + " == " + a )
			if eingabe in a:
				result(qLanguage, True, eingabe, a,q, problems)
			else:
				result(qLanguage, False, eingabe, a,q, problems)
				wrongAnswer = True
				

			

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

		if wrongAnswer:
			currentProblemVocabulary.append(question)
		
		if count >= numberOfQuestions:
				print("\nAnzahl der Fragen erreicht.")
				break

	return problems

def usage():
	print('Usage: ./vocabulary.py -i <inputfile> [-v] [-e] [-d] [-m] [-r] [-c n] [-h]')
	print('	-i <inputfile> :: name of the file containing the vocabulary')
	print('	-v             :: voice based results (say correct answer)')
	print('	-n             :: no problem vocabulary')
	print('	-h             :: prints this help message')
	print('	-c <Anzahl>    :: number of words to ask')
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
		elif opt in ("-n", "--noProblemVocabulary"):
			ignoreProblems = True
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


	
	if ( note <= 1.5 ):
		print(Color.GREEN + "  _________                              _____          __               ._."+ Color.END)
		print(Color.GREEN + " /   _____/__ ________   ___________    /  _  \   _____/  |_  ____   ____| |"+ Color.END)
		print(Color.GREEN + " \_____  \|  |  \____ \_/ __ \_  __ \  /  /_\  \ /    \   __\/  _ \ /    \ |"+ Color.END)
		print(Color.GREEN + " /        \  |  /  |_> >  ___/|  | \/ /    |    \   |  \  | (  <_> )   |  \|"+ Color.END)
		print(Color.GREEN + "/_______  /____/|   __/ \___  >__|    \____|__  /___|  /__|  \____/|___|  /_"+ Color.END)
		print(Color.GREEN + "        \/      |__|        \/                \/     \/                 \/\/"+ Color.END)
	elif ( note <= 2 ):
		print(Color.GREEN +"  ________        __       _____          __               ._."+ Color.END)
		print(Color.GREEN + " /  _____/ __ ___/  |_    /  _  \   _____/  |_  ____   ____| |"+ Color.END)
		print(Color.GREEN + "/   \  ___|  |  \   __\  /  /_\  \ /    \   __\/  _ \ /    \ |"+ Color.END)
		print(Color.GREEN + "\    \_\  \  |  /|  |   /    |    \   |  \  | (  <_> )   |  \|"+ Color.END)
		print(Color.GREEN + " \______  /____/ |__|   \____|__  /___|  /__|  \____/|___|  /_"+ Color.END)
		print(Color.GREEN + "        \/                      \/     \/                 \/\/"+ Color.END)
	elif ( note <= 3 ):
		print(Color.YELLOW +"__________.__         ._____.         .___                   ._."+ Color.END)
		print(Color.YELLOW +"\______   \  |   ____ |__\_ |__     __| _/___________    ____| |"+ Color.END)
		print(Color.YELLOW +" |    |  _/  | _/ __ \|  || __ \   / __ |\_  __ \__  \  /    \ |"+ Color.END)
		print(Color.YELLOW +" |    |   \  |_\  ___/|  || \_\ \ / /_/ | |  | \// __ \|   |  \|"+ Color.END)
		print(Color.YELLOW +" |______  /____/\___  >__||___  / \____ | |__|  (____  /___|  /_"+ Color.END)
		print(Color.YELLOW +"        \/          \/        \/       \/            \/     \/\/"+ Color.END)
	elif ( note > 3 ):
		print(Color.RED +" __      __       .__  __                                       .__                 ._."+ Color.END)
		print(Color.RED +"/  \    /  \ ____ |__|/  |_  ___________    _____ _____    ____ |  |__   ____   ____| |"+ Color.END)
		print(Color.RED +"\   \/\/   // __ \|  \   __\/ __ \_  __ \  /     \\__  \ _/ ___\|  |  \_/ __ \ /    \ |"+ Color.END)
		print(Color.RED +" \        /\  ___/|  ||  | \  ___/|  | \/ |  Y Y  \/ __ \\  \___|   Y  \  ___/|   |  \|"+ Color.END)
		print(Color.RED +"  \__/\  /  \___  >__||__|  \___  >__|    |__|_|  (____  /\___  >___|  /\___  >___|  /_"+ Color.END)
		print(Color.RED +"       \/       \/              \/              \/     \/     \/     \/     \/     \/\/"+ Color.END)


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
print(Color.BG_BLUE + Color.WHITE)
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
print(Color.BLACK + Color.BG_WHITE + "" + Color.END)

if __name__ == "__main__":
   main(sys.argv[1:])
   #testRuns()

#TODO
# - Parameter -d : deutsche Wörter fragen
# - Parameter -e : englische Wörter fragen
# - Parameter -m : mixed (deutsch / english)
# - Schulnoten geben
#		- a googlen wie die Regeln für die Schulnoten bei Vokabeltest sind
#		- regeln implementieren
# - kleine Ninjas reinmachen (Cole) - Idee von Papa Unicode Zeichen suchen
# - Fortschritt / Highscore speichern (Gamification)


