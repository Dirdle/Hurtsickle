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

if __name__ == "__main__":
	import animeChoose as choose
	
	testListBase = choose.convertFileLines(choose.openExisting("testCase.txt"))
	
	n = 2000

	# Alright, what's needed?
	# 1) create a large number of shuffles of the test case list
	# 2) create a hexbin plot with weight on x and position on y
	
	choose.temp = 10
	choose.gravity = 5
	choose.increment = 1
	x = []
	y = []
	for i in range (0, n):
		testList = testListBase.copy()
		
		x.extend((tasklistToTasknames(testList)))
		testList = choose.thermalShuffle(testList)
		y.extend(tasklistToTasknames(testList))

	plot.hexbin(x,y,gridsize=10,bins='log')
	#plot.axis([xmin, xmax, ymin, ymax])
	cb = plot.colorbar()
	plot.xlabel("Weight")
	plot.ylabel("Resultant position")
	plot.show()
