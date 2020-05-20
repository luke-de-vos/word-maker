'''
Luke De Vos
Generate words with char ngrams markov chains
2020 May 11
'''

import random
import sys

'''
FUNCTIONS
'''

#return total of all ngram counts in list
def getSum(passedL):	#(list of [ngram, count]s)
	total=0
	for entry in passedL:
		total += entry[1]
	return total

#returns True if passed grams "gram match"
def isGramMatch(gram1, gram2): 	#(string, string)
	if gram1[1:] == gram2[0:-1]: #XYY == YYZ
		return True
	return False

#generates gram to start generation
#returns string of length gramLen
def getFirstGram():
	global startGramL
	global totalStartGrams 
	chance = 0.0
	r = random.random()
	for entry in startGramL:
		chance += entry[1]/totalStartGrams
		if r < chance:
			return entry[0]

#determines and returns a character based on the last gramLen-1 generated characters
def getNextChar(output):	#(string)
	global gramL
	lastGram = output[-gramLen:]
	#get list of matches
	matchList = []
	for entry in gramL:
		if isGramMatch(lastGram, entry[0]):
			matchList.append(entry)
	totalGrams = getSum(matchList)
	chance = 0.0
	r = random.random()	
	for entry in matchList:
		chance += entry[1]/totalGrams
		if r < chance:
			return entry[0][-1]
	

'''
========================
'''

trainingSet = "Corpora/dictionary.txt"	#file from which ngrams are drawn
gramLen = 4			#gram length
totalStartGrams = 0	#total number of grams that begin words
startGramD = {} 	#dict of char ngrams that begin words in the training set
gramD = {}			#dict of the rest of the char ngrams in the training set
startGramL = [] 	#above dicts coverted to lists once completely written. for faster traversal
gramL = []	

#populate startGramD and gramD 
with open(trainingSet) as file:
	for line in file:
		for i in range(len(line)-gramLen+1): #+1 to include newline
			gram = line[i:i+gramLen]
			if i == 0:
				totalStartGrams+=1
				if gram in startGramD:
					startGramD[gram] += 1
				else:
					startGramD[gram] = 1
			else:
				if gram in gramD:
					gramD[gram] += 1
				else:
					gramD[gram] = 1
#sort dicts by value, high low
gramD={k: v for k, v in sorted(gramD.items(), key=lambda item: item[1], reverse=True)}
startGramD={k: v for k, v in sorted(startGramD.items(), key=lambda item: item[1], reverse=True)}
#convert dicts to lists
for key in gramD:
	gramL.append([key])
	gramL[-1].append(gramD[key])
for key in startGramD:
	startGramL.append([key])
	startGramL[-1].append(startGramD[key])

#GENERATION
print("<Hit ENTER to generate word>")
while input() == '':
	output=""
	if len(sys.argv) > 1 and len(sys.argv[1]) >= gramLen:
		output = sys.argv[1]
	else:
		output = getFirstGram()
	while output[-1] != '\n':	
		output = output + getNextChar(output)

	#output result
	print(output,end='')

print("EXIT")










	
