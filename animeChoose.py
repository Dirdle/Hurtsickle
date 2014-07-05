#!/usr/bin/python
'''animeChoose.py
An attempt to apply simulated-annealing-like methods to the 
oh-so-difficult problem of deciding which chinese girl cartoon 
to watch next.'''

import sys

inputText = "Please input a different file name," \
			+ " or enter nothing to quit: "

def openExisting(List):
	'''Opens a list, assumed to already be appropriately ordered.'''
	try:	
		print "trying to open ", List
		with open(List, 'r+') as listFile:
			print "Opening the file succeeded"
			#TODO decide whether to load the whole list into memory or not.
			pass
		
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

if __name__ == "__main__":
	print "Starting..."
	#If there's one argument, try to open a list with that as the file name
	#Remember the argv always contains the source's 
	if len(sys.argv) == 2:
		openExisting(sys.argv[1])
	else:
		requestNewFileName()
	#TODO application logic
