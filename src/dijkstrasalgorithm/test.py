graph_data: dict[str, list[float]] = {
#           W   T  G2  G1    B   F
    "W":  [ 0, 10,  0,  8,   9,  0], #W
    "T":  [10,  0,  6,  0,   0,  0], #T
    "G2": [ 0,  6,  0,  0,   8, 10], #G2
    "G1": [ 8,  0,  0,  0,   6,  8], #G1
    "B":  [ 9,  0,  8,  6,   0, 12], #B
    "F":  [ 0,  0, 10,  8,  12,  0], #F
}

class Graph():
    def __init__(self, data: list[list[float]]):
       self.data = data
       self.vertices = [i for i in range(len(self.data))]
       self.size = len(self.data)

    def printSolution(self, dist):
        print("Vertex \t Distance from Source")
        for node in range(self.size):
            print(node, "\t\t", dist[node])

    def minDistance(self, dist: list[float], sptSet):
        min = 1e7
        min_index = 1e7

        for v in range(self.size):
            if dist[v] < min and sptSet[v] == False:
                min = dist[v]
                min_index = v

        return min_index

    def Dijkstra(self, src):

        dist: list[float] = [1e7] * self.size
        dist[src] = 0
        sptSet = [False] * self.size

        for cout in range(self.size):

            #Get the minimum distance vertex from unprocessed vertices
            #u is always src in first iteration
            u = int(self.minDistance(dist, sptSet))

            #Put min distance to shortest path tree
            sptSet[u] = True

            #Update the dist value for adjacent vertices if new distance
            # is shorter than current distance and vertex is not in
            # sptSet already
            for v in range(self.size):
                if (self.data[u][v] > 0 and
                    sptSet[v] == False and
                    dist[v] > dist[u] + self.data[u][v]):
                    dist[v] = dist[u] + self.data[u][v]

        self.printSolution(dist)

g = Graph(graph_data)

g.Dijkstra(0)