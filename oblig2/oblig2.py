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
printSolutionTask2(solution, actorGraph)


print('Oppg3')
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
    # prettyPrintGraph(graph)
    path_lengths = {node_id: {'dist': float('inf'), 'path': [startNodeId]} for node_id in graph}
    path_lengths[startNodeId]['dist'] = 0
    path_stack = {}
    leftToVisit = {node for node in graph}
    leftToVisit.remove(startNodeId)
    visited = {startNodeId}

    neighbours = [{"actorId": node['actorId'], "weight": 10-float(node['rating'])} for node in graph[startNodeId]['edges']]
    for neighbour in neighbours:
        if neighbour['actorId'] in path_lengths[neighbour['actorId']]['path']:
            continue
        path_lengths[neighbour['actorId']]['dist'] = neighbour['weight']
        path_stack[neighbour['actorId']]= neighbour
        path_lengths[neighbour['actorId']]['path'].append(neighbour['actorId'])
    i= 0
    while i < len(leftToVisit):
        i+=1
        pathStackList = [{"weight":path_stack[key]['weight'], "id": key} for key in path_stack]
        nextNode = min(pathStackList, key=lambda x:x['weight'])['id']
        nextNodeDist = path_lengths[nextNode]['dist']
        neighbours = [{"actorId":node['actorId'], "weight": 10-float(node['rating'])} for node in graph[nextNode]['edges']]
        for neighbour in neighbours:
            if neighbour['actorId'] in visited:
                continue
            neighbourWeight = neighbour['weight']
            if nextNodeDist+neighbourWeight < path_lengths[neighbour['actorId']]['dist']:
                path_lengths[neighbour['actorId']]['dist'] = nextNodeDist+neighbourWeight
                path_lengths[neighbour['actorId']]['path'] = list(path_lengths[nextNode]['path'])
                path_lengths[neighbour['actorId']]['path'].append(neighbour['actorId'])
            if neighbour['actorId'] == endNodeId:
                return path_lengths[neighbour['actorId']]
            path_stack[neighbour['actorId']] = neighbour
        visited.add(nextNode)
        del path_stack[nextNode]


'''
nm2255973 nm0000460 Donald Glover Jeremy Irons
nm0424060 nm0000243 Scarlett Johansson Denzel Washington
nm4689420 nm0000365 Carrie Coon Julie Delpy
nm0000288 nm0001401 Christian Bale Angelina Jolie
nm0031483 nm0931324 Atle Antonsen Michael K. Williams
'''


solution = dijkstraWeighted(actorGraph, 'nm0000001', 'nm0000006')
solution = dijkstraWeighted(actorGraph, 'nm2255973', 'nm0000460')
printSolutionTask3(solution, actorGraph)