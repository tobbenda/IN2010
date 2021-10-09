#LOCAL MODE
file = open('oppg3/test0.in')
lines = file.readlines()

# KATTIS MODE:
# import sys
# lines = []

# for line in sys.stdin.readlines():
#     lines.append(line)

class Node:
    def __init__(self, nodeName, parent=None):
        self.nodeName = nodeName
        self.parent = parent

def findWayOut(startNode):
    currentNode = startNode
    while(currentNode.parent):
        print(currentNode.nodeName)
        currentNode = currentNode.parent
    print(currentNode.nodeName)

def getFormatedLines(lines):
    startNodeNum = None
    formated_lines  = []
    for i, line in enumerate(lines):
        if i==0:
            startNodeNum = int(line.strip())
            continue
        if '-1' in line:
            break
        digits = line.replace('\n', '').split(' ')
        formated_lines .append([int(x) for x in digits])
    return formated_lines , startNodeNum

def createTree(lines):
    nodes = []
    formated_lines ,startNodeNum = getFormatedLines(lines)
    # Oneliner for å gjøre om den nestede listen formated_lines , til en liste med alle unike nodeNavn
    allDigits = list(set([item for sublist in formated_lines  for item in sublist])) 
    for digit in allDigits:
        nodes.append(Node(digit))
    for new_line in formated_lines :
        thisParent = next(node for node in nodes if node.nodeName == new_line[0])
        for x in range(1, len(new_line)):
            thisNode = next(node for node in nodes if node.nodeName == new_line[x])
            thisNode.parent = thisParent
    return nodes, startNodeNum

def index(lines):
    nodes, startNodeNum = createTree(lines)
    startNode = next(node for node in nodes if node.nodeName == startNodeNum)  
    findWayOut(startNode)

index(lines)
