#!/usr/bin/python
'''animeChoose.py
An attempt to apply simulated-annealing-like methods to the 
oh-so-difficult problem of deciding which chinese girl cartoon 
to watch next.'''

import sys
import numpy as N

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

def findSwapProbability(i,j,taskList):
	'''Returns the (non-normalised) probability of swapping tasks i and j in the given list'''
	deltaE = gravity*(i-j)*(taskList[i].weight - taskList[j].weight)
	return N.exp(-1*deltaE/temp)

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
