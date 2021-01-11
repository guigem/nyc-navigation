from flask import Flask
import osmnx as ox
import pandas as pd
import networkx as nx
import osmnx

from script.app.config import Config
from script.app.routing_animation import create_graph


navig = Flask(__name__)
navig.config.from_object(Config)


from script.app import routes

