#!/usr/local/bin/python3

import random
import sys
import getopt
import os
from Config import Color
import datetime
import time
from util.FileHandler import readKonjugationen
from util.mail import sendInfoMail
from util.diff import show_diff


def prasens(json):
    return [x for x in json["tempus"] if x['name'] == "Präsens"][0]

def imperfekt(json):
    return [x for x in json["tempus"] if x['name'] == "Imperfekt"][0]

def perfekt(json):
    return [x for x in json["tempus"] if x['name'] == "Perfekt"][0]

def runTest(konjugationen, settingKonjugation):

    # measure time
    startTime = time.time()
    start = datetime.datetime.now()

    # do the test
    try:
        if settingKonjugation == "":
            zufallsIndex = random.randint(0,len(konjugationen)-1)
            konjugation = konjugationen[zufallsIndex]  
        else: # konjugation is given by user
            konjugationen = [x for x in konjugationen if x['name'] == settingKonjugation+"-Konjugation"]
            if len(konjugationen) == 1: # there is exactly one hit ignoring genus
                konjugation = konjugationen[0]
    except IndexError:
        print("")
        print(Color.RED + settingkonjugation + "-konjugation für " + settingGenus + "kann nicht geladen werden" + Color.END)
        sys.exit(3)

    settingKonjugation = konjugation["name"]
    
    #print(konjugation)
    result = checkKonjugation(konjugation)
    richtigListe = result["richtig"]
    fehlerListe = result["falsch"]
    gesamt = result["gesamt"]
    fehler = result["fehler"]
    
    note = calcSchulnote(gesamt, fehler)
    richtig = gesamt - fehler

    # measure time
    endTime = time.time()
    end = datetime.datetime.now()
    user = os.getlogin()	
    duration = round ( ( endTime - startTime) , 0)
    minuten = round ( ( endTime - startTime) / 60  , 0)
    sekunden = round ( ( endTime - startTime) % 60  , 0)
    note = calcSchulnote(gesamt, fehler)
    print()
    print(Color.BOLD + "Ergebnis:" + Color.END)
    print("============= Ergebnis ================")
    print()
    print(Color.BOLD + "	Note 		: %1.1f" % (note) + Color.END)
    #print(Color.BOLD + "	Note (kor.) 	: %1.1f" % (noteKorr) + Color.END)
    print()
    print("---------------------------------------")
    print(			   "	Dauer   :  %d Minuten %d Sekunden" % (minuten, sekunden))
    print(			   "	Gesamt  :  " + str(gesamt))
    print(Color.BOLD + Color.GREEN + "	Richtig :  " + str(richtig) + Color.END)
    print(Color.BOLD + Color.RED + "	Falsch  :  " + str(fehler) + Color.END)
    print("=======================================")
    #	print("	Dauer  : %2d"  + str(minuten) + " : " + str(sekunden))
    print()

    sendInfoMail(start.strftime('%A, der %d.%m.%Y'),start.time().strftime("%H:%M:%S"), 
    #sendInfoMail(start.strftime('%H:%M Uhr am %A, dem %d.%m.%Y'),start.time().strftime("%H:%M:%S"), 
    end.time().strftime("%H:%M:%S"),str(note),str(duration),user ,
    str(gesamt),str(fehler),
    settingKonjugation,
    "Pauken", 
    richtigListe, fehlerListe)


def checkTempusList(konjugationJson,  tempus, tempusList):
    result = {}
    basis = tempus["basis"]
    infinitive = konjugationJson["infinitive"]
    frageText = " " +tempusList["fall"] 
    frageText = frageText.ljust(25) 
    if "sonderform" in tempusList:
        ergebnis = tempusList["sonderform"]
    else:
        ergebnis = basis+tempusList["endung"]
    eingabe = input(frageText+ "> ")

    length = 25 + len(eingabe) + 4
    moveString = "\033[{}C\033[1A".format(length) # \033[1C (one Column right) \033[1A (one row up)

    asked = { 'language' : "la", 
        'question' :  tempus["name"] + ", " + frageText, 
        'correctAnswer' : [ergebnis], 
        'answer' :  eingabe.ljust(18) 
        }

    result["question"] = asked
    
    if (eingabe != ergebnis):
        diffed_result = show_diff(eingabe, ergebnis)
        print(moveString + ">> Falsch richtig wäre: " + Color.BOLD + Color.RED + ergebnis + Color.END + Color.DARKCYAN +" >" + Color.END + diffed_result + Color.DARKCYAN +"<" + Color.END,flush=True)
        result["correct"] =  False
    else:
        result["correct"] = True
    return result

def checkKonjugation(konjugationJson):
    result ={}
    gesamt = 0
    fehler = 0
    richtigListe = []
    fehlerListe = []
    
    print("")
    print("**** Abfrage für " + Color.BOLD + konjugationJson["infinitive"] + Color.END + " " + konjugationJson['name'] + " ****")  
    print("")
    print(Color.BOLD + Color.BLUE +  "Präsens")
    print("=======" + Color.END) 
    for tempusList in prasens(konjugationJson)["faelle"]:
        result = checkTempusList(konjugationJson, prasens(konjugationJson), tempusList)
        correct = result["correct"]
        question = result["question"]
        gesamt += 1
        if correct:
            richtigListe.append(question)
        else:
            fehler += 1
            fehlerListe.append(question)

    print("")

    print(Color.BOLD + Color.BLUE +  "Perfekt")
    print("=======" + Color.END) 
    for tempusList in perfekt(konjugationJson)["faelle"]:
        result = checkTempusList(konjugationJson, perfekt(konjugationJson),  tempusList)
        correct = result["correct"]
        question = result["question"]
        gesamt += 1
        if correct:
            richtigListe.append(question)
        else:
            fehler += 1
            fehlerListe.append(question)


    result["richtig"] = richtigListe
    result["falsch"] = fehlerListe
    result["gesamt"] = gesamt
    result["fehler"] = fehler
    return result


def parseKonjugation(json):
    
    for konjugation in konjugationen:
        print()
        print("**** " + konjugation['name'] + " ****")
        print(konjugation)  
        for kasus in singular(konjugation):
            print(kasus + ":\t" + konjugation["basis"]+""+singular(konjugation)[kasus])



def calcSchulnote(gesamt, fehler):
	if gesamt == 0:
		return 0
	fehler = fehler
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

def usage():
    print('Usage: ./konjugieren.py [-i] [-e] [-a] [-k]')
    print('	-a             :: a Konjugation)')
    print('	-i             :: o Konjugation)')
    print('	-e             :: e Konjugation)')
    print('	-k             :: konsonantische Konjugation)')
    print('	-t <präsens|imperfekt|perfekt|plusquamperfekt>    :: tempus')
    print('Example:')
    print('	./konjugieren.py -a')

def parseParamter(argv):
    setting = {}
    konjugation = ""
    try:
        opts, args = getopt.getopt(argv,"aiek",["a","i","e","k"])
    except getopt.GetoptError:
        usage()
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            usage()
            sys.exit()
        elif opt in ("-a", "--a"):
           konjugation = "a"
        elif opt in ("-o", "--o"):
           konjugation = "o"
        elif opt in ("-e", "--e"):
           konjugation = "e"


    setting["konjugation"] = konjugation
    return setting


def printHeader():
    header = (
        " ____  __.                 __             .__                             \n"
        "|    |/ _|____   ____     |__|__ __  ____ |__| ___________   ____   ____  \n"
        "|      < /  _ \\ /    \\    |  |  |  \\/ ___\|  |/ __ \\_  __ \\_/ __ \\ /    \\ \n"
        "|    |  (  <_> )   |  \\   |  |  |  / /_/  >  \\  ___/|  | \\/\  ___/|   |  \\\n"
        "|____|__ \\____/|___|  /\__|  |____/\___  /|__|\___  >__|    \\___  >___|  /\n"
        "        \\/          \\/\______|    /_____/         \\/            \\/     \\/\n"
    )
    print(header)

def main(argv):
    os.system('clear')
    printHeader()
    setting = parseParamter(argv)
    konjugationen = readKonjugationen()
    # print(konjugation)
    # print(setting)
    runTest(konjugationen["Konjugationen"], setting["konjugation"])


if __name__ == "__main__":
   main(sys.argv[1:])