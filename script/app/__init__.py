from flask import Flask
import osmnx as ox

from script.app.config import Config
from script.app.routing_animation import create_graph

navig = Flask(__name__)
navig.config.from_object(Config)

G = create_graph("Gothenburg", 2500, "drive")
G = ox.add_edge_speeds(G) 
G = ox.add_edge_travel_times(G) 

from script.app import routes

