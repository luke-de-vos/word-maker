'''
Luke De Vos
Generate words with char ngrams and markov chains
'''

'''
TODO
add --help

'''

import random
import sys
import re
import time
from sty import fg, bg, rs

'''
FUNCTIONS ==
'''
#returns true if passed string has a non-whitespace next char in passed list
def canContinue(passKey): #(string)
	global gramD
	if passKey in gramD:
		if len(gramD[passKey]) == 1:
			if '\n' in gramD[passKey]:
				return False
		return True	
	else:
		return False

#generates gram to start generation
def getFirstGram():
	global totalStartGrams
	global startGramD
	global relFreqL
	global expectL
	r=random.random()
	cumu=0.0
	for key, value in startGramD.items():
		cumu += value/totalStartGrams
		if r < cumu:
			if iSet or cSet:
				relFreqL.append(value/totalStartGrams)
				expectL.append(relFreqL[-1] - (1/len(startGramD)))
			return key
			
#given a string of gramLen-1 characters (the 'state' of the generation),
# returns the next letter to be generated, stored in a list.
#if iSet or cSet, the above list also includes the values to append to relFreqL and expectL
def getNextChar(passKey, NN): #(string, bool)
	global gramD
	global relFreqL
	global expectL
	totalVals=0		#used to determine relative frequency
	options=len(gramD[passKey])	#used to determine relative 'expectedness'

	if NN and not canContinue(passKey):
		return False

	for val in gramD[passKey].values():
		totalVals += val

	attempts=0
	while True:
		attempts += 1
		if attempts > 10000: return False
		r=random.random()
		cumu=0
		for letter, val in gramD[passKey].items():
			cumu += val/totalVals
			if r < cumu:
				if NN and letter == '\n':
					break
				else:
					tempL=[letter]
					if iSet or cSet: 
						tempL.append(val/totalVals)
						tempL.append((val/totalVals) - (1/options))
					return tempL

#color printing
def cPrint(string):
	global expectL
	global initLen
	j=0
	for i in range(len(string) - (initLen-1)):
		#if chance[i] is positive, it is more likely than average
		c0=0
		c1=0
		if expectL[i] < 0:
			c0 = int(-expectL[i] * 6 * 255)
			if c0 > 255:
				c0 = 255
		elif expectL[i] > 0:
			c1 = int(expectL[i] * 200)
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

#prints stats detailed in iSet and used for coloring. 
def printStats():
	global relFreqL
	global expectL
	sign=''
	print(str(round(relFreqL[-1]*100, 2))+'%\t',end='')
	if expectL[-1] >= 0:
		sign = '+'
	print(sign+str(round(expectL[-1]*100, 2))+'%\t',end='')


if __name__ == '__main__':

	#VARIABLE DECLARATIONS
	trainingSet="dictionary.txt"	#file from which ngrams are drawn
	gramLen=4			#n-gram length
	startGramD={} 		#dict of char ngrams that begin words in the training set
	gramD={}			#dict of the rest of the char ngrams in the training set
	startGramL=[] 		#above dicts coverted to lists once completely written. for faster traversal
	expectL=[]			#if iSet or cSet, for each char generated, expectL appends the char's relative frequency minus the average relative frequency in the list of possible next chars
	relFreqL=[]			#if iSet, stores relative frequency of each generated char
	deadEndL=[]			#sets of letters that return False are added. used for backtracking
	totalStartGrams=0	#combined counts of all grams that begin words. used in relFreqL and expectL

	root=''		#assigned to final arg if it is a [A-Za-z] word, not a flag
				#otherwise assigned gram from a startGram list
				#serves as base from which to generate more characters
	rootState=''#final characters of root to be used as the keys in gramD
	minLen=0	#minimum length of generated word. set with -min flag
	maxLen=1000	#maximum length of generated word. set with -max flag
	waitTime=0	#time between generations if -t NUM is passed

	#bools set with flags of the same initial letter
	vSet=False	#generation is printed each time a character is generated
	cSet=False	#generated chars are highlighted red if their generation was "unusual", green if it was particularly likely
	mSet=False	#user must hit ENTER to generate next char. Ideally paired with -v
	iSet=False	#outputs two columns of extra info for most recently generated char
	tSet=False	#next character is generated each x seconds. x passed as argument following -t


	#COMMAND LINE ARGS
	if len(sys.argv) > 1:
		line=" ".join(sys.argv[1:])
		#ensure command line args fit form that will be processed correctly
		match=re.match("^((\-(min|max|n|t|r) [0-9]+)( |$)|(\-[vcmiq])( |$))*( *[a-zA-Z]+)? *$", line)
		if match == None:
			print('Invalid arguments syntax')
			sys.exit()

		#flags
		for i in range(1, len(sys.argv)):
			if sys.argv[i] == '-min':
				minLen = int(sys.argv[i+1])
			elif sys.argv[i] == '-max':
				maxLen = int(sys.argv[i+1])
			elif sys.argv[i] == '-n':
				gramLen = int(sys.argv[i+1])
			elif sys.argv[i] == '-t':
				tSet = True
				waitTime = int(sys.argv[i+1])
			elif sys.argv[i] == '-v':
				vSet = True
			elif sys.argv[i] == '-c':
				cSet = True
			elif sys.argv[i] == '-m':
				mSet = True
			elif sys.argv[i] == '-i':
				iSet = True

		#match passed root
		match = re.match("^[A-Za-z]+ *$", sys.argv[-1])
		if match != None:
			root = match.group().strip()
			root = " "+root
			rootState = root[-(gramLen-1):]
		#check root
		while (len(root) > 0 and len(root) < gramLen-1):	#not -2 because " " is added to beginning
			print("Root must be at least (" + str(gramLen-2) + ") characters long")
			print("Please re-enter: ")
			root = " "+input()
			rootState = root[-(gramLen-1):]

	print('Loading...')

	#populate startGramD and gramD 
	with open(trainingSet) as file:
		for line in file:
			line=" "+line
			for i in range(len(line)-gramLen+1): #+1 to include newline
				key = line[i:i+gramLen-1]
				valChar = line[i+gramLen-1]
				if i == 0:
					totalStartGrams += 1
					if key in startGramD:
						startGramD[key] += 1
					else:
						startGramD[key] = 1
				if key in gramD:
					if valChar in gramD[key]:
						gramD[key][valChar] += 1
					else:
						gramD[key][valChar] = 1
				else:
					gramD[key] = {}
					gramD[key][valChar] = 1

	#check that root is valid again, now with gram info
	while (len(root) > 0 and len(root) < gramLen-1) or root != '' and not canContinue(rootState):
		if (len(root) > 0 and len(root) < gramLen-1):
			print("Root must be at least (" + str(gramLen-2) + ") characters long")
		elif not canContinue(rootState):
			print("Root is never followed by a non-whitespace character")
		print("Please re-enter: ")
		root = " "+input()
		rootState = root[-(gramLen-1):]

	#GENERATION
	gen=''		#'generation'. generated characters added to gen. gen printed when complete
	NN=False	#"No Newline". passed to getNextChar() when the word should not end
	initLen=0	#length of passed root or initial gram
	print("<Hit ENTER to generate words>")

	while input() == '':
		
		if root == '': #user did not pass a root
			gen = getFirstGram()
		else:
			gen = root
			if iSet or cSet: 
				relFreqL.append(1)
				expectL.append(0)

		initLen = len(gen)

		while gen[-1] != '\n':
			if vSet or iSet or mSet or tSet: 
				if iSet:
					printStats()
				print(gen)

			if len(gen) < minLen+1:	#+1 because trailing whitespace is part of generation
				NN = True
			else:
				NN = False

			#action
			state=gen[-(gramLen-1):]
			result=getNextChar(state, NN)
			if result != False and len(gen.strip()) <= maxLen:
				gen = gen + result[0]
				if iSet or cSet:
					relFreqL.append(result[1])
					expectL.append(result[2])
			else:
				deadEndL.append(state)
				for i in range(deadEndL.count(state)):
					if len(gen) > initLen:
						gen = gen[0:-1]
						if iSet or cSet: 
							expectL.pop()
							relFreqL.pop()
					else: 
						break

			if mSet:
				input()
			if tSet:
				time.sleep(waitTime)


		#print final complete generation
		if iSet:
			printStats()

		if cSet:
			cPrint(gen)
		else:
			print(gen,end='')

		deadEndL.clear()
		expectL.clear()
		relFreqL.clear()

	print("EXIT")










	
