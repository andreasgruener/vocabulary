Simple Python3 Command Line tool to train foreign languange vocabulary.   
Done with my son for his English and Latin course.   

![alt text](https://github.com/andreasgruener/vocabulary/blob/master/example/Example-Screenshot.png?raw=true "Example Screen of running Vocabulary Test")

It offers three features:
- A) Vocabulary Trainer
- B) Spellchecker for english vocabulary files 
- C) Generate Latin declination & konjugation
All three use the same file format

## File Format
CSV based vocabulary files. Strcuture of vocabulary files:  
```<Vocabulary>[:<Alternate Vocabulary>]*;<Translation>[:<Alternate Translation>]*```

Example:  
fluere:volvere;fließen:strömen  
fluere;fließen

### Optional Type pf Word (for Latin Test see C) )
- A: Adjective 
- S: Noun (Substantiv)
- V; Verb  

```<Vocabulary>[:<Alternate Vocabulary>]*;<Translation>[:<Alternate Translation>]*;<A|V|N>```

Example:   
		fluere,volvere;fließen:strömen;V  
		fluere;fließen;V  
		dominus;Herr;S     
		iratus;böse;A  

## Status
- Works, is in daily use
- Python dependencies need to be installed first
- internationalization missing
- focus on our needs, not generalized

## Progress
- Latin: Genus, Genetiv & Verbs, Times
  - additional file format | for genetiv, genus and fpr present, perfect

## Requirements / Dependencies
### Mac
~~~bash
# Install Python3  
bash> brew install python3 
# Install enchant (Spellchecker)
bash> brew install enchant
# Install pyenchant
bash> pip3 install pyenchant
~~~
# A) Vocabulary Test - Features:
## Question
- foreign language words - asks e.g. latin you answer in your language
- orginal language words - asks your langauge you answer in e.g. latin
- number of words k - the number of 
- all variants - you need to provide all variants of a translation 
- voice based results (say correct answer)  - says the correct answer (works on mac)
- no problem vocabulary - switches of default mode, which asks all wrongly answered vaocabularies at the end

## Grades
Gives a grade based on the german school grades (1 - Best to 6 - worst)  
~~~
Ergebnis:
============= Ergebnis ================

        Note            : 6.0

---------------------------------------
        Dauer   : 0 Minuten 4 Sekunden
        Gesamt  :  26
        Richtig :  0
        Falsch  :  26
=======================================
~~~


## Usage Tracker
Creates a .result file, which contains the time duration type of test and the result, e.g.:  
~~~~
2017-03-05 : 11:34:23 : 11:34:27 : 6 : 3.0 :username : 18 : 20 : mixed : ./example-voc.csv  
~~~
## Problem Vocabulary
Keeps track of wrong vocabulary and mixes the problem vocabulary into the question stream.
~~~
Example File:
example-voc.csv_problemVocabularyFile
de;böse;['iratus'];irratus;1  
(Language; Vocabulary; Correct Answer(s), Wrong Ansert; Wrong Count  
~~~~

## Vocabulary Tracker
Keeps track that the randomly asked vocabularies are distributed somehow evenly.  
~~~~
{'dum': 2, 'fluere,volvere': 2, 'aegrotus': 2, 'forum': 2, 'iratus': 2, 'quamquam': 2, 'ignoscere': 2, 'diu': 2, 'quod': 2, 'imperium': 2, 'caput': 2, 'templum': 2, 'aedificum': 2}
~~~~

## Usage
~~~
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
~~~

# B) Spellchecker
Checks the CSV file for typos (English only)

## Usage
~~~
Usage: ./SpellChecker.py -i <inputfile> [-v] [-e] [-d] [-m] [-r] [-c n] [-h]  
	-i <inputfile> :: name of the file containing the vocabulary  

Example:  
	./SpellChecker.py -i voc.csv
~~~

# C) Generate Latin Test 
Generates a simple latin test based on the vocabulary. If the lines contains the type of word it asks for Genus and Kasus or Person and mode.

## Usage
~~~
Usage: ./generateLatinTest.py -i <inputfile> [-c n] [-h]
        -i <inputfile> :: name of the file containing the vocabulary
        -h             :: prints this help message
        -c <Anzahl>    :: number of words to ask

Example:
        ./generateLatinTest.py -i voc.csv -v
~~~

## Example Report
~~~
bash-3.2$ ./generateLatinTest.py -i example/example-voc.csv
Es werden 12 Vokabeln abgefragt.
example
====================================================================
 Vokabeldatei : example/example-voc.csv
 Erzeugt am   : 2017-03-05_19-23
====================================================================
--------------------------------------------------------------------
                               |
caput :                        |
  Gen. Pl.                     |
--------------------------------------------------------------------
                               |
fluere :                       |
  2. Pers Pl.                  |
--------------------------------------------------------------------
                               |
imperium :                     |
  Gen. Pl.                     |
--------------------------------------------------------------------
                               |
forum :                        |
  Akk. Pl.                     |
--------------------------------------------------------------------
                               |
quod :                         |
                               |
--------------------------------------------------------------------
                               |
iratus :                       |
  m. Gen. Sg.                  |
--------------------------------------------------------------------
                               |
templum :                      |
  Gen. Pl.                     |
--------------------------------------------------------------------
                               |
aedificum :                    |
  Gen. Pl.                     |
--------------------------------------------------------------------
                               |
quamquam :                     |
                               |
--------------------------------------------------------------------
~~~

# Requirements / Dependencies
## Mac
- Install Python3 
  - brew install python3
- Install enchant (Spellchecker)
  - brew install enchant
- Install pyenchant
  -pip3 install pyenchant