'''
Luke De Vos
Generate words with char ngrams markov chains
2020 11 June
'''


import random
import sys
import re
from sty import fg, bg, rs

'''
FUNCTIONS ==
'''

#return total of all ngram counts in a list
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

#returns true if passed string has a non-whitespace next char in passed list
def hasNextLetter(string):
	global gramLNN
	matchList=[]
	thisGram=string[-gramLen:]
	for entry in gramLNN:
		if isGramMatch(thisGram, entry[0]):
			matchList.append(entry)
	#print('matchList for \'' + string[-gramLen:] + '\': ' + str(matchList))
	if len(matchList) == 0:
		return False
	return True

#return list of relative frequencies. each entry is the rel freq of a term in passed list of gram:count lists
def getRelFreqs(L):
	totalGrams=getSum(L)
	newL=[]	#store rel freqs, return at end
	for entry in L:
		newL.append(entry[1]/totalGrams)
	return newL

#return average (float) of elements in passed list of numbers
def getAvg(L):
	total=0
	for entry in L:
		total += entry
	return total/len(L)

#generates gram to start generation
#returns string of length gramLen
def getFirstGram():
	global startGramL 
	global likelyL
	global relFreqL
	rfL=getRelFreqs(startGramL)
	if iSet or cSet: avg=getAvg(rfL)
	while True:
		chance=0.0
		r=random.random()
		for i in range(len(startGramL)):
			chance += rfL[i]
			if r < chance:
				if hasNextLetter(startGramL[i][0]):
					if iSet or cSet: likelyL.append(rfL[i] - avg)
					if iSet: relFreqL.append(rfL[i])
					return startGramL[i][0]
				break
			

#determines and returns a character based on the last gramLen-1 generated characters
def getNextChar(output, NN):	#(string, bool)
	global gramL
	global gramLNN
	global likelyL
	lastGram = output[-gramLen:]
	#get list of matches
	matchList=[]
	if NN: 
		for entry in gramLNN:
			if isGramMatch(lastGram, entry[0]):
				matchList.append(entry)
	else:
		for entry in gramL:
			if isGramMatch(lastGram, entry[0]):
				matchList.append(entry)
	chance = 0.0
	r=random.random()
	rfL=getRelFreqs(matchList)		#rfL is a list of the relative frequencies of the terms in matchList
	if iSet or cSet: avg=getAvg(rfL)	#avg is the average value of rfL
	for i in range(len(matchList)):
		chance += rfL[i]
		if r < chance:
			if iSet or cSet: likelyL.append(rfL[i] - avg)
			if iSet: relFreqL.append(rfL[i])
			return matchList[i][0][-1]

#color print
def cPrint(string):	#(string)
	global likelyL
	global initLen
	j=0
	for i in range(len(string) - (initLen-1)):
		#if chance[i] is positive, it is more likely than average
		c0=0
		c1=0
		if likelyL[i] < 0:
			c0 = int(-likelyL[i] * 6 * 255)
			if c0 > 255:
				c0 = 255
		elif likelyL[i] > 0:
			c1 = int(likelyL[i] * 200)
		#clump together initial gram or passed root
		if i==0:
			while j < initLen:
				print(bg(c0,c1,0) + string[j] + bg.rs,end='')
				j+=1
		#print trailing \n as space
		elif i==len(string) - initLen:
			print(bg(c0,c1,0) + " " + bg.rs,end='')
		#normally
		else:
			print(bg(c0,c1,0) + string[j] + bg.rs,end='')
			j+=1
	print()


'''
========================
'''

trainingSet = "dictionary.txt"	#file from which ngrams are drawn
gramLen=4			#gram length
startGramD={} 		#dict of char ngrams that begin words in the training set
gramD={}			#dict of the rest of the char ngrams in the training set
startGramL=[] 		#above dicts coverted to lists once completely written. for faster traversal
gramL=[]			#"
startGramLNN=[]		#copy of startGramL except no grams end with whitespace
gramLNN=[]			#"
likelyL=[]			#if iSet or cSet, for each char generated, likelyL appends the char's relative frequency minus the average relative frequency in the list of possible next chars
relFreqL=[]			#if iSet, stores relative frequency of each generated char



#COMMAND LINE ARGS
root=''		#assigned to final arg if it is a [A-Za-z] word, not a flag
			#otherwise assigned gram from a startGram list
			#serves as base from which to generate more characters
minNo=0		#minimum length of generated word. set with -min flag
maxNo=1000	#maxmimum length of generated word. set with -max flag
#bools set with flags of the corresponding letter. if True...
vSet=False	#generation is printed each time a character is generated
cSet=False	#generated chars are highlighted red if their generation was "unusual", green if it was particularly likely
sSet=False	#user must hit ENTER to generate next char. Ideally paired with -v
iSet=False	#outputs extra info. first column is generated char's relative frequency (and probability of generation given previous state), second column is 
if len(sys.argv) > 1:
	line=" ".join(sys.argv[1:])
	#ensure command line args fit form that will be processed correctly
	match=re.match("^((\-(min|max|n) [0-9]+)( |$)|(\-[vcsi])( |$))*( *[a-zA-Z]+)? *$", line) #what a doozy
	if match == None:
		print('Invalid arguments syntax')
		sys.exit()

	#flags
	for i in range(1, len(sys.argv)):
		if sys.argv[i] == '-min':
			minNo = int(sys.argv[i+1])
		elif sys.argv[i] == '-max':
			maxNo = int(sys.argv[i+1])
		elif sys.argv[i] == '-v':
			vSet = True
		elif sys.argv[i] == '-n':
			gramLen = int(sys.argv[i+1])
		elif sys.argv[i] == '-c':
			cSet = True
		elif sys.argv[i] == '-s':
			sSet = True
		elif sys.argv[i] == '-i':
			iSet = True

	#match passed root
	match = re.match("^[A-Za-z]+ *$", sys.argv[-1])
	if match != None:
		root = match.group().strip()
		root = " "+root
	#check root
	while (len(root) > 0 and len(root) < gramLen):	#no -1 because " " is added to beginning
		print("Passed word must be at least (" + str(gramLen-1) + ") characters long")
		print("Please re-enter: ")
		root = " "+input()

#populate startGramD and gramD 
with open(trainingSet) as file:
	for line in file:
		line=" "+line
		for i in range(len(line)-gramLen+1): #+1 to include newline
			gram = line[i:i+gramLen]
			if i == 0:
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
#also create versions without trailing \n
for key in gramD:
	gramL.append([key])
	gramL[-1].append(gramD[key])
	if key[-1] != '\n':
		gramLNN.append([key])
		gramLNN[-1].append(gramD[key])
for key in startGramD:
	startGramL.append([key])
	startGramL[-1].append(startGramD[key])
	if key[-1] != '\n':
		startGramLNN.append([key])
		startGramLNN[-1].append(startGramD[key])

#check root again, now with gram info
while (len(root) > 0 and len(root) < gramLen-1) or root != '' and not hasNextLetter(root):
	if (len(root) > 0 and len(root) < gramLen-1):
		print("Passed word must be at least (" + str(gramLen-1) + ") characters long")
	elif not hasNextLetter(root):
		print("Passed word is never followed by a non-whitespace character")
	print("Please re-enter: ")
	root = " "+input()
		

#GENERATION
output=''	#generated characters added to output. output printed when complete
nextChar=''
NN=False	#"No Newline"
initLen=0
print("\n<Hit ENTER to generate word>")
while input() == '':
	deadEndL=[]
	likelyL=[]
	relFreqL=[]
	if root == '': #user did not pass a root
		output = getFirstGram()
	else:
		output = root
		if iSet or cSet: likelyL.append(0)
		if iSet: relFreqL.append(0)
	initLen = len(output)	#initial length
	while output[-1] != '\n':
		if vSet: 
			if iSet:
				sign=''
				print(str(round(relFreqL[-1]*100, 2))+'%\t',end='')
				if likelyL[-1] >= 0: sign='+'
				print(sign+str(round(likelyL[-1]*100, 2))+'%\t',end='')
			print(output,end='')
			print()
		if len(output) < minNo+1:	#+1 because trailing whitespace is part of generation
			NN = True
		else:
			NN = False
		if len(output.strip()) <= maxNo:
			output = output + getNextChar(output, NN)	
		else:
			deadEndL.append(output[-gramLen:])
			for i in range(deadEndL.count(output[-gramLen:])):
				if len(output) > initLen:
					output = output[0:-1]
					if likelyL: likelyL.pop()
					if relFreqL: relFreqL.pop()
		if sSet:	#wait for user to hit enter to generate next character
			input()

	#print final complete generation
	if cSet:
		if iSet:
			sign=''
			print(str(round(relFreqL[-1]*100, 2))+'%\t',end='')
			if likelyL[-1] >= 0: sign='+'
			print(sign+str(round(likelyL[-1]*100, 2))+'%\t',end='')
		print(" ",end='')
		cPrint(output)
	else:
		print(" "+output,end='')

print("EXIT")










	
