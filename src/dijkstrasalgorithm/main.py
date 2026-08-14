from manim import * # type: ignore
    
class MainScene(Scene):
    def construct(self):
        vertices = ['W', 'G1', 'T', 'B', 'G2', 'F']

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
        graph = Graph(vertices, edgeList)
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

        self.interactive_embed()
