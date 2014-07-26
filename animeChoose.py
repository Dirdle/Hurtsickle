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

gravity   = 10
temp	  = 10
increment = 1


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
		splitLine = line.split(",")
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
	deltaE = gravity*(i-j)*(m_i - m_j)
	return N.exp(-1*deltaE/temp)

def thermalShuffle(taskArray):
	'''Shuffle the tasks according to thermal-motion based laws. I think a good analogy
	would be a gas of particles of mixed masses at relatively low temperature, in a 
	fairly vertical container.'''	
	# Loop over the tasks:
	length  = len(taskArray)
	weights = N.arange(0, length)
	# Create an array of the weights. I'm tired of trying to be clever about this.
	for a in weights:
		a = taskArray[a].weight

	for i in range (0, length):
		# Create an array of swap probabilities for i by replacing j with an array of every possible j
		
		rawDistribution = findSwapProbability(i, N.arange(0, length), weights[i], weights)
		# Normalise the probabilities
		probabilityDist = rawDistribution/N.sum(rawDistribution)
		
		# Choose which position i will swap to by musical chairs algorithm
		# Swapping to its own position is legitimate (and will be the most probable swap 
		# if the array is ordered)
		randomVal = random.random()
		for k in range (i, length + i):
			if randomVal <= 0:
				taskArray = taskSwap(i, k % length, taskArray)
				pass
			else:
				randomVal -= probabilityDist[k % length]
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
	taskSwap(0, choice - 1)
	print "You have selected " + repr(shuffledTasks[0])
	shuffledTasks[1].weight += 1
	shuffledTasks[2].weight += 1
	return shuffledTasks[1:]


if __name__ == "__main__":
	print "Starting..."
	#If there's one argument, try to open a list with that as the file name
	#Remember the argv always contains the source's 
	if len(sys.argv) == 2:
		fileLines = openExisting(sys.argv[1])
		tasks     = convertFileLines(fileLines)
		shuffled  = thermalShuffle(tasks)
		tasks = getUserChoice(shuffled)
	else:
		requestNewFileName()
