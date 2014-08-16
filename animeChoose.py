#!/usr/bin/python
'''animeChoose.py
An attempt to apply simulated-annealing-like methods to the 
oh-so-difficult problem of deciding which chinese girl cartoon 
to watch next.'''

import sys
import numpy as N
import random

inputText = "Please input a file name," \
			+ " or enter nothing to quit: "

gravity   = 4
temp	  = 25
increment = 0.3


class Task:
	def __init__(self, name, weight = 1):
		self.name = name
		self.weight = weight
		pass

	def __str__(self):
		return self.name + ',' + str(self.weight)

	def __repr__(self):
		return self.name

def openExisting(filePath):
	'''Opens a list from a file, assumed to already be appropriately ordered and formatted.'''
	try:	
		print "trying to open", filePath
		with open(filePath, 'r+') as listFile:
			print "Opening the file succeeded"
			# Let's just load the whole list into memory. At maybe 64 bytes per entry, you'd need thousands of 
			# chinese girl cartoons to seriously impact any respectable device.
			# First, we'll return an array of strings, each one line of the file. 
			# This will be much easier to handle than a file object etc.
			linesInFile = listFile.readlines()
			return N.array(linesInFile)
	except IOError:
		print "Something went wrong with that file."
		requestNewFileName()

def requestNewFileName():
	'''Requests a new file name from the user. '''
	newFile = raw_input(inputText)
	if newFile == "":
		quit()
	else:
		openExisting(newFile)

def convertFileLines(linesArray):
	'''Convert an array of lines from a file to an array of Task objects.
	If there are weights recorded in the file, use them; otherwise assign
	all tasks equal weight.'''
	taskList = []
	for line in linesArray:
		# remove all newline characters from the line first, then split around "," 
		# the split does nothing if there is no comma
		# if your favourite animu has a comma in the name, that's your problem		
		splitLine = line.rstrip().split(",")
		if len(splitLine) == 1 :
			# Task automatically sets weight to 1
			taskList.append(Task(splitLine[0]))
		elif len(splitLine) == 2 :
			taskList.append(Task(splitLine[0], splitLine[1]))
		else :
			print "Right now, putting commas in names is a really bad idea."
	return N.array(taskList)

def findSwapProbability(i,j,m_i, m_j):
	'''Returns the (non-normalised) probability of swapping tasks i and j in given list'''
	E_1 = (i*m_i) + (j*m_j)
	E_2 = (i*m_j) + (j*m_i)
	deltaE = gravity*(E_1 - E_2)
	return N.exp(-1*deltaE/temp)


### Code from http://stackoverflow.com/questions/3679694/a-weighted-version-of-random-choice
### As given by Ned Batchelder
### (Unused)
def weighted_choice(choices):
   total = sum(w for c, w in choices)
   r = random.uniform(0, total)
   upto = 0
   for c, w in choices:
      if upto + w > r:
         return c
      upto += w
   assert False, "Shouldn't get here"


def thermalShuffle(taskArray):
	'''Shuffle the tasks according to thermal-motion based laws. I think a good analogy
	would be a gas of particles of mixed masses at relatively low temperature, in a 
	fairly vertical container.'''	
	# Loop over the tasks:
	length  = len(taskArray)
	weights = numpy.arange(0, length)
	# Create an array of the weights. I'm tired of trying to be clever about this.
	for a in range (0, len(weights)):
		weights[a] = int(testListBase[a].weight)
	for i in range (0, length):
		# Create an array of swap probabilities for i by replacing j with an array of every possible j
		
		rawDistribution = findSwapProbability(i, N.arange(0, length), weights[i], weights)
		# Normalise the probabilities
		probabilityDist = rawDistribution/N.sum(rawDistribution)
		# Choose which position i will swap to by musical chairs algorithm
		# Swapping to its own position is legitimate (and will be the most probable swap 
		# if the array is ordered)
		randomVal = random.random()
		k = 0
		while ((randomVal - probabilityDist[k]) > 0):
			randomVal -= probabilityDist[k]
			k = (k+1) % (length)
		taskArray = taskSwap(i, k, taskArray)		
	return taskArray

def taskSwap(i, j, taskArray):
	'''Swaps tasks i and j in the array'''
	#don't feel like avoiding using a temporary variable
	#lazy
	temp = taskArray[i]
	taskArray[i] = taskArray[j]
	taskArray[j] = temp
	return taskArray

def getUserChoice(shuffledTasks):
	'''Permits the user to choose their favourite of the top three; 
	the other two have their weight increased'''
	choice = input( "Please select the task you'll perform: " + '\n' +
	"1. " + repr(shuffledTasks[0])  + '\n' +
	"2. " + repr(shuffledTasks[1])  + '\n' +
	"3. " + repr(shuffledTasks[2]))
	taskSwap(0, choice - 1, shuffledTasks)
	print "You have selected " + repr(shuffledTasks[0])
	shuffledTasks[1].weight = int(shuffledTasks[1].weight) + increment
	shuffledTasks[2].weight = int(shuffledTasks[2].weight) + increment
	return shuffledTasks[1:]

def writeOutputToFile(outputTasks, filePath):
	'''Write the tasklist back to the file, deleting any current contents of said file'''
	with open(filePath, 'r+') as listFile:
		outputText = ""
		for task in outputTasks:
			taskline = str(task)
			outputText += taskline
			outputText += '\n'
		listFile.write(outputText)
		listFile.truncate()
	pass	


if __name__ == "__main__":
	print "Starting..."
	#If there's one argument, try to open a list with that as the file name
	#Remember the argv always contains the source's 
	if len(sys.argv) == 2:
		fileLines = openExisting(sys.argv[1])
		tasks     = convertFileLines(fileLines)
		shuffled  = thermalShuffle(tasks)
		tasks = getUserChoice(shuffled)
		writeOutputToFile(tasks, sys.argv[1])
	else:
		requestNewFileName()
