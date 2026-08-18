from manim import * # type: ignore

graph_data: dict[str, dict[str, float]] = {
#           W   T  G2  G1    B   F
    "W":  { "W": 0, "T": 10,  "G2": 0,  "G1": 8,   "B": 9,  "F": 0}, #W
    "T":  {"W": 10,  "T": 0,  "G2": 6,  "G1": 0,   "B": 0,  "F": 0}, #T
    "G2": { "W": 0,  "T": 6,  "G2": 0,  "G1": 0,   "B": 8, "F": 10}, #G2
    "G1": { "W": 8,  "T": 0,  "G2": 0,  "G1": 0,   "B": 6,  "F": 8}, #G1
    "B":  { "W": 9,  "T": 0,  "G2": 8,  "G1": 6,   "B": 0, "F": 12}, #B
    "F":  { "W": 0,  "T": 0, "G2": 10,  "G1": 8,  "B": 12,  "F": 0}, #F
}

class WeightedGraph(Graph): # type: ignore
    def __init__(self, data: dict[str, dict[str, float]], **kwargs):
        self.data = data
        
        self.vertices_list = [vert for vert in self.data]
        self.edge_list: list[tuple[str, str]] = []
        for u in self.data:
           for v in self.data[u]:
               if (u is not None) and (
                    v is not None) and (
                    self.data[u][v] != 0) and (
                    set((u, v)) not in [set(i) for i in self.edge_list]):
                   self.edge_list += [(u, v)]

        self.labels: bool = True

        super().__init__(
            vertices = self.vertices_list,
            edges = self.edge_list,
            labels = self.labels,
            **kwargs
        )

    def rearrange(self, coords: dict[str, list[int]]):
        print(self.vertices)
        for v in coords:
            print(coords[v])
            self.vertices[v].animate.move_to([-5, -2, 0])

    def printSolution(self, dist):
        print("Vertex \t Distance from Source")
        for node in self.data:
            print(node, "\t\t", dist[node])
        print(self.vertices_list)

    def minDistance(self, dist: dict[str, float], sptSet) -> str:
        min = 1e7
        min_index = ""

        for v in self.data:
            if dist[v] < min and sptSet[v] == False:
                min = dist[v]
                min_index = v

        return min_index

    def Dijkstra(self, src):

        dist: dict[str, float] = {}
        sptSet: dict[str, bool] = {}

        for vert in self.data:
            dist[vert] = 1e7
            sptSet[vert] = False

        dist[src] = 0

        for vert in self.data:

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

g = WeightedGraph(graph_data)

g.Dijkstra('W')
class MainScene(Scene): # type: ignore
    def construct(self):

        #The distance from source vertex vertices['W'] to vertex dist[u]
        
        # self.interactive_embed()

        graph = WeightedGraph(graph_data)
        self.play(Create(graph)) # type: ignore
        self.wait()
        weightLabels = VGroup()

        self.play(graph.rearrange({"W": [-5, -2, 0],
                         "G1": [-3, 2, 0],
                         "T": [0, -3, 0],
                         "B": [-1, 0, 0],
                         "G2": [2, -1, 0],
                         "F": [3, 2, 0]}))
        # self.play(graph['W'].animate.move_to([-5, -2, 0]),
        #           graph['G1'].animate.move_to([-3, 2, 0]),
        #           graph['T'].animate.move_to([0, -3, 0]),
        #           graph['B'].animate.move_to([-1, 0, 0]),
        #           graph['G2'].animate.move_to([2, -1, 0]),
        #           graph['F'].animate.move_to([3, 2, 0]),
        #           )

        # for u, v, w in edgeList:
        #     #Get the midpoint of the edge
        #     midpoint = (graph[u].get_center() + graph[v].get_center()) / 2
        #     label = Text(str(w), font_size=24).move_to(midpoint)
        #     weightLabels.add(label)

        # self.play(FadeIn(weightLabels))
        # self.wait()
        # self.play(Create(Text(str(graph['W']))))