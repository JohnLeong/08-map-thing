import osmnx as ox
from collections import defaultdict
import json
import math

def multi_dict(K, type):    # converting to 2d array format
    if K == 1:
        return defaultdict(type)
    else:
        return defaultdict(lambda: multi_dict(K - 1, type))

# entire map of punggol
G = ox.core.graph_from_file("map/punggol.osm", simplify=False, retain_all=True)

node_dict = {}
node_dict = multi_dict(2, float)

for node in G:
    for way, way_data in G[node].items():
        # print("Node", node, " is connected to Node", way, " with the cost of ", way_data[0]["length"])
        node_dict[node][way] = way_data[0]["length"]

new_dict = json.loads(json.dumps(node_dict))
graph = dict(new_dict)  # print(new_dict) in ensuring that it is in dictonary format

def dijkstra(graph, start, goal):   # dijkstra algorithm to set graph, start & goal
    shortest_distance = {}
    predecessor = {}
    unseenNodes = graph
    infinity = math.inf
    path = []
    for node in unseenNodes:
        shortest_distance[node] = infinity
    shortest_distance[start] = 0

    while unseenNodes:  # iterate graph to find min_distance_node
        minNode = None
        for node in unseenNodes:
            if minNode is None:
                minNode = node
            elif shortest_distance[node] < shortest_distance[minNode]:
                minNode = node

        for childNode, weight in unseenNodes[minNode].items():
            if childNode in unseenNodes:
                if weight + shortest_distance[minNode] < shortest_distance[childNode]:
                    shortest_distance[childNode] = weight + shortest_distance[minNode]
                    predecessor[childNode] = minNode
        unseenNodes.pop(minNode)  # get nodes

    currentNode = goal
    while currentNode != start:
        try:
            path.insert(0, currentNode)
            currentNode = predecessor[currentNode]
        except KeyError:
            print('Path unreachable')
            break

    path.insert(0, start)
    if shortest_distance[goal] != infinity:
        print('Shortest distance is ' + str(shortest_distance[goal]))   # find shortest distance
        print('And the path is ' + str(path))   # find path taken by the nodes

# sample of finding path and distance between nodes
#dijkstra(graph, '7246484954', '6374981557')
## TODO: get lat long relation to node id