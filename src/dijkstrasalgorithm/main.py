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
        self.edge_list: dict[tuple[str, str], float] = {}
        for u in self.data:
           for v in self.data[u]:
               if (u is not None) and (
                    v is not None) and (
                    self.data[u][v] != 0) and (
                    set((u, v)) not in [set(i) for i in self.edge_list]):
                   self.edge_list[(u, v)] = self.data[u][v]

        self.labels: bool = True

        def labeled_edge(start, end, **kwargs):
            # Find which edge this is (order doesn't matter)
            edge_key = (start, end) if (start, end) in self.edge_list.keys() else (end, start)
            label_text = str(self.edge_list.get(edge_key, ""))
            return LabeledLine(
                start=start,
                end=end,
                label=label_text,
                label_position=0.5,
                label_color=YELLOW,
                stroke_color=BLUE,
                stroke_width=3,
            )

        super().__init__(
            vertices = self.vertices_list,
            edges = list(self.edge_list.keys()),
            labels = self.labels,
            layout_scale=3,
            edge_type=labeled_edge,
            **kwargs
        )


    def rearrange(self, coords: dict[str, tuple[float, float, float]]):

        for v in coords:
            self.vertices[v].move_to(coords[v])

        return self

    def getEdge(self, u: str, v: str):
        if (u, v) in self.edges:
            return self.edges[(u, v)]
        if (v, u) in self.edges:
            return self.edges[(v, u)]
        raise KeyError(f"No edge found between {u} and {v}")

    def printSolution(self, dist):
        print("Vertex \t Distance from Source")
        for node in self.data:
            print(node, "\t\t", dist[node])
        print(self.vertices_list)

    def minDistance(self, dist: dict[str, float], sptSet) -> str:
        min = 1e7
        min_index = ""

        for v in self.data:
            if (dist[v] < min) and ( #If distance to v is less than previous (dist[v] starts at 1e7)
                sptSet[v] == False): #If v is not in shortest spanning tree yet
                min = dist[v] #Set the new shortest distance to any vertex
                min_index = v #Set the shortest distance to any vertex to ID of v

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

    def minDistance(self, graph: WeightedGraph, dist: dict[str, float], sptSet) -> str:
        min = 1e7
        min_index = ""
    
        for v in graph.data:
            graph.vertices[v].set_color(RED)
            self.wait()
            if (dist[v] < min) and ( #If distance to v is less than previous (dist[v] starts at 1e7)
                sptSet[v] == False): #If v is not in shortest spanning tree yet
                min = dist[v] #Set the new shortest distance to any vertex
                min_index = v #Set the shortest distance to any vertex to ID of v
    
        return min_index
    
    def construct(self):

        #The distance from source vertex vertices['W'] to vertex dist[u]
        
        # self.interactive_embed()

        graph = WeightedGraph(graph_data)
        self.play(Create(graph))

        self.wait()

        self.play(graph.animate.rearrange({"W": (-5, -2, 0),
                         "G1": (-3, 2, 0),
                         "T": (0, -3, 0),
                         "B": (-1, 0, 0),
                         "G2": (2, -1, 0),
                         "F": (3, 2, 0)}))
        self.wait()

        #region DIJKSTRA
        src = "W"

        dist: dict[str, float] = {}
        sptSet: dict[str, bool] = {}
        
        for vert in graph.data:
            dist[vert] = 1e7
            sptSet[vert] = False
        
        dist[src] = 0
        
        for vert in graph.data:
        
            #Get the minimum distance vertex from unprocessed vertices
            #u is always src in first iteration
            #(get the vertex closest to vert)
            u = graph.minDistance(dist, sptSet)
        
            graph.vertices[u].set_color(RED)
            self.wait()
            graph.vertices[u].set_color(WHITE)
        
        
            #Put min distance to shortest path tree
            sptSet[u] = True
        
            #Update the dist value for adjacent vertices if new distance
            # is shorter than current distance and vertex is not in
            # sptSet already
            for v in graph.data:
                if (graph.data[u][v] > 0 and
                    sptSet[v] == False and
                    dist[v] > dist[u] + graph.data[u][v]):
                    dist[v] = dist[u] + graph.data[u][v]
        #endregion

        # for u, v, w in edgeList:
        #     #Get the midpoint of the edge
        #     midpoint = (graph[u].get_center() + graph[v].get_center()) / 2
        #     label = Text(str(w), font_size=24).move_to(midpoint)
        #     weightLabels.add(label)

        # self.play(FadeIn(weightLabels))
        # self.wait()
        # self.play(Create(Text(str(graph['W']))))