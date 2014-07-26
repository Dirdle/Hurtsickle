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
	
	testList = choose.convertFileLines(choose.openExisting("testCase.txt"))
	
	n = 10000

	# Alright, what's needed?
	# 1) create a large number of shuffles of the test case list
	# 2) create a hexbin plot with weight on x and position on y
	
	choose.temp = 1
	choose.gravity = 1
	choose.increment = 1
	x = []
	y = []
	for i in range (0, n):
		x.extend((tasklistToTasknames(testList)))
		testList = choose.thermalShuffle(testList)
		y.extend(tasklistToTasknames(testList))

	plot.hexbin(x,y,gridsize=20)
	#plot.axis([xmin, xmax, ymin, ymax])
	cb = plot.colorbar()
	cb.set_label('log10(N)')

	plot.show()
