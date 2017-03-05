Simple Command Line tool to train foreign languange vocabulary.   
Done with my son for his English and Latin course.   
  
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
