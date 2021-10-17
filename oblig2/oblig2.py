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
    actorGraph[row[0]] = {"movies" : row[2:], "edges":[]}
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
            actorGraph[actor1]["edges"].append({"actorId":actor2, "movieid":movie, "rating":value["rating"]})
checkTime(start)
countNodes(actorGraph)
countEdges(actorGraph)
if short:
    prettyPrintGraph(actorGraph)


# OPPG 2
print('Oppgave 2')
def dijkstra(graph, startNodeId, endNodeId):
    path_lengths = {node_id: float('inf') for node_id in graph}
    path_lengths[startNodeId] = 0
    path_stack = {}
    leftToVisit = {node for node in graph}
    leftToVisit.remove(startNodeId)
    visited = {startNodeId}

    neighbours = [node['actorId'] for node in graph[startNodeId]['edges']]
    for neighbour in neighbours:
        path_lengths[neighbour] = 1
        path_stack[neighbour]= 1
    i= 0
    while i < len(leftToVisit):
        i+=1
        nextNode = min(path_stack, key=path_stack.get)
        nextNodeDist = path_lengths[nextNode]
        neighbours = [node['actorId'] for node in graph[nextNode]['edges']]
        for neighbour in neighbours:
            if neighbour in visited:
                continue
            try:
                path_lengths[neighbour] = min(nextNodeDist+1, path_lengths[neighbour])
                if neighbour == endNodeId:
                    print(neighbour, path_lengths[neighbour])
                    return ''
                path_stack[neighbour] = 1
            except:
                print('Nope:', neighbour)
        print('AFTER path_lengths',path_lengths)
        visited.add(nextNode)
        del path_stack[nextNode]


dijkstra(actorGraph, 'nm0000001', 'nm0000006')