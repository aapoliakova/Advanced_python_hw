import ast
import inspect
from collections import defaultdict

import matplotlib.pyplot as plt
import networkx as nx
from networkx.drawing.nx_pydot import graphviz_layout

from hw_1.easy import fibonacci_numbers


class AST_VIS(ast.NodeVisitor):
    def __init__(self):
        self.G = nx.DiGraph()
        self.stack = []
        self.cl = defaultdict(int)
        self.labels, self.colors = dict(), dict()

    def add(self, node, label, color):
        class_name = node.__class__.__name__
        self.cl[class_name] += 1
        node_name = f"{class_name}_{self.cl[class_name]}"

        if len(self.stack) > 0:
            p_name = self.stack[- 1]
            self.G.add_edge(p_name, node_name)
        self.G.add_node(node_name)
        self.stack += [node_name]
        self.labels[node_name], self.colors[node_name] = label, color
        super(self.__class__, self).generic_visit(node)
        self.stack.pop()

    def generic_visit(self, node):
        label = node.__class__.__name__
        self.add(node, label, "skyblue")

    def visit_Name(self, node):
        label = f"{node.__class__.__name__}\nid: {node.id}"
        self.add(node, label, "sandybrown")

    def visit_FunctionDef(self, node):
        label = f"{node.name}"
        self.add(node, label, "tomato")

    def visit_arg(self, node):
        label = f"{node.__class__.__name__}\n: {node.arg}"
        self.add(node, label, "gold")

    def visit_Constant(self, node):
        label = f"{node.__class__.__name__}\n: {node.value}"
        self.add(node, label, "yellowgreen")

    def draw(self, path):
        plt.figure(figsize=(20, 20))
        layout = graphviz_layout(self.G, prog="dot")
        nx.draw_networkx(self.G, layout,
                         node_color=[self.colors[y] for y in self.G.nodes()],
                         node_size=[300 * len(x) for x in self.G.nodes()],
                         labels=self.labels)
        plt.savefig(path)


if __name__ == "__main__":
    decor = AST_VIS()
    ast_object = ast.parse(inspect.getsource(fibonacci_numbers))
    decor.visit(ast_object)
    decor.draw("artifacts/AST.png")
