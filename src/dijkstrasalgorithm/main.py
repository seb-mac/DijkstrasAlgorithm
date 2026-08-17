from manim import * # type: ignore

graph_data: dict[str, list[float]] = {
#           W   T  G2  G1    B   F
    "W":  [ 0, 10,  0,  8,   9,  0], #W
    "T":  [10,  0,  6,  0,   0,  0], #T
    "G2": [ 0,  6,  0,  0,   8, 10], #G2
    "G1": [ 8,  0,  0,  0,   6,  8], #G1
    "B":  [ 9,  0,  8,  6,   0, 12], #B
    "F":  [ 0,  0, 10,  8,  12,  0], #F
}

class WeightedGraph(GenericGraph):
    def __init__(self, data: list[list[float]]):
       self.data = data
       self.vertex_list = [i for i in range(len(self.data))]
       self.size = len(self.data)

       self.vertices

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


class MainScene(Scene):
    def construct(self):
        vertices = ['W', 'G1', 'T', 'B', 'G2', 'F']

        #The distance from source vertex vertices['W'] to vertex dist[u]
        dist: dict[str, int] = {}

        edgeList = [('W', 'G1', 8), 
                    ('W', 'B', 9), 
                    ('W', 'T', 10), 
                    ('T', 'G2', 6), 
                    ('G1', 'B', 6), 
                    ('G2', 'B', 8), 
                    ('F', 'G1', 8),
                    ('F', 'B', 12),
                    ('F', 'G2', 10),
                    ]
        
        # self.interactive_embed()

        graph = Graph(vertices, [(u, v) for u, v, __ in edgeList], labels=True)
        self.play(Create(graph))
        self.wait()
        weightLabels = VGroup()

        self.play(graph['W'].animate.move_to([-5, -2, 0]),
                  graph['G1'].animate.move_to([-3, 2, 0]),
                  graph['T'].animate.move_to([0, -3, 0]),
                  graph['B'].animate.move_to([-1, 0, 0]),
                  graph['G2'].animate.move_to([2, -1, 0]),
                  graph['F'].animate.move_to([3, 2, 0]),
                  )

        for u, v, w in edgeList:
            #Get the midpoint of the edge
            midpoint = (graph[u].get_center() + graph[v].get_center()) / 2
            label = Text(str(w), font_size=24).move_to(midpoint)
            weightLabels.add(label)

        self.play(FadeIn(weightLabels))
        self.wait()
        self.play(Create(Text(str(graph['W']))))

    def Dijkstra(self, graph, source):
        for vertex in graph:
            pass