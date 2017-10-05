#!/usr/local/bin/python3

import random
import sys
import getopt
import os
from Config import Color
import datetime
import time
from FileHandler import readDeklination
from mail import sendInfoMail


def plural(json):
    return [x for x in json["numerus"] if x['name'] == "plural"][0]

def singular(json):
    return [x for x in json["numerus"] if x['name'] == "singular"][0]


def runTest(deklinationen, type):

    # measure time
    startTime = time.time()
    start = datetime.datetime.now()

    # do the test
    try:
        deklination = [x for x in deklinationen if x['name'] == type+"-Deklination"][0]
    except IndexError:
        print("")
        print(Color.RED + type + "-Deklination kann nicht geladen werden" + Color.END)
        sys.exit(3)

    #print(deklination)
    result = checkDeklination(deklination)
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
    type+"-Deklinination",
    "Pauken", 
    richtigListe, fehlerListe)


def checkKasusList(deklinationJson, numerus, kasusList):
    result = {}
    basis = deklinationJson["basis"]
    nominativ = deklinationJson["nominativ"]
    frageText = "\t"+kasusList["kasus"] + ", " + numerus
    frageText = frageText.ljust(25) 
    ergebnis = basis+kasusList["endung"]
    eingabe = input(frageText+ "> ")
    	
    asked = { 'language' : "la", 'question' :  frageText.ljust(25), 'correctAnswer' : [ergebnis], 'answer' :  eingabe.ljust(18) }
    result["question"] = asked
    
    if (eingabe != ergebnis):
        print(Color.RED + "\tFalsch richtig wäre: " + ergebnis +Color.END,flush=True)
        result["correct"] =  False
    else:
        result["correct"] = True
    return result

def checkDeklination(deklinationJson):
    result ={}
    gesamt = 0
    fehler = 0
    richtigListe = []
    fehlerListe = []
    
    print("")
    print("**** Abfrage für " + Color.BOLD + deklinationJson["nominativ"] + Color.END + " " + deklinationJson['name'] + " " + deklinationJson['genus'] +" ****")  
    print("")

    for singularKasusEntry in singular(deklinationJson)["kasus"]:
        result = checkKasusList(deklinationJson, "Singular", singularKasusEntry)
        correct = result["correct"]
        question = result["question"]
        gesamt += 1
        if correct:
            richtigListe.append(question)
        else:
            fehler += 1
            fehlerListe.append(question)

    print("")

    for pluralKasusList in plural(deklinationJson)["kasus"]:
        result = correct = checkKasusList(deklinationJson, "Plural", pluralKasusList)
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


def parseDeklination(json):
    
    for deklination in deklinationen:
        print()
        print("**** " + deklination['name'] + " ****")
        print(deklination)  
        for kasus in singular(deklination):
            print(kasus + ":\t" + deklination["basis"]+""+singular(deklination)[kasus])



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
    print('Usage: ./deklinieren.py [-o] [-e] [-a] ]')
    print('	-a             :: a Dekliniation)')
    print('	-o             :: o Dekliniation)')
    print('	-e             :: e Dekliniation)')
    print()
    print('Example:')
    print('	./deklinieren.py -a')

def parseParamter(argv):
    deklination = "a"
    try:
        opts, args = getopt.getopt(argv,"aoe",["a","o","e"])
    except getopt.GetoptError:
        usage()
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            usage()
            sys.exit()
        elif opt in ("-a", "--a"):
           deklination = "a"
        elif opt in ("-o", "--o"):
           deklination = "o"
        elif opt in ("-e", "--e"):
           deklination = "e"

    return deklination




def main(argv):
    deklination = parseParamter(argv)
    deklinationen = readDeklination()
    print(deklination)
    runTest(deklinationen['Deklinationen'], deklination)


if __name__ == "__main__":
   main(sys.argv[1:])