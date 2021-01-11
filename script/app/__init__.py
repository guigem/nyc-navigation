from flask import Flask
import osmnx as ox
import pandas as pd
import networkx as nx
import osmnx

from script.app.config import Config
from script.app.routing_animation import create_graph

def nodes_from_csv(path):
    df = pd.read_csv(path, index_col=0)
    nodes = []
    
    for ix , row in df.iterrows():
        d = dict(row)
        node = d.pop('node')
        nodes.append((node, {k:v for k,v in d.items() if v}))
        
    return nodes

navig = Flask(__name__)
navig.config.from_object(Config)

<<<<<<< HEAD
#G = ox.graph_from_place('Manhattan, New York, USA', network_type="drive")
#G = ox.add_edge_speeds(G) 
#G = ox.add_edge_travel_times(G)

#adj_matrix = pd.read_csv(r"C:\Users\Guillaume\Documents\git\nyc-navigation\CSV\drive_safest.csv")
#G = nx.from_pandas_edgelist(adj_matrix, create_using=nx.MultiDiGraph)

#nodes = nodes_from_csv(r"C:\Users\Guillaume\Documents\git\nyc-navigation\CSV\drive_safe_node.csv")

#G.update(nodes=nodes)

G = osmnx.graph.graph_from_xml(filepath=r'C:\Users\Guillaume\Documents\git\nyc-navigation\CSV\test.osm')
=======
G = create_graph("Gothenburg", 2500, "drive") #En attendant les csv
>>>>>>> d7b057f2c3c6a1bb124daf7cb0781f8e6b598937
G = ox.add_edge_speeds(G) 
G = ox.add_edge_travel_times(G) 
#G = create_graph("Gothenburg", 2500, "drive")
#G = ox.add_edge_speeds(G) 
#G = ox.add_edge_travel_times(G) '

from script.app import routes

