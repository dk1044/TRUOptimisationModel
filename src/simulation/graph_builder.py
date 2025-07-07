import networkx as nx
from models.station import Station
import matplotlib.pyplot as plt

def build_graph(stations, edges):
    graph = nx.DiGraph()
    for station in stations:
        graph.add_node(station.name, station=station)
    
    for from_station, to_station, distance in edges:
        graph.add_edge(from_station, to_station, weight=distance, direction="up")
        graph.add_edge(to_station, from_station, weight=distance, direction="down")
    return graph

def visualize_graph(graph):
    pos = nx.spring_layout(graph)
    nx.draw(graph, pos, with_labels=True, node_size=500, node_color="lightblue", font_size=5, font_weight="bold")
    labels = nx.get_edge_attributes(graph, 'weight')
    nx.draw_networkx_edge_labels(graph, pos, edge_labels=labels)
    plt.show()
