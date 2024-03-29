#!/usr/local/bin/python3

import random
import sys
import getopt
import os
from vocabulary.Config import Color
import datetime
import time
from vocabulary.util.FileHandler import readDeklination
from vocabulary.util.Mail import sendInfoMail
from vocabulary.util.Diff import show_diff
from vocabulary.util.MqttClient import publishResult


def plural(json):
    return [x for x in json["numerus"] if x['name'] == "plural"][0]

def singular(json):
    return [x for x in json["numerus"] if x['name'] == "singular"][0]


def runTest(deklinationen, setting):

    settingDeklination = setting["deklination"]
    settingGenus = setting["numerus"]
    kasus = setting['kasus']

    # print("Die folgenden Kasus werden abgefragt:" + str(kasus))

    # measure time
    startTime = time.time()
    start = datetime.datetime.now()

    # do the test
    try:
        if settingDeklination == "":
            zufallsIndex = random.randint(0,len(deklinationen)-1)
            deklination = deklinationen[zufallsIndex]  
        else: # deklination is given by user
            deklinationen = [x for x in deklinationen if x['name'] == settingDeklination+"-Deklination"]
            if len(deklinationen) == 1: # there is exactly one hit ignoring genus
                deklination = deklinationen[0]
            elif len(deklinationen) > 1: # there is more than one hit
                if settingGenus == "": # no genus but multiple hits
                    zufallsIndex = random.randint(0,len(deklinationen)-1)
                    deklination = deklinationen[zufallsIndex]
                else: # genus is given trying
                    deklination = [x for x in deklinationen if x['genus'] == settingGenus][0]
    except IndexError:
        print("")
        print(Color.RED + settingDeklination + "-Deklination für " + settingGenus + "kann nicht geladen werden" + Color.END)
        sys.exit(3)
  
    settingDeklination = deklination["name"]
    #print(deklination)
    result = checkDeklination(deklination, kasus)
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

   # publishResult(user, "Latein","Deklinieren", settingDeklination, "Pauken",  note, duration, gesamt, fehler)
    # sendInfoMail(start.strftime('%A, der %d.%m.%Y'),start.time().strftime("%H:%M:%S"), 
    # end.time().strftime("%H:%M:%S"),str(note),str(duration),user ,
    # str(gesamt),str(fehler),
    # settingDeklination,
    # "Pauken", 
    # richtigListe, fehlerListe)


def checkKasusList(deklinationJson, numerus, kasusList, pick):
    result = {}
    basis = deklinationJson["basis"][pick]
    # nominativ = deklinationJson["nominativ"][pick]
    frageText = " " +kasusList["kasus"] + ", " + numerus
    frageText = frageText.ljust(25) 
    if "sonderform" in kasusList:
        ergebnis = kasusList["sonderform"]
    else:
        ergebnis = basis+kasusList["endung"]
    eingabe = input(frageText+ "> ")

    length = 25 + len(eingabe) + 4
    moveString = "\033[{}C\033[1A".format(length) # \033[1C (one Column right) \033[1A (one row up)

    asked = { 'language' : "la", 'question' :  frageText.ljust(25), 'correctAnswer' : [ergebnis], 'answer' :  eingabe.ljust(18) }
    result["question"] = asked
    
    if (eingabe != ergebnis):
        diffed_result = show_diff(eingabe, ergebnis)
        print(moveString + ">> Falsch richtig wäre: " + Color.BOLD + Color.RED + ergebnis + Color.END + Color.DARKCYAN +" >" + Color.END + diffed_result + Color.DARKCYAN +"<" + Color.END,flush=True)
        result["correct"] =  False
    else:
        result["correct"] = True
    return result

def checkDeklination(deklinationJson, kasusList):
    result ={}
    gesamt = 0
    fehler = 0
    richtigListe = []
    fehlerListe = []

    pick_max = len(deklinationJson["nominativ"])
    #print(deklinationJson["nominativ"])
    pick = random.randint(0,pick_max-1)
    print("")
    print("**** [Vokabel " + str(pick+1) + "/" + str(pick_max) + "] Abfrage für " + Color.BOLD + deklinationJson["nominativ"][pick] + Color.END + " " + deklinationJson['name'] + " " + deklinationJson['genus'] +" ****")  
    print("")

    for singularKasusEntry in singular(deklinationJson)["kasus"]:
        if (singularKasusEntry['kasus'] in kasusList):
            result = checkKasusList(deklinationJson, "Singular", singularKasusEntry, pick)
            correct = result["correct"]
            question = result["question"]
            gesamt += 1
            if correct:
                richtigListe.append(question)
            else:
                fehler += 1
                fehlerListe.append(question)
        # else:
        #     print("Skipping " +str(singularKasusEntry))

    print("")

    for pluralKasusList in plural(deklinationJson)["kasus"]:
        if (pluralKasusList['kasus'] in kasusList):
            result = correct = checkKasusList(deklinationJson, "Plural", pluralKasusList, pick)
            correct = result["correct"]
            question = result["question"]
            gesamt += 1
            if correct:
                richtigListe.append(question)
            else:
                fehler += 1
                fehlerListe.append(question)
        # else:
        #     print("Skipping " +str(pluralKasusList['kasus']))

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
    print('Usage: ./deklinieren.py [-o] [-e] [-u] [-a] [-k] [-g <m|n|f>]]')
    print('	-a             :: a Dekliniation')
    print('	-o             :: o Dekliniation')
    print('	-e             :: e Dekliniation')
    print('	-u             :: u Dekliniation')
    print('	-s             :: konsonantische Dekliniation')
    print('	-m             :: gemischte Dekliniation')
    print(' -g <m|n|f>     :: genus')
    print(' -k <ngdab>     :: kasus Nominativ Genetiv Dativ Akkusativ aBlativ')
    print('Example:')
    print('	./deklinieren.py -a')

def parseParamter(argv):
    setting = {}
    deklination = ""
    numerus = ""
    kasus = []
    try:
        opts, args = getopt.getopt(argv,"amoesuk:g:",["a","m","o","e","s","u","k=","g="])
    except getopt.GetoptError:
        usage()
        sys.exit(2)
    for opt, arg in opts:
        # print (str(opt) + " = " + str(arg))
        if opt == '-h':
            usage()
            sys.exit()
        elif opt in ("-a", "--a"):
           deklination = "a"
        elif opt in ("-o", "--o"):
           deklination = "o"
        elif opt in ("-e", "--e"):
           deklination = "e"
        elif opt in ("-u", "--u"):
           deklination = "u"
        elif opt in ("-m", "--m"):
           deklination = "gemischte"
        elif opt in ("-s", "--s"):
           deklination = "konsonantische"
        elif opt in ("-g", "--g"):
            if arg == "f":
               numerus = "femininum"
            elif arg == "m":
                numerus = "maskulinum"
            elif arg == "n":
                numerus ="neutrum"
        elif opt in ("-k", "--k"):
            if "n" in arg:
               kasus.append("Nominativ")
            if "g" in arg:
               kasus.append("Genetiv")
            if "d" in arg:
               kasus.append("Dativ")
            if "a" in arg:
               kasus.append("Akkusativ")
            if "l" in arg:
               kasus.append("Ablativ")
    
    if len(kasus) == 0:
        kasus =  ['Nominativ', 'Genetiv', 'Dativ', 'Akkusativ', 'Ablativ']

    setting["deklination"] = deklination
    setting["numerus"] = numerus
    setting["kasus"] = kasus
    return setting


def printHeader():
    header = (
        "________          __   .__  .__       .__                             \n"
        "\______ \   ____ |  | _|  | |__| ____ |__| ___________  ____   ____   \n"
        " |    |  \_/ __ \|  |/ |  | |  |/    \|  _/ __ \_  __ _/ __ \ /    \  \n"
        " |    `   \  ___/|    <|  |_|  |   |  |  \  ___/|  | \\\\  ___/|   |  \ \n"
        "/_______  /\___  |__|_ |____|__|___|  |__|\___  |__|   \___  |___|  / \n"
        "        \/     \/     \/            \/        \/           \/     \/ 1.1"
    )
    print(header)

def startTest(argv):
    os.system('clear')
    printHeader()
    setting = parseParamter(argv)
    deklinationen = readDeklination()
    # print(deklination)
    # print(setting)
    runTest(deklinationen['Deklinationen'], setting)


if __name__ == "__main__":
   startTest(sys.argv[1:])