# -*- coding: UTF-8 -*-
# !/usr/bin/env python2

import sys
import copy

sys.path.append("/System/Library/Frameworks/Python.framework/Versions/2.7/Extras/lib/python")
import numpy as np
import time

matrixLength = 0
numberOfPoliceOfficers = 0
numberOfScooters = 0
numpyFrequency = []
rowLookUp = []
columnLookUp = []
slashLookUp = []
backSlashLookUp = []
sortedFrequencyLength = 0
maximumValue = 0
currentMaximum = 0
noOfQueens = 0
globalValue = 0
isMaximumFound = 0


def main():
    readData()
    initialization()
    solvePoliceOfficers()


def solvePoliceOfficers():
    global board, slashCode, backslashCode, rowLookUp, slashLookUp, backSlashLookUp, columnLookUp, globalValue, noOfQueens, maximumValue
    board = np.zeros((matrixLength, matrixLength))
    sortedFrequencyIndex = 0

    while (sortedFrequencyIndex < sortedFrequencyLength):
        print(sortedFrequencyIndex)
        solvePoliceOfficersUtil(sortedFrequencyIndex)
        sortedFrequencyIndex = sortedFrequencyIndex + 1
        if (maximumValue >= (noOfQueens * globalValue)):
            break
        initBranchBound()
    return 1


def isSafe(row, col):
    global globalValue, noOfQueens, maximumValue, currentMaximum, sortedFrequency
    # print(globalValue)

    if ((time.time() - start_time) == 150):
        print("aadsadas")

    if (maximumValue >= (currentMaximum + (noOfQueens * globalValue))):
        return 0

    if (backSlashLookUp[int(backslashCode[int(row)][int(col)])] or slashLookUp[int(slashCode[int(row)][int(col)])] or
            rowLookUp[int(row)] or columnLookUp[int(col)]):
        return 0

    return 1


def solvePoliceOfficersUtil(sortedFrequencyIndex):
    global maximumValue, currentMaximum, sortedFrequency, noOfQueens, backSlashLookUp, slashLookUp, rowLookUp, columnLookUp, globalValue, isMaximumFound

    if (noOfQueens == 0):
        isMaximumFound = 1

        # print(currentMaximum)
        # if(time.time() > start_time + 120):
        # print("sasasasasasa")
        if (maximumValue < currentMaximum):
            maximumValue = currentMaximum
            # print(currentMaximum)
            print(maximumValue)

        return

    for i in range(sortedFrequencyIndex, sortedFrequencyLength):
        row = sortedFrequency[i][1]
        col = sortedFrequency[i][0]
        value = sortedFrequency[i][2]
        globalValue = int(value)

        if (noOfQueens == 2):
            isMaximumFound = 0

        if (isMaximumFound == 1):
            return
        if (isSafe(row, col)):
            currentMaximum = currentMaximum + value
            # print(currentMaximum)
            rowLookUp[row] = bool(1)
            columnLookUp[col] = bool(1)
            backSlashLookUp[int(backslashCode[int(row)][int(col)])] = bool(1)
            slashLookUp[int(slashCode[int(row)][int(col)])] = bool(1)
            noOfQueens = noOfQueens - 1
            print str(row) + " , " + str(col) + " , " + str(value) +"  -Placed:"+ str(noOfQueens)

            if (solvePoliceOfficersUtil(i + 1)):
                return 1

            currentMaximum = currentMaximum - value
            rowLookUp[row] = bool(0)
            columnLookUp[col] = bool(0)
            backSlashLookUp[int(backslashCode[int(row)][int(col)])] = bool(0)
            slashLookUp[int(slashCode[int(row)][int(col)])] = bool(0)
            noOfQueens = noOfQueens + 1
            print "- " + str(row) + " , " + str(col) + " , " + str(value) +"  -Placed:"+ str(noOfQueens)


def initialization():
    global sortedFrequencyLength, sortedFrequency
    dtype = [('i', int), ('j', int), ('frequency', int)]
    tempSortedFrequency = np.array(numpyFrequency, dtype=dtype)
    # print(tempSortedFrequency)
    sortedFrequency = np.sort(tempSortedFrequency, order='frequency')
    # print(sortedFrequency)
    sortedFrequency = sortedFrequency[::-1]
    # print(sortedFrequency)
    sortedFrequencyLength = len(sortedFrequency)
    # print(sortedFrequencyLength)

    initBranchBound()


def initBranchBound():
    global backslashCode, slashCode, backSlashLookUp, slashLookUp, rowLookUp, columnLookUp
    rowLookUp = np.zeros(matrixLength, dtype=bool)
    columnLookUp = np.zeros(matrixLength, dtype=bool)
    slashLookUp = np.zeros((2 * matrixLength - 1), dtype=bool)
    backSlashLookUp = np.zeros((2 * matrixLength - 1), dtype=bool)

    slashCode = np.zeros((matrixLength, matrixLength))
    backslashCode = np.zeros((matrixLength, matrixLength))

    for i in range(0, matrixLength):
        for j in range(0, matrixLength):
            slashCode[i][j] = i + j
            backslashCode[i][j] = i - j + (matrixLength - 1)

    # print(slashCode)
    # print(backslashCode)


def readData():
    global matrixLength, numberOfPoliceOfficers, numberOfScooters, numpyFrequency, frequencyOfScooters, matrixLength, noOfQueens
    lineNumber = 0
    with open("/Users/parth/Desktop/input3.txt", 'r') as my_file:
        for line in my_file:
            if (lineNumber == 0):
                matrixLength = int(line)
                lineNumber = lineNumber + 1
                frequencyOfScooters = np.zeros((matrixLength, matrixLength))
            elif (lineNumber == 1):
                numberOfPoliceOfficers = int(line)
                noOfQueens = numberOfPoliceOfficers
                lineNumber = lineNumber + 1
            elif (lineNumber == 2):
                numberOfScooters = line
                lineNumber = lineNumber + 1
            else:
                tokens = line.strip().split(",")
                # print(tokens)
                frequencyOfScooters[int(tokens[1])][int(tokens[0])] = frequencyOfScooters[int(tokens[1])][
                                                                          int(tokens[0])] + 1

    for i in range(0, matrixLength):
        for j in range(0, matrixLength):
            tempList = (j, i, frequencyOfScooters[i][j])
            numpyFrequency.append(tempList)

    # print(numpyFrequency)
    # print(matrixLength)
    # print(frequencyOfScooters)


if __name__ == '__main__':
    start_time = time.time()
    main()
    print("--- %s seconds ---" % (time.time() - start_time))