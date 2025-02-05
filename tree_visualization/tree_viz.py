import networkx as nx
import matplotlib.pyplot as plt
import gradio as gr
import plotly.graph_objects as go
import json
from collections import defaultdict

# Load and parse the JSON file
def fun(file_path):
    with open(file_path, 'r') as file:
        solutions_data = json.load(file)
    return solutions_data

solutions_data = fun("solutions.json")

adj_list = defaultdict(list)
for ele in solutions_data:
    if ele["parent"] is None:
        continue
    adj_list[ele["parent"]].append(ele["agent_id"])

print(adj_list)

def build_tree_structure(adj_list, root="root"):
    """
    Converts an adjacency list to Plotly-compatible labels and parents for Sunburst.
    """
    labels = []
    parents = []

    # Recursive function to traverse the tree
    def traverse(node, parent=None):
        labels.append(node)
        parents.append(parent if parent else "")
        for child in adj_list.get(node, []):
            traverse(child, node)

    traverse(root)
    return labels, parents

# Generate labels and parent-child relationships
root_node = list(set(adj_list.keys()) - {child for children in adj_list.values() for child in children})
root_node = root_node[0] if root_node else "root"
labels, parents = build_tree_structure(adj_list, root=root_node)

def display_interactive_tree():
    """
    Returns an interactive Plotly tree using Sunburst.
    """
    fig = go.Figure(go.Sunburst(
        labels=labels,
        parents=parents,
        hoverinfo='label+percent parent',
        marker=dict(colorscale='Viridis')
    ))
    fig.update_layout(margin=dict(t=0, l=0, r=0, b=0))
    fig.show()

    # Placeholder for Gradio compatibility
    return "Interactive Plot Displayed (Check Plotly Visualization)"

# Gradio interface for the interactive plot
interface = gr.Interface(
    fn=display_interactive_tree,
    inputs=None,
    outputs="text",
    title="Interactive Tree Visualization"
)

interface.launch()
