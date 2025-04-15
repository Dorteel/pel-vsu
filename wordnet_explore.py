import nltk
from nltk.corpus import wordnet as wn
import networkx as nx
import matplotlib.pyplot as plt

# Download WordNet
nltk.download('wordnet')
nltk.download('omw-1.4')

def get_synsets(word):
    synsets = wn.synsets(word)
    for i, synset in enumerate(synsets):
        print(f"[{i}] {synset.name()}: {synset.definition()}")
    return synsets

def build_graph(synset, graph, visited=None, depth=0, max_depth=3):
    """Recursively add synset and its hyponyms to the graph."""
    if visited is None:
        visited = set()

    if synset.name() in visited or depth > max_depth:
        return

    visited.add(synset.name())
    hyponyms = synset.hyponyms()
    for h in hyponyms:
        graph.add_edge(synset.name(), h.name())
        build_graph(h, graph, visited, depth+1, max_depth)

def hierarchy_pos(G, root, width=1.0, vert_gap=0.4, vert_loc=0, xcenter=0.5,
                  pos=None, parent=None, parsed=None, node_spacing=0.1):
    """Modified tree layout with spacing buffer between siblings."""
    if pos is None:
        pos = {}
    if parsed is None:
        parsed = set()

    pos[root] = (xcenter, vert_loc)
    parsed.add(root)

    children = list(G.successors(root))
    if parent:
        children = [c for c in children if c != parent]

    if children:
        total_children = len(children)
        # Add spacing buffer
        dx = width / (total_children + (total_children - 1) * node_spacing)
        next_x = xcenter - width / 2 + dx / 2

        for child in children:
            pos = hierarchy_pos(G, child,
                                width=dx * (1 + node_spacing),
                                vert_gap=vert_gap,
                                vert_loc=vert_loc - vert_gap,
                                xcenter=next_x,
                                pos=pos,
                                parent=root,
                                parsed=parsed,
                                node_spacing=node_spacing)
            next_x += dx * (1 + node_spacing)

    return pos


def visualize_wordnet_tree(word, max_depth=2):
    synsets = get_synsets(word)
    if not synsets:
        print("No synsets found.")
        return

    selected_synset = synsets[0]  # You can prompt the user here

    G = nx.DiGraph()
    build_graph(selected_synset, G, max_depth=max_depth)

    if not G.nodes:
        print("No graph to draw.")
        return

    pos = hierarchy_pos(G, selected_synset.name())
    plt.figure(figsize=(16, 10))
    labels = {n: n.split('.')[0].replace('_', ' ') for n in G.nodes()}
    nx.draw(G, pos, labels=labels, with_labels=True,
        node_size=2000, font_size=9, node_color='lightblue', arrows=False)
    plt.title(f"WordNet Hyponym Tree for '{selected_synset.name()}'", fontsize=14)
    plt.axis('off')
    plt.savefig("wordnet_tree.png", bbox_inches="tight")
    print("Graph saved to 'wordnet_tree.png'")

# Run it
visualize_wordnet_tree("chair", max_depth=3)
