import csv
import time
import json
import sys

print("Oppgave 1")
start = time.time()

def checkTime(startTime):
    now = time.time()
    print(now - startTime)

def countNodes(graph):
    print('Number of nodes:', len(graph))

def countEdges(graph):
    print('Number of edges:', sum(len(dct['edges']) for dct in graph.values())/2)

def prettyPrintGraph(graph):
    print(json.dumps(graph, sort_keys=True, indent=4))

short = True if (len(sys.argv)>1 and sys.argv[1]=='short') else False
actor_tsv = open("actors_short.tsv") if short else open("actors.tsv")
actors = csv.reader(actor_tsv, delimiter="\t")
movies_tsv = open("movies_short.tsv") if short else open("movies.tsv")
movies = csv.reader(movies_tsv, delimiter="\t")
actorGraph = {}

print("creating actors")
for row in actors:
    actorGraph[row[0]] = {"movies" : row[2:], "edges":[], "name":row[1]}
checkTime(start)

movieGraph = {}
print("creating movies")
for row in movies:
    movieGraph[row[0]] = {"title":row[1], "rating":row[2], "actors":[]}
checkTime(start)

print("creating movieset")
movieSet = set(movieGraph.keys())
checkTime(start)

print("Adding actors to movies")
for actor in actorGraph:
    for movie in actorGraph[actor]["movies"]:
        if movie in movieSet:
            movieGraph[movie]["actors"].append(actor)
checkTime(start)

print("Adding edges")
for key, value in movieGraph.items():
    for actor1 in value['actors']:
        for actor2 in value['actors']:
            if actor1==actor2:
                continue 
            actorGraph[actor1]["edges"].append({"actorId":actor2, "movieId":key, 'movieTitle': value['title'], "rating":value["rating"]})
checkTime(start)
countNodes(actorGraph)
countEdges(actorGraph)
if short:
    prettyPrintGraph(actorGraph)

# OPPG 2
print('Oppgave 2')
start2 = time.time()
def dijkstra(graph, startNodeId, endNodeId):
    path_lengths = {node_id: {'dist': float('inf'), 'path': [startNodeId]} for node_id in graph}
    path_lengths[startNodeId]['dist'] = 0
    path_stack = {}
    leftToVisit = {node for node in graph}
    leftToVisit.remove(startNodeId)
    visited = {startNodeId}

    neighbours = [node['actorId'] for node in graph[startNodeId]['edges']]
    for neighbour in neighbours:
        if neighbour in path_lengths[neighbour]['path']:
            continue
        path_lengths[neighbour]['dist'] = 1
        path_stack[neighbour]= 1
        path_lengths[neighbour]['path'].append(neighbour)
    i= 0
    while i < len(leftToVisit):
        i+=1
        nextNode = min(path_stack, key=path_stack.get)
        nextNodeDist = path_lengths[nextNode]['dist']
        neighbours = [node['actorId'] for node in graph[nextNode]['edges']]
        for neighbour in neighbours:
            if neighbour in visited:
                continue
            try:
                if nextNodeDist+1 < path_lengths[neighbour]['dist']:
                    path_lengths[neighbour]['dist'] = nextNodeDist+1
                    path_lengths[neighbour]['path'] = list(path_lengths[nextNode]['path'])
                    path_lengths[neighbour]['path'].append(neighbour)
                if neighbour == endNodeId:
                    return path_lengths[neighbour]
                path_stack[neighbour] = 1
            except:
                print('Nope:', neighbour)
        visited.add(nextNode)
        del path_stack[nextNode]

def printSolutionTask2(solution, graph):
    for index, actor in enumerate(solution['path']):
        if index < len(solution['path'])-1:
            commonEdges = [edge for edge in graph[actor]['edges'] if edge["actorId"] == solution['path'][index+1]][0]
            commonMovie = commonEdges['movieTitle']
            commonMovieId = [edge for edge in graph[actor]['edges'] if edge["actorId"] == solution['path'][index+1]][0]['movieId']
            print(graph[actor]['name'], '(', actor,')', 'via the movie', commonMovie, '(', commonMovieId,')', 'to', graph[solution['path'][index+1]]['name'])

# solution = dijkstra(actorGraph, 'nm0000001', 'nm0000006')
solution = dijkstra(actorGraph, 'nm0031483', 'nm0931324')
checkTime(start2)
printSolutionTask2(solution, actorGraph)


print('Oppg3')
'''
def printSolutionTask3(solution, graph):
    totalWeight = 0
    for index, actor in enumerate(solution['path']):
        if index < len(solution['path'])-1:
            commonEdges = [edge for edge in graph[actor]['edges'] if edge["actorId"] == solution['path'][index+1]]
            commonEdge = max(commonEdges, key=lambda x:x['rating'])
            commonMovie = commonEdge['movieTitle']
            commonMovieId = [edge for edge in graph[actor]['edges'] if edge["actorId"] == solution['path'][index+1]][0]['movieId']
            print(graph[actor]['name'], '(', actor,')', 'via the movie', commonMovie, '(', commonMovieId, commonEdge['rating'] ,')', 'to', graph[solution['path'][index+1]]['name'])
            totalWeight = totalWeight + (10-float(commonEdge['rating']))
    print('Total Weight:', totalWeight)


def dijkstraWeighted(graph, startNodeId, endNodeId):
    prettyPrintGraph(graph)
    path_lengths = {node: float('inf') for node in graph}
    nodeUpdatedFrom = {startNodeId:startNodeId}
    path_lengths[startNodeId] = 0
    stack = []

    neighbourEdges = graph[startNodeId]['edges']
    neighbourActors = set([node['actorId'] for node in graph[startNodeId]['edges']])

    for actorId in neighbourActors:
        actorEdges = [node for node in neighbourEdges if node['actorId'] == actorId]
        edge = max(actorEdges, key=lambda x:x['rating'])
        path_lengths[actorId] = 10 - float(edge['rating'])
        nodeUpdatedFrom[actorId] = startNodeId
        stack.append({'actorId': actorId, "weight": 10 - float(edge['rating'])})
    
    while path_lengths[endNodeId] == float('inf'):
        nextNode = min(stack, key=lambda x:x['weight'])
        nextNodeId = nextNode['actorId']
        nextNodeNeighbourEdges = graph[nextNodeId]['edges']
        neighbourActors = set([node['actorId'] for node in graph[nextNodeId]['edges']])
        for actorId in neighbourActors:
            #If actorId is where we came from, continue
            if actorId == nodeUpdatedFrom[nextNodeId]:
                continue
            actorEdges = [node for node in neighbourEdges if node['actorId'] == actorId]
            print(actorEdges )
            edge = max(actorEdges, key=lambda x:x['rating'])
            
            if (path_lengths[nextNode] + (10 - float(edge['rating']))) < path_lengths[actorId]:
                path_lengths[actorId] = path_lengths[nextNode] + (10 - float(edge['rating']))
                nodeUpdatedFrom[actorId] = nextNodeId

            stack.append({'actorId': actorId, "weight": 10 - float(edge['rating'])})
            stack[:] = [d for d in stack if d.get('actorId') != nextNodeId]

        print(nextNodeNeighbourEdges)



solution = dijkstraWeighted(actorGraph, 'nm0000001', 'nm0000006')
# solution = dijkstraWeighted(actorGraph, 'nm2255973', 'nm0000460')
def dijkstraWeighted(graph, startNodeId, endNodeId):
    # prettyPrintGraph(graph)
    path_lengths = {node_id: {'dist': float('inf'), 'path': [startNodeId]} for node_id in graph}
    path_lengths[startNodeId]['dist'] = 0
    path_stack = {}
    leftToVisit = {node for node in graph}
    leftToVisit.remove(startNodeId)
    visited = {startNodeId}

    neighbourEdges = graph[startNodeId]['edges']
    neighbourActors = set([node['actorId'] for node in graph[startNodeId]['edges']])
    neighbours = []
    for node in neighbourActors:
        relevantNodes = [stuff for stuff in neighbourEdges if stuff['actorId']==node]
        myNode = max(relevantNodes, key=lambda x:x['rating'])
        neighbours.append(myNode)

    print(neighbours)
    # print('startedgeds', graph[startNodeId]['edges'])

    # next(item for item in neighbourEdges if item["name"] == "Pam")

    for neighbour in neighbours:
        if neighbour['actorId'] in path_lengths[neighbour['actorId']]['path']:
            continue
        path_lengths[neighbour['actorId']]['dist'] = 10 - float(neighbour['rating'])
        path_stack[neighbour['actorId']]= 10-float(neighbour['rating'])
        path_lengths[neighbour['actorId']]['path'].append(neighbour['actorId'])
    i= 0
    while i < len(leftToVisit):
        i+=1
        print(path_stack)
        nextNode = min(path_stack, key=path_stack.get)
        nextNodeDist= path_stack[nextNode]
        nextNodeDist = graph[nextNode]

        neighbourEdges = graph[nextNode]['edges']
        neighbourActors = set([node['actorId'] for node in graph[startNodeId]['edges']])
        neighbours = []
        for node in neighbourActors:
            if node in path_lengths[node]['path']:
                continue
            relevantNodes = [stuff for stuff in neighbourEdges if stuff['actorId']==node]
            myNode = max(relevantNodes, key=lambda x:x['rating'])
            neighbours.append(myNode)

            for neighbour in neighbours:
                print('neighbour',neighbour)
                neighbourWeight = neighbour['weight']
                if neighbour['actorId'] in visited:
                    if nextNodeDist+neighbourWeight < path_lengths[neighbour['actorId']]['dist']:
                        path_lengths[neighbour['actorId']]['dist'] = nextNodeDist+neighbourWeight
                    continue
                if nextNodeDist+neighbourWeight < path_lengths[neighbour['actorId']]['dist']:
                    path_lengths[neighbour['actorId']]['dist'] = nextNodeDist+neighbourWeight
                    path_lengths[neighbour['actorId']]['path'] = list(path_lengths[nextNode]['path'])
                    path_lengths[neighbour['actorId']]['path'].append(neighbour['actorId'])
                if neighbour['actorId'] == endNodeId:
                    return path_lengths[neighbour['actorId']]
                path_stack[neighbour['actorId']] = neighbour
        visited.add(nextNode)
        del path_stack[nextNode]

def getBestEdges(edges):
    neighbourActors = set([node['actorId'] for node in edges])
    neighbours = []
    for node in neighbourActors:
        relevantNodes = [stuff for stuff in edges if stuff['actorId']==node]
        myNode = max(relevantNodes, key=lambda x:x['rating'])
        neighbours.append(myNode)
    return neighbours

def dijkstraWeighted(graph, startNodeId, endNodeId):
    path_lengths = {node_id: { 'dist': float('inf'), 'path': [startNodeId]} for node_id in graph}
    path_lengths[startNodeId] = 0
    stack = []
    visited = []
    
    neighbours = getBestEdges(graph[startNodeId]['edges'])
    for neighbour in neighbours:
        stack.append(neighbour)
        # add if actually shorter check for general application
        path_lengths[neighbour['actorId']]['dist'] = 10 - float(neighbour['rating'])
    visited.append(startNodeId)
    i=0
    while i<1:
        i = i+1
        nextNode = max(stack, key=lambda x:float(x['rating']))
        neighbours = getBestEdges(graph[nextNode['actorId']]['edges'])
        for neighbour in neighbours:
            if neighbour['actorId'] in visited:
                continue
            stack.append(neighbour)
            # add if actually shorter check for general application
            currentDist = path_lengths[neighbour['actorId']]['dist']
            edgeDist = 10-float(neighbour['rating'])
            if path_lengths[nextNode['actorId']]['dist'] + edgeDist < currentDist:
                path_lengths[neighbour['actorId']]['dist'] =path_lengths[nextNode['actorId']]['dist'] + 10 - float(neighbour['rating'])
        stack = [node for node in stack if node['actorId']!=nextNode['actorId'] ]

        print('STAAAACK',stack)

solution = dijkstraWeighted(actorGraph, 'nm0000001', 'nm0000006')
# solution = dijkstraWeighted(actorGraph, 'nm2255973', 'nm0000460')

# printSolutionTask3(solution, actorGraph)
'''