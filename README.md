Simple Python3 Command Line tool to train foreign languange vocabulary.   
Done with my son for his English and Latin course.   

![alt text](https://github.com/andreasgruener/vocabulary/blob/master/example/Example-Screenshot.png?raw=true "Example Screen of running Vocabulary Test")

# Status
Works for ourselves - not prepared to run out of the box, e.g.
- Python dependencies need to be installed first, 
- internationalization 

# Requirements / Dependencies
## Mac
- Install Python3 
-- brew install python3
- Install enchant (Spellchecker)
-- brew install enchant
- Install pyenchant
-- pip3 install pyenchant

# Vocabulary Test - Features:
## Question
- foreign language words - asks e.g. latin you answer in your language
- orginal language words - asks your langauge you answer in e.g. latin
- number of words k - the number of 
- all variants - you need to provide all variants of a translation 
- voice based results (say correct answer)  - says the correct answer (works on mac)
- no problem vocabulary - switches of default mode, which asks all wrongly answered vaocabularies at the end

## Grades
Gives a grade based on the german school grades (1 - Best to 6 - worst)  
Ergebnis:  

	Note 		: 6.0

	Duration   	: 0 Minuten 30 Sekunden
	Total  		:  20
	Correct 	:  18
	Wrong  		:  2


## Usage Tracker
Creates a .result file, which contains the time duration type of test and the result, e.g.:  
2017-03-05 : 11:34:23 : 11:34:27 : 6 : 3.0 :username : 18 : 20 : mixed : ./example-voc.csv  

## Problem Vocabulary
Keeps track of wrong vocabulary and mixes the problem vocabulary into the question stream.
Example File:
example-voc.csv_problemVocabularyFile
de;böse;['iratus'];irratus;1  
(Language; Vocabulary; Correct Answer(s), Wrong Ansert; Wrong Count  

## Vocabulary Tracker
Keeps track that the randomly asked vocabularies are distributed somehow evenly.  
{'dum': 2, 'fluere,volvere': 2, 'aegrotus': 2, 'forum': 2, 'iratus': 2, 'quamquam': 2, 'ignoscere': 2, 'diu': 2, 'quod': 2, 'imperium': 2, 'caput': 2, 'templum': 2, 'aedificum': 2}

## Usage
Usage: ./vocabulary.py -i <inputfile> [-v] [-e] [-d] [-m] [-r] [-c n] [-h]  
	-i <inputfile> :: name of the file containing the vocabulary  
	-v             :: voice based results (say correct answer)  
	-n             :: no problem vocabulary  
	-h             :: prints this help message   
	-f             :: asks foreign language words  
	-d             :: asks orginal language words  
	-m             :: asks mixed  
	-c <Anzahl>    :: number of words to ask  
	-a             :: all variants are asked  
   
Example:  
	./vocabulary.py -i voc.csv


# Spellchecker
Checks the CSV file for typos (English only)

CSV based vocabulary files. Strcuture of vocabulary files:  

```<Vocabulary>[:<Alternate Vocabulary>]*;<Translation>[:<Alternate Translation>]*```
Example:  
fluere,volvere;fließen:strömen  
fluere;fließen

## Usage
Usage: ./SpellChecker.py -i <inputfile> [-v] [-e] [-d] [-m] [-r] [-c n] [-h]  
	-i <inputfile> :: name of the file containing the vocabulary  

   
Example:  
	./SpellChecker.py -i voc.csv


# Generate Latin Test 
Generates a simple latin test based on the vocabulary. If the lines contains the type of word it asks for Genus and Kasus or Person and mode.

## Usage
Usage: ./generateLatinTest.py -i <inputfile> [-c n] [-h]
        -i <inputfile> :: name of the file containing the vocabulary
        -h             :: prints this help message
        -c <Anzahl>    :: number of words to ask

Example:
        ./generateLatinTest.py -i voc.csv -v