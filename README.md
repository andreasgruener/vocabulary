Simple Python3 Command Line tool to train foreign languange vocabulary.   
Done with my son for his English and Latin course.   

# Features:
## Question
- foreign language words - asks latin you answer in yout language
- orginal language words - asks latin/english/french/german/etc. and your language
- number of words k - the number of 
- all variants - you need to provide all variante of a translation  
- voice based results (say correct answer)  - says the correct answer (works on mac)
- no problem vocabulary - switches of default mode, which asks all wrongly answered vaocabularies at the end

## Problem Vocabulary
Keeps track of wrong vocabulary and mixes the problem vocabulary into the question stream.
Example File:
example-voc.csv_problemVocabularyFile
de;böse;['iratus'];irratus;1  
(Language; Vocabulary; Correct Answer(s), Wrong Ansert; Wrong Count  

### Tracker
Keeps track that the randomly asked vocabularies are distributed evenly.  
{'dum': 2, 'fluere,volvere': 2, 'aegrotus': 2, 'forum': 2, 'iratus': 2, 'quamquam': 2, 'ignoscere': 2, 'diu': 2, 'quod': 2, 'imperium': 2, 'caput': 2, 'templum': 2, 'aedificum': 2}

### Spellchecker
Checks the CSV file for typos (English only)

CSV based vocabulary files. Strcuture of vocabulary files:  

```<Orignial Language Term>[,<Alternate Orig Language Termin]*;<Translation>[:<Alternate Translation>]*```
Example:  
fluere,volvere;fließen:strömen  
fluere;fließen


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
