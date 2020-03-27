import math

class Pathfinding():
    @staticmethod
    def find_path_astar(start_node, end_node):
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
                elif (item.f < lowest.f):
                    lowest = item
            current_node = lowest
            open_dict.pop(lowest.node_id)
            #current_node = open_dict.popitem(last=False)[1]

            #Add item to closed set
            closed_dict[current_node.node_id] = current_node

            if (current_node == end_node):
                print("Astart path found")
                path = []
                cur = end_node
                while(cur != start_node):
                    path.append(cur)
                    cur = cur.parent
                path.append(start_node)
                return path

            #Get all connections to current node
            for i in range(len(current_node.connections)):
                #Check if connection is in closed set
                directed_edge = current_node.connections[i]
                weight = directed_edge[1]
                neighbor = directed_edge[0]
                if (neighbor.node_id in closed_dict):
                    continue

                new_cost_to_neighbor = current_node.g + weight
                if (new_cost_to_neighbor < neighbor.g or neighbor.node_id not in open_dict):
                    neighbor.g = new_cost_to_neighbor
                    neighbor.h = neighbor.position.distance_from_sqr(end_node.position)
                    neighbor.parent = current_node

                    if (neighbor.node_id not in open_dict):
                        open_dict[neighbor.node_id] = neighbor

        print("Path not found")
        return []

    @staticmethod
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
            print('Path taken is ' + str(path))   # find path taken by the nodes
