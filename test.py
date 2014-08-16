#!/usr/bin/python
'''Test code for animeChoose.py'''

import numpy
import matplotlib.pyplot as plot


def tasklistToTasknames(tasklist):
	c = []
	for i in tasklist:
		c.append(i.name)
	return numpy.array(c)

def tasklistToTaskweights(tasklist):
	d = []
	for j in tasklist:
		d.append(j.weight)
	return numpy.array(d)

def massShuffleTest():
	testListBase = choose.convertFileLines(choose.openExisting("testCase.txt"))
	n = 2000

	# Alright, what's needed?
	# 1) create a large number of shuffles of the test case list
	# 2) create a hexbin plot with weight on x and position on y
	
	x = []
	y = []
	for i in range (0, n):
		testList = testListBase.copy()
		
		x.extend(tasklistToTasknames(testList))
		testList = choose.thermalShuffle(testList)
		y.extend(tasklistToTasknames(testList))

	plot.hexbin(x,y,gridsize=10,bins='log')
	#plot.axis([xmin, xmax, ymin, ymax])
	cb = plot.colorbar()
	plot.xlabel("Weight")
	plot.ylabel("Resultant position")
	plot.show()
	pass

def singleHeavyweight():
	testListBase = choose.convertFileLines(choose.openExisting("testCase2.txt"))
	length = len(testListBase)

	weights = numpy.arange(0, length)
	# Create an array of the weights. I'm tired of trying to be clever about this.
	for a in range (0, len(weights)):
		weights[a] = float(testListBase[a].weight)
	distributions = []
	for i in range (0,length):
		# Create an array of swap probabilities for i by replacing j with an array of every possible j
		
		rawDistribution = choose.findSwapProbability(i, numpy.arange(0, length), weights[i], weights)
		# Normalise the probabilities
		probabilityDist = rawDistribution/numpy.sum(rawDistribution)
		distributions.append(probabilityDist)
	x = tasklistToTasknames(testListBase)
	#l = 1
	#for curve in distributions:			
	#	plot.plot(x, curve, label=str(l))
	#	l = l + 1

	y_1 = distributions[0]
	print y_1
	y_2 = distributions[1]
	y_3 = distributions[2]
	plot.plot(x, y_1, label="1")
	plot.plot(x, y_2, label="2")
	plot.plot(x, y_3, label="3")
	plot.legend()
	plot.show()

if __name__ == "__main__":
	import animeChoose as choose
	choose.temp = 10
	choose.gravity = 1
	choose.increment = 1	
	singleHeavyweight()
	
	

