from flask import Flask
import osmnx as ox

from app.config import Config
from app.routing_animation import create_graph

navig = Flask(__name__)
navig.config.from_object(Config)

G = create_graph("Gothenburg", 2500, "drive")
G = ox.add_edge_speeds(G) 
G = ox.add_edge_travel_times(G) 

from app import routes

