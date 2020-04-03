import math
from LLRBT import *
import heapq

class Pathfinding():
    @staticmethod
    def find_path_astar(start_node, end_node, walk_only=False):
        """ Calculates the shortest path from a start node to end node
            using Astar pathfinding
            Returns a list of MapNodes which form a path from the start to end node

        Parameters:
        start_node:     The starting MapNode
        end_node:       The destination MapNode
        walk_only:   Whether to include bus paths in the pathfinding
        """
        open_dict = {}
        closed_dict = {}

        #Clear previous pathfinding data
        start_node.reset_pathfinding_data()
        end_node.reset_pathfinding_data()

        #Add start node to open set
        open_dict[start_node.node_id] = start_node

        while (len(open_dict) > 0):
            #Get item with lowest f score
            lowest = False
            for item in open_dict.values():
                if (lowest == False):
                    lowest = item
                elif (item.g + item.h < lowest.g + lowest.h and item.h < lowest.h):
                    lowest = item
            current_node = lowest
            open_dict.pop(lowest.node_id)
            #current_node = open_dict.popitem(last=False)[1]

            #Add item to closed set
            closed_dict[current_node.node_id] = current_node

            if (current_node == end_node):
                path = []
                cur = end_node
                while(cur != start_node):
                    path.append(cur)
                    cur = cur.parent
                path.append(start_node)
                return path[::-1]

            #Get all connections to current node
            for i in range(len(current_node.connections)):
                #Check if connection is in closed set
                directed_edge = current_node.connections[i]
                weight = directed_edge[1]
                neighbor = directed_edge[0]
                #Skip if node is already in the closed set
                if (neighbor.node_id in closed_dict):
                    continue
                #Skip if walk_only is true and this directed edge is a bus service
                if (walk_only and len(directed_edge) > 2):
                    continue

                #Get the total combined path cost from start to neighbor
                new_cost_to_neighbor = current_node.g + weight
                if (new_cost_to_neighbor < neighbor.g or neighbor.node_id not in open_dict):
                    neighbor.g = new_cost_to_neighbor
                    neighbor.h = neighbor.position.real_distance_from(end_node.position)
                    neighbor.parent = current_node

                    if (neighbor.node_id not in open_dict):
                        open_dict[neighbor.node_id] = neighbor

        return []

    @staticmethod
    def find_path_astar_heap(start_node, end_node, walk_only=False):
        """ Calculates the shortest path from a start node to end node
            using Astar pathfinding
            Returns a list of MapNodes which form a path from the start to end node
            Uses a heap for the open list

        Parameters:
        start_node:     The starting MapNode
        end_node:       The destination MapNode
        walk_only:   Whether to include bus paths in the pathfinding
        """
        open_heap = []
        closed_dict = {}

        #Clear previous pathfinding data
        start_node.reset_pathfinding_data()
        end_node.reset_pathfinding_data()

        #Add start node to open set
        heapq.heappush(open_heap, start_node)

        while (len(open_heap) > 0):
            #Get item with lowest f score
            current_node = heapq.heappop(open_heap)

            #Add item to closed set
            closed_dict[current_node.node_id] = current_node

            if (current_node == end_node):
                path = []
                cur = end_node
                while(cur != start_node):
                    path.append(cur)
                    cur = cur.parent
                path.append(start_node)
                return path[::-1]

            #Get all connections to current node
            for i in range(len(current_node.connections)):
                #Check if connection is in closed set
                directed_edge = current_node.connections[i]
                weight = directed_edge[1]
                neighbor = directed_edge[0]
                #Skip if node is already in the closed set
                if (neighbor.node_id in closed_dict):
                    continue
                #Skip if walk_only is true and this directed edge is a bus service
                if (walk_only and len(directed_edge) > 2):
                    continue

                #Get the total combined path cost from start to neighbor
                new_cost_to_neighbor = current_node.g + weight
                if (new_cost_to_neighbor < neighbor.g or neighbor not in open_heap):
                    neighbor.g = new_cost_to_neighbor
                    neighbor.h = neighbor.position.real_distance_from(end_node.position)
                    neighbor.parent = current_node

                    if (neighbor not in open_heap):
                        heapq.heappush(open_heap, neighbor)

        return []

    @staticmethod
    def find_path_djikstra(start_node, end_node, walk_only=False):
        """ Calculates the shortest path from a start node to end node
            using djikstra's algorithm
            Returns a list of MapNodes which form a path from the start to end node

        Parameters:
        start_node:     The starting MapNode
        end_node:       The destination MapNode
        walk_only:   Whether to include bus paths in the pathfinding
        """
        open_dict = {}
        closed_dict = {}

        #Clear previous pathfinding data
        start_node.reset_pathfinding_data()
        end_node.reset_pathfinding_data()

        #Add start node to open set
        open_dict[start_node.node_id] = start_node

        while (len(open_dict) > 0):
            #Get item with lowest f score
            lowest = False
            for item in open_dict.values():
                if (lowest == False):
                    lowest = item
                elif (item.g < lowest.g):
                    lowest = item
            current_node = lowest
            open_dict.pop(lowest.node_id)

            #Add item to closed set
            closed_dict[current_node.node_id] = current_node

            if (current_node == end_node):
                path = []
                cur = end_node
                while(cur != start_node):
                    path.append(cur)
                    cur = cur.parent
                path.append(start_node)
                return path[::-1]

            #Get all connections to current node
            for i in range(len(current_node.connections)):
                #Check if connection is in closed set
                directed_edge = current_node.connections[i]
                weight = directed_edge[1]
                neighbor = directed_edge[0]
                #Skip if node is already in the closed set
                if (neighbor.node_id in closed_dict):
                    continue
                #Skip if walk_only is true and this directed edge is a bus service
                if (walk_only and len(directed_edge) > 2):
                    continue

                #Get the total combined path cost from start to neighbor
                new_cost_to_neighbor = current_node.g + weight
                if (new_cost_to_neighbor < neighbor.g or neighbor.node_id not in open_dict):
                    neighbor.g = new_cost_to_neighbor
                    neighbor.parent = current_node

                    if (neighbor.node_id not in open_dict):
                        open_dict[neighbor.node_id] = neighbor

        return []

    @staticmethod
    def dijkstra_old(graph, start, goal):
        """ Calculates the shortest path from a start node to end node
            using djikstra's algorithm

        Parameters:
        start:          The starting node
        goal:           The destination node
        """
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
            print('Path taken is ' + str(path))   # find path taken by the nodes
