from queue import Queue
""" Class which contains modified methods:
__init__
__hash__
__str__
__eq__ """
from Vertex import Vertex


class Graph:
    # Class which represents map
    # adjacency list with keys of vertices and values of array of neighbours
    def __init__(self):
        self.adjacency_list = {}

    # string representation of graph for testing purpose
    def __str__(self):
        result = "{ "
        for vertex in self.adjacency_list:
            result += (str(vertex) + ": [")
            for neighbor in self.adjacency_list[vertex]:
                result += (str(neighbor) + " ")
            result += "] "
        result += "}"
        return result

    # adding vertex with row i and column j in adjacency list and setting up neighbours to empty array
    def add_vertex(self, i, j):
        if not (i, j) in self.adjacency_list:
            new_vertex = Vertex(i, j)
            self.adjacency_list[new_vertex] = []

    # for vertex with row i and column j we looking for any of his four directions Cartesian
    # x and y basis if it is already inserted vertex in adjacency list
    # and if is we adding it as heighbors
    def check_for_adding_edges(self, i, j):
        combinations = [(i, j+1), (i, j-1), (i+1, j), (i-1, j)]
        # it goes through all combinations
        for combination in combinations:
            possible_neighbor = Vertex(combination[0], combination[1])
            if possible_neighbor in self.adjacency_list:
                self.add_edge(possible_neighbor, Vertex(i, j))

    #graph is undirected
    def add_edge(self, fromVertex, toVertex):
        self.adjacency_list[fromVertex].append(toVertex)
        self.adjacency_list[toVertex].append(fromVertex)

    # bfs implementation
    # result is dictionary parent where key-value pair is vertex and array of his parent
    # over which is the shortest distance from the source vertex
    def bfs(self, source):
        parent = {}
        distance = {}
        for vertex in self.adjacency_list:
            parent[vertex] = []
            # on the beginning distance from source to any other vertex is +inf
            distance[vertex] = float('inf')

        # using queue as representation of FIFO
        q = Queue(maxsize=0)
        # on the beginning only source is in the queue
        q.put(source)
        # distance from source to self is 0
        distance[source] = 0
        while(not q.empty()):
            # take first vertex from front side of queue
            u = q.get()
            # goes through all neighbours
            for v in self.adjacency_list[u]:
                # graph is unweighted, we could say that every edge is 1
                # case when distance from source to v is better over u than over previous parent
                if(distance[v] > distance[u] + 1):
                    distance[v] = distance[u] + 1
                    # push vertex v at the back of queue
                    q.put(v)
                    # update parent because over u is shortest distance from source
                    parent[v] = [u]
                # otherwise, if distance over u is equal to current distance push in parent array of u
                elif (distance[v] == distance[u] + 1):
                    parent[v].append(u)
        return parent

    # paths and path are lists
    # lists are mutable objects in python
    # on the end result will be in the paths
    # we starting from destination vertex backwards until source != destination
    # that route is in the path and that is new shortest path
    # this is some kind of modified dfs
    def all_shortest_paths(self, paths, path, parent, source, destination):
        if (destination == source):
            # currently source is not in path
            path.append(source)
            # copy by value path in paths as new list
            paths.append(path[::-1])
            path.pop()
            return

        for destination_parent in parent[destination]:
            path.append(destination)
            # recursive call for one of destination parent
            self.all_shortest_paths(paths, path, parent, source, destination_parent)
            # in the case that destination has no more parent
            path.pop()
