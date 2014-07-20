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
gravity	= 10
temp	= 50


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

def findSwapProbability(i,j,taskArray):
	'''Returns the (non-normalised) probability of swapping tasks i and j in given list'''
	deltaE = gravity*(i-j)*(taskArray[i].weight - taskArray[j].weight)
	return N.exp(-1*deltaE/temp)

def thermalShuffle(taskArray):
	'''Shuffle the tasks according to thermal-motion based laws. I think a good analogy
	would be a gas of particles of mixed masses at relatively low temperature, in a 
	fairly vertical container.'''	
	# Loop over the tasks:
	length = len(taskArray))
	for i in range (0, length):
		task = taskArray[i]
		# Create an array of swap probabilities for i by replacing j with an array of every possible j
		rawDistribution = findSwapProbabilities(i, N.arange(0, length, taskArray)
		# Normalise the probabilities
		probabilityDist = rawDistribution/N.sum(rawDistribution)
		
		# Choose which position i will swap to by musical chairs algorithm
		# Swapping to its own position is legitimate (and will be the most probable swap 
		# if the array is ordered)
		randomVal = random.random()
		for k in range (i, length + i):
			if randomVal <= 0:
				taskArray = swap(i, k % length, taskArray)
				return
			else:
				randomVal -= probabilityDist[k % length]


def taskSwap(i, j, taskArray):
	'''Swaps tasks i and j in the array'''
	#don't feel like avoiding using a temporary variable
	#lazy
	temp = taskArray[i]
	taskArray[i] = taskArray[j]
	taskArray[j] = temp
	return taskArray
				

if __name__ == "__main__":
	print "Starting..."
	#If there's one argument, try to open a list with that as the file name
	#Remember the argv always contains the source's 
	if len(sys.argv) == 2:
		fileLines = openExisting(sys.argv[1])
		tasks     = convertFileLines(fileLines)
		# Next:
		# For each task, generate a list of the probabilities of it swapping
		# to each position including its current one
		# Normalise that list
		# Decide on an outcome and execute that swap
	else:
		requestNewFileName()
	#TODO application logic
