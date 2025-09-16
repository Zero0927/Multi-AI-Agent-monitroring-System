import pandas as pd
import networkx as nx
from node2vec import Node2Vec

class InteractionAgent:
    def __init__(self, file_path, mode="baseline"):
        self.data = pd.read_csv(file_path)
        self.mode = mode

    def calculate_ci(self):
        """Baseline metric"""
        replied = len(self.data[self.data["is_reply"] == 1])
        received = len(self.data)
        return replied / received if received > 0 else 0

    def calculate_embeddings(self):
        """AI-powered: Graph embeddings"""
        edges = list(zip(self.data["sender"], self.data["receiver"]))
        graph = nx.DiGraph()
        graph.add_edges_from(edges)

        node2vec = Node2Vec(graph, dimensions=8, walk_length=5, num_walks=10)
        model = node2vec.fit(window=3, min_count=1, batch_words=4)
        return model.wv