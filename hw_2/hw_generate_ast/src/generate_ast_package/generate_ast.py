import ast
import inspect
import igraph
import numpy as np
import seaborn as sns
from plotly.validators.scatter.marker import SymbolValidator
import networkx as nx
import plotly.graph_objects as go


class MyVisitor(ast.NodeVisitor):
    def __init__(self):
        self.stack = []
        self.G = nx.Graph(directed=True)

    def generic_visit(self, node):
        if len(self.stack) > 0:
            parent = self.stack[-1]
            self.G.add_edge(parent.__class__.__name__, node.__class__.__name__)

        self.stack.append(node)
        ast.NodeVisitor.generic_visit(self, node)
        self.stack.pop()

    def prep_for_plot(self):
        # self.g = igraph.Graph.from_networkx(self.G)
        self.g = igraph.Graph(directed=True)
        self.g.add_vertices(list(self.G.nodes()))
        self.g.add_edges(list(self.G.edges()))

        # Prepare names
        self.names = list(map(lambda node: node["name"], self.g.vs))  # node - index
        self.unique_names = set(self.names)

        # Prepare colors
        self.color_palette = sns.color_palette("Set3", n_colors=len(self.unique_names))
        self.name_to_color = {name: f"rgb{color}" for name, color in zip(list(self.unique_names), self.color_palette)}
        self.vertex_colors = [self.name_to_color[name] for name in self.names]

        # Prepare shapes
        self.shapes = [SymbolValidator().values[i + 2] for i in range(0, len(SymbolValidator().values), 3)]
        if len(self.shapes) < len(self.unique_names):
            self.shapes = np.random.choice(self.shapes, size=len(self.unique_names), replace=True)

        self.name_to_shape = {name: shape for name, shape in zip(list(self.unique_names), self.shapes)}
        self.vertex_shape = [self.name_to_shape[name] for name in self.names]

    def build_graph(self, node):
        self.generic_visit(node)
        self.prep_for_plot()
        return self.g


def plot_and_save_ast(f, save_path):
    text_function = inspect.getsource(f)
    ast_object = ast.parse(text_function)

    v = MyVisitor()
    v.build_graph(ast_object)

    G = v.g
    nr_vertices = G.vcount()
    v_label = v.names
    lay = G.layout('rt')

    position = {k: lay[k] for k in range(nr_vertices)}
    Y = [lay[k][1] for k in range(nr_vertices)]
    M = max(Y)

    E = [e.tuple for e in G.es]  # list of edges

    L = len(position)
    Xn = [position[k][0] for k in range(L)]
    Yn = [2 * M - position[k][1] for k in range(L)]
    Xe = []
    Ye = []
    for edge in E:
        Xe += [position[edge[0]][0], position[edge[1]][0], None]
        Ye += [2 * M - position[edge[0]][1], 2 * M - position[edge[1]][1], None]

    labels = v_label

    def make_annotations(pos, text, font_size=7, font_color='rgb(0,0,0)'):
        L = len(pos)
        if len(text) != L:
            raise ValueError('The lists pos and text must have the same len')
        annotations = []
        for k in range(L):
            annotations.append(
                dict(
                    text=labels[k],  # or replace labels with a different list for the text within the circle
                    x=pos[k][0], y=2 * M - position[k][1],
                    xref='x1', yref='y1',
                    font=dict(color=font_color, size=font_size),
                    showarrow=False)
            )
        return annotations

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=Xe,
                             y=Ye,
                             mode='lines',
                             line=dict(color='rgb(210,210,210)', width=1),
                             hoverinfo='none'
                             ))
    fig.add_trace(go.Scatter(x=Xn,
                             y=Yn,
                             mode='markers',
                             marker=dict(symbol=v.vertex_shape,  # 'circle-dot',
                                         size=45,
                                         color=v.vertex_colors,  # '#6175c1',  #'#DB4551',
                                         line=dict(color='rgb(50,50,50)', width=1)
                                         ),
                             text=labels,
                             hoverinfo='text',
                             opacity=0.8
                             ))

    axis = dict(showline=False,  # hide axis line, grid, ticklabels and  title
                zeroline=False,
                showgrid=False,
                showticklabels=False,
                )

    fig.update_layout(title=None,
                      annotations=make_annotations(position, v_label),
                      font_size=4,
                      showlegend=False,
                      xaxis=axis,
                      yaxis=axis,
                      margin=dict(l=20, r=20, b=20, t=20),
                      hovermode='closest',
                      plot_bgcolor='rgb(248,248,248)'
                      )

    fig.write_image(save_path)
print("OUT")

if __name__ == "__main__":
    print("Hello world")
    print(plot_and_save_ast)