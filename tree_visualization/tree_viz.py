import networkx as nx
import matplotlib.pyplot as plt
import gradio as gr
from PIL import Image

# Adjacency list representation of the tree
adj_list = {
    "root": ["child1", "child2"],
    "child1": ["grandchild3333", "grandchild2"],
    "child2": [],
    "grandchild1": [],
    "grandchild2": []
}

# Build the directed graph
G = nx.DiGraph()
for parent, children in adj_list.items():
    for child in children:
        G.add_edge(parent, child)

# Draw and save the tree
plt.figure(figsize=(6, 4))
pos = nx.spring_layout(G)
nx.draw(G, pos, with_labels=True, node_size=1200, node_color='lightblue', font_size=8)
plt.title("Nested Tree Visualization (From Adjacency List)")
plt.savefig("nested_tree_adjacency.png")
plt.close()

def display_tree():
    return Image.open("nested_tree_adjacency.png")

interface = gr.Interface(fn=display_tree, inputs=None, outputs="image", title="Nested Tree Visualization")
interface.launch()
