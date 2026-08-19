from manim import * # type: ignore

graph_data: dict[str, dict[str, float]] = {
    "W":  { "W": 0,   "T": 10,  "G2": 0,   "G1": 8,   "B": 9,   "F": 0},
    "T":  { "W": 10,  "T": 0,   "G2": 6,   "G1": 0,   "B": 0,   "F": 0},
    "G2": { "W": 0,   "T": 6,   "G2": 0,   "G1": 0,   "B": 8,   "F": 10},
    "G1": { "W": 8,   "T": 0,   "G2": 0,   "G1": 0,   "B": 6,   "F": 8},
    "B":  { "W": 9,   "T": 0,   "G2": 8,   "G1": 6,   "B": 0,   "F": 12},
    "F":  { "W": 0,   "T": 0,   "G2": 10,  "G1": 8,   "B": 12,  "F": 0},
}

class DijkGraph(Graph):
    def __init__(self, data: dict[str, dict[str, float]]):
       self.data = data
       self.vertices = [vert for vert in self.data]
       self.size = len(self.data)

    def printSolution(self, dist):
        print("Vertex \t Distance from Source")
        for node in self.data:
            print(node, "\t\t", dist[node])

    def minDistance(self, dist: dict[str, float], sptSet):
        min = 1e7
        min_index = ""

        for v in self.data:
            if dist[v] < min and sptSet[v] == False:
                min = dist[v]
                min_index = v

        return min_index

    def Dijkstra(self, src: str):
        dist: dict[str, float] = {}
        sptSet: dict[str, float] = {}

        for vertex in self.data:
            dist[vertex] = 1e7
            sptSet[vertex] = False

        dist[src] = 0

        for cout in self.data:

            #Get the minimum distance vertex from unprocessed vertices
            #u is always src in first iteration
            u = self.minDistance(dist, sptSet)

            #Put min distance to shortest path tree
            sptSet[u] = True

            #Update the dist value for adjacent vertices if new distance
            # is shorter than current distance and vertex is not in
            # sptSet already
            for v in self.data:
                if (self.data[u][v] > 0 and
                    sptSet[v] == False and
                    dist[v] > dist[u] + self.data[u][v]):
                    dist[v] = dist[u] + self.data[u][v]

        self.printSolution(dist)



class MainScene(Scene):
    def constructor(self):
        graph = DijkGraph(graph_data)
        self.play(Create(graph))
        graph.Dijkstra("W")
        self.wait()
        self.play(Uncreate(graph))
        self.wait()
        self.play(Create(Label("test")))
        self.wait()
