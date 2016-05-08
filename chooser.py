"""chooser.py.

An attempt to apply simulated-annealing-like methods to the
oh-so-difficult problem of deciding which chinese girl cartoon
to watch next.
"""

import numpy as N
import random
import argparse as A

inputText = "Please input a file name, or enter nothing to quit: "

gravity = 4
temp = 22
increment = 0.6


class Task:
    """Class to represent a task to be performed.

    Who are we kidding, these are cartoons and other crap. If you need a
    program to thermally shuffle your actual priorities, you should probably
    get help of a kind I'm not qualified to provide.
    """

    def __init__(self, name, weight=6):
        """Create a task.

        Higher weight = lower priority/desirability.
        """
        self.name = name
        self.weight = weight
        pass

    def __str__(self):
        """Create a string containing the name and weight, with a comma."""
        return self.name + ',' + str(self.weight)

    def __repr__(self):
        """Create a string containing the name."""
        return self.name


def openExisting(filePath):
    """Open a list from a file, assumed to already be ordered and formatted."""
    try:
        print("trying to open", filePath)
        with open(filePath, 'r+') as listFile:
            if args.verbose:
                print("Opening the file succeeded")
            # Let's just load the whole list into memory. At maybe 64 bytes per
            # entry, you'd need thousands of
            # chinese girl cartoons to seriously impact any respectable device.
            # First we'll return an array of strings, each one line of the file
            # This will be much easier to handle than a file object etc.
            return N.array([l for l in listFile])
    except IOError:
        print("Something went wrong with that file.")
        requestNewFileName()


def requestNewFileName():
    """Request a new file name from the user."""
    newFile = input(inputText)
    if newFile == "":
        return None
    else:
        return openExisting(newFile)


def convertFileLines(linesArray):
    """Convert an array of lines from a file to an array of Task objects.

    If there are weights recorded in the file, use them; otherwise assign
    all tasks equal weight.
    """
    taskList = []
    for line in linesArray:
        # remove all newline characters from the line first, then split around
        # ","
        # The split does nothing if there is no comma
        # If your favourite animu has a comma in the name, that's your problem
        splitLine = line.rstrip().split(",")
        if len(splitLine) == 1:
            # Task automatically sets weight to 1
            taskList.append(Task(splitLine[0]))
        elif len(splitLine) == 2:
            taskList.append(Task(splitLine[0], splitLine[1]))
        else:
            print("Right now, putting commas in names is a really bad idea.")
    if args.verbose:
        print("Converted lines to array of tasks successfully.")
    return N.array(taskList)


def findSwapProbability(i, j, m_i, m_j):
    """Find the non-normalised probability of swapping tasks i and j."""
    E_1 = (i*m_i) + (j*m_j)
    E_2 = (i*m_j) + (j*m_i)
    deltaE = gravity*(E_1 - E_2)
    return N.exp(-1*deltaE/temp)


def thermalShuffle(taskArray):
    """Shuffle the tasks according to thermal-motion based laws.

    I think a good analogy would be a gas of particles of mixed masses at
    relatively low temperature, in a vertical container.
    """
    # Loop over the tasks:
    if args.verbose:
        print("Shuffling the list of tasks...")
    length = len(taskArray)
    weights = N.arange(0, length)
    # Create an array of the weights.
    # I'm tired of trying to be clever about this.
    for a in range(0, len(weights)):
        weights[a] = float(taskArray[a].weight)
    for i in range(0, length):
        # Create an array of swap probabilities for i by replacing j with an
        # array of every possible j

        rawDistribution = findSwapProbability(i,
                                              N.arange(0, length),
                                              weights[i],
                                              weights)
        # Normalise the probabilities
        probabilityDist = rawDistribution/N.sum(rawDistribution)
        # Choose which position i will swap to by musical chairs algorithm
        # Swapping to its own position is legitimate
        # (and will be the most probable swap if the array is ordered)
        randomVal = random.random()
        k = 0
        while ((randomVal - probabilityDist[k]) > 0):
            randomVal -= probabilityDist[k]
            k = (k+1) % (length)
        taskArray = taskSwap(i, k, taskArray)
    return taskArray


def taskSwap(i, j, taskArray):
    """Swaps tasks i and j in the array"""
    # Don't feel like avoiding using a temporary variable
    temp = taskArray[i]
    taskArray[i] = taskArray[j]
    taskArray[j] = temp
    return taskArray


def getUserChoice(shuffledTasks):
    """Permit the user to choose their favourite of the top three.

    The other two have their weight increased.
    """
    choice = input("Please select the task you'll perform,\
                   or enter nothing to exit: " + '\n' + "1. " +
                   repr(shuffledTasks[0]) + '\n' +
                   "2. " + repr(shuffledTasks[1]) + '\n' +
                   "3. " + repr(shuffledTasks[2]) + '\n')
    if choice in ['1', '2', '3']:
        taskSwap(0, int(choice) - 1, shuffledTasks)
        print("You have selected " + repr(shuffledTasks[0]))
        shuffledTasks[1].weight = float(shuffledTasks[1].weight) + increment
        shuffledTasks[2].weight = float(shuffledTasks[2].weight) + increment
        return shuffledTasks[1:]
    else:
        return None


def writeOutputToFile(outputTasks, filePath):
    """Write the tasklist back to the file, deleting any contents of file."""
    if args.verbose:
        print("Rewriting file in new order...")
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
    parser = A.ArgumentParser()
    # Let's add some better command-line functionality
    parser.add_argument("-f", "--file", help="The file of possible tasks.")
    parser.add_argument("-v", "--verbose", action="store_true",
                        help="Output extra information")
    args = parser.parse_args()
    if args.verbose:
        print("Starting...")
    # If there's one argument, try to open a list with that as the file name
    # Remember the argv always contains the source's
    if args.file:
        fileLines = openExisting(args.file)
    else:
        fileLines = requestNewFileName()
    if fileLines is not None:
        tasks = convertFileLines(fileLines)
        shuffled = thermalShuffle(tasks)
        tasks = getUserChoice(shuffled)
        if tasks is not None:
            writeOutputToFile(tasks, args.file)
