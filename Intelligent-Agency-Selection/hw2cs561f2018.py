from ast import literal_eval
import sys
import collections
from numpy import inf
import numpy as np
import time

count = 1
depth = 2
maxCount = 2


class CreateNodes:
    def __init__(self, nodeName, nodeValue=0, nodeParent=None, nodeLahsaScore=0, nodeSplaScore=0,
                 nodeSplaConfig=None, nodeLahsaConfig=None):
        self.nodeName = nodeName  # applicant number
        self.nodeValue = nodeSplaScore - nodeLahsaScore  # value of node
        self.nodeParent = nodeParent  # parent of node
        self.nodeChildren = []  # array of children nodes
        self.nodeLahsaScore = nodeLahsaScore
        self.nodeSplaScore = nodeSplaScore
        self.nodeLahsaConfig = nodeLahsaConfig
        self.nodeSplaConfig = nodeSplaConfig

    def insertChild(self, node):
        self.nodeChildren.append(node)


class GenerateTree:
    def __init__(self, splaGlobalPool, lahsaGlobalPool):
        self.root = None
        self.turn = "SPLA"
        self.splaGlobalPool = splaGlobalPool.copy()
        self.lahsaGlobalPool = lahsaGlobalPool.copy()

    def createTree(self, splaProbablePool, lahsaProbablePool, splaConfig, lahsaConfig, depth):
        global splaChosenConfig, lahsaChosenConfig, t1
        self.root = CreateNodes("ROOT", nodeSplaConfig=splaConfig, nodeLahsaConfig=lahsaConfig,
                                nodeSplaScore=splaChosenEfficiency, nodeLahsaScore=lahsaChosenEfficiency)
        self.turn = "SPLA"
        list_of_nodes = splaProbablePool.copy()
        for node in list_of_nodes:
            # print node
            self.create_inner_tree(node, self.root, splaProbablePool.copy(), lahsaProbablePool.copy(), depth, self.turn)

    def create_inner_tree(self, name, parent, splaProbablePool, lahsaProbablePool, depth, turn):
        global count, probableLAHSA, probableSPLA, noOfBedsinShelter, noOfSpacesinParking, maxCount, t1
        if ((time.time() - t1) > 176):
            raise Exception(time.time() - t1)
        lScore = parent.nodeLahsaScore
        sScore = parent.nodeSplaScore
        lConfig = parent.nodeLahsaConfig
        sConfig = parent.nodeSplaConfig
        if name != "-1":
            if turn == "LAHSA":
                currentConfig = probableLAHSA[name][0]
                currentScore = sum(list(map(int, currentConfig)))
            elif turn == "SPLA":
                currentConfig = probableSPLA[name][0]
                currentScore = sum(list(map(int, currentConfig)))
        else:
            currentConfig = "0000000"
            currentScore = 0

        if turn == "SPLA":
            sScore = sScore + currentScore
            sConfig = np.add(sConfig, list(map(int, currentConfig)))
            nSelected = turn

            splaProbablePool.pop(name, None)
            if name in lahsaProbablePool:
                lahsaProbablePool.pop(name)
            dataList = lahsaProbablePool.copy()
            turn = "LAHSA"

        elif turn == "LAHSA":
            lScore = lScore + currentScore
            lConfig = np.add(lConfig, list(map(int, currentConfig)))
            nSelected = turn

            lahsaProbablePool.pop(name, None)
            if name in splaProbablePool:
                splaProbablePool.pop(name)
            dataList = splaProbablePool.copy()
            turn = "SPLA"

        tnode = CreateNodes(name, nodeLahsaConfig=lConfig, nodeSplaConfig=sConfig, nodeLahsaScore=lScore,
                            nodeSplaScore=sScore)

        if nSelected == "SPLA":
            temp = max(tnode.nodeSplaConfig)
            temp1 = int(noOfSpacesinParking)
            if (temp > temp1):
                del tnode
                # print "delete return"
                return

        if nSelected == "LAHSA":
            temp = max(tnode.nodeLahsaConfig)
            temp1 = int(noOfBedsinShelter)
            if (temp > temp1):
                del tnode
                # print "delete return"
                return

        count += 1
        # print "count",count
        if count > maxCount:
            maxCount = count

        if count > depth:
            count -= 1
            # print "depth return"
            # print "count", count
            return

        tnode.nodeParent = parent
        parent.insertChild(tnode)

        if (len(lahsaProbablePool) == 0 and len(splaProbablePool) > 0 and nSelected == "SPLA"):
            dataList["-1"] = "-1"

        dataList = dataList.copy()
        for node in dataList:
            # print node
            self.create_inner_tree(node, tnode, splaProbablePool.copy(), lahsaProbablePool.copy(), depth, turn)

        # print "return"
        if name in probableLAHSA:
            lahsaProbablePool[name] = probableLAHSA[name]
        if name in probableSPLA:
            splaProbablePool[name] = probableSPLA[name]
        count -= 1
        # print "count", count

        return


class MinMax:
    def __init__(self, mmtree):
        self.mmtree = mmtree
        self.mmroot = mmtree.root

    def find_min_max(self, node):
        currentBestValue = -inf
        betaValue = inf

        successorNodes = node.nodeChildren
        bestPath = None
        for successor in successorNodes:
            val = self.findMin(successor, currentBestValue, betaValue)
            if val > currentBestValue:
                currentBestValue = val
                bestPath = successor
        print "AlphaBeta:  Utility Value of Root Node: = " + str(currentBestValue)
        print "AlphaBeta:  Best State is: " + bestPath.nodeName + "\n"
        return bestPath

    # def fetchSuccessorNodes(self,node):
    #     assert node is not None
    #     return node.nodeChildren

    def findMin(self, node, alphaValue, betaValue):
        # print "AlphaBeta-->MIN: Visited Node :: " + node.nodeName
        if (len(node.nodeChildren) == 0):
            return node.nodeValue
        val = inf

        successorNodes = node.nodeChildren
        for successor in successorNodes:
            val = min(val, self.findMax(successor, alphaValue, betaValue))
            if (alphaValue >= val):
                return val
            betaValue = min(betaValue, val)
        return val

    def findMax(self, node, alphaValue, betaValue):
        print "AlphaBeta-->MAX: Visited Node :: " + node.nodeName
        if (len(node.nodeChildren) == 0):
            return node.nodeValue
        val = -inf
        successorNodes = node.nodeChildren
        for successor in successorNodes:
            val = max(val, self.findMin(successor, alphaValue, betaValue))
            if (val >= betaValue):
                return val
            alphaValue = max(alphaValue, val)
        return val

    # def isTerminal(self, node):
    #     assert node is not None
    #     return len(node.nodeChildren) == 0
    #
    # def getUtility(self, node):
    #     assert node is not None
    #     return node.nodeValue


noOfBedsinShelter = 0
noOfSpacesinParking = 0
noOfLAHSA = 0
noOfSPLA = 0
totalNoOfApplicants = 0
SPLAChosen = {}
LAHSAChosen = {}
probableSPLA = collections.OrderedDict()
probableLAHSA = collections.OrderedDict()
splaChosenConfig = [0, 0, 0, 0, 0, 0, 0]
lahsaChosenConfig = [0, 0, 0, 0, 0, 0, 0]
splaChosenEfficiency = 0
lahsaChosenEfficiency = 0


def parseFile():
    global noOfBedsinShelter, noOfSpacesinParking, noOfLAHSA, noOfSPLA, totalNoOfApplicants, SPLAChosen, LAHSAChosen, probableLAHSA, probableSPLA, splaChosenEfficiency, splaChosenConfig, lahsaChosenEfficiency, lahsaChosenConfig
    f = open("/Users/parth/Desktop/USC/AI/Assignment2/input1.txt")
    lines = f.readlines()
    lines = map(lambda each: each.strip("\r\n"), lines)
    # print(lines)
    noOfBedsinShelter = lines[0]
    # print(noOfBedsinShelter)
    noOfSpacesinParking = lines[1]
    # print(noOfSpacesinParking)
    noOfLAHSA = lines[2]
    # print (noOfLAHSA)
    j = 3
    for i in range(j, j + int(noOfLAHSA)):
        # print lines[i]
        LAHSAChosen[lines[i]] = 1
    j = j + int(noOfLAHSA)
    noOfSPLA = lines[j]
    # print(noOfSPLA)
    j = j + 1
    for i in range(j, j + int(noOfSPLA)):
        # print(lines[i])
        SPLAChosen[lines[i]] = 1
    j = j + int(noOfSPLA)
    totalNoOfApplicants = lines[j]
    j = j + 1
    for i in range(j, j + int(totalNoOfApplicants)):
        # print lines[i]
        id = lines[i][0:5]
        gender = lines[i][5]
        age = lines[i][6:9]
        pets = lines[i][9]
        medicalCondition = lines[i][10]
        car = lines[i][11]
        drivingLicense = lines[i][12]
        daysRequested = lines[i][13:20]
        daysRequestedList = list(map(int, daysRequested))
        efficiency = sum(daysRequestedList)

        if (car == 'Y' and drivingLicense == 'Y' and medicalCondition == 'N'):
            if id in SPLAChosen:
                SPLAChosen[id] = (daysRequested, efficiency)
                splaChosenEfficiency += efficiency
                splaChosenConfig = np.add(splaChosenConfig, daysRequestedList)
            else:
                if id not in LAHSAChosen:
                    if (max(daysRequestedList) <= noOfSpacesinParking):
                        probableSPLA[id] = (daysRequested, efficiency)

        if (age > 17 and pets == "N" and gender == 'F'):
            if id in LAHSAChosen:
                LAHSAChosen[id] = (daysRequested, efficiency)
                lahsaChosenEfficiency += efficiency
                lahsaChosenConfig = np.add(lahsaChosenConfig, daysRequestedList)
            else:
                if id not in SPLAChosen:
                    if (max(daysRequestedList) <= noOfBedsinShelter):
                        probableLAHSA[id] = (daysRequested, efficiency)
    if len(probableSPLA) == 0:
        print "Not Valid Input"
        writeFile("output.txt", "No Valid applicant found for SPLA")
        sys.exit(0)
        # print(id)
        # print(gender)
        # print(age)
        # print pets
        # print medicalCondition
        # print car
        # print drivingLicense
        # print daysRequested
    f.close()


def main():
    global maxCount, depth, t1
    # data_list = literal_eval("['A', ['B', ('D', 3), ('E', 5)], ['C', ['F', ['I',('K',0), ('L', 7)],('J',5)], ['G', ('M',7), ('N',8)], ('H',4)]]")
    # data_tree = GenerateTree()
    # data_tree.createTree(data_list)
    # a = MinMax(data_tree)
    # a.find_min_max(a.mmroot)
    t1 = time.time()
    parseFile()
    depth = 2
    while maxCount == depth:
        try:
            gameTree = GenerateTree(splaGlobalPool=probableSPLA.copy(), lahsaGlobalPool=probableLAHSA.copy())
            gameTree.createTree(probableSPLA.copy(), probableLAHSA.copy(), splaChosenConfig, lahsaChosenConfig, depth)
            depth = depth + 1
            if ((time.time() - t1) > 176):
                raise Exception(time.time() - t1)
            a = MinMax(gameTree)
            b = a.find_min_max(a.mmroot)
            # print "depth", depth
            # print (time.time() - t1)
            writeFile("output.txt", b.nodeName)
            del gameTree
            del a
            del b
            if ((time.time() - t1) > 176):
                break
        except Exception as e:
            print e.message
            sys.exit(0)

    # print b.nodeLahsaScore
    # print b.nodeSplaScore
    # print SPLAChosen
    # print LAHSAChosen
    # print probableSPLA
    # print probableLAHSA
    # print splaChosenConfig
    # print lahsaChosenConfig
    # print splaChosenEfficiency
    # print lahsaChosenEfficiency
    # print "9"
    print "time", time.time() - t1


def writeFile(file_name, d):
    with open(file_name, "w") as f:
        f.write(str(d))


if __name__ == "__main__":
    main()
