from flask import render_template,url_for,redirect, render_template_string
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point, LineString
import matplotlib.pyplot as plt
import plotly_express as px
import networkx as nx
import osmnx as ox
import osmnx

from app.config import Config

from app.location_moderator import change_type


def ratio(safe:bool = True, choice_user:str = "drive"):

    if safe:
        
        if choice_user == "drive": 
            G = ox.io.load_graphml(filepath=Config.drive_safest)   

        if choice_user == "walk": 
            G = ox.io.load_graphml(filepath=Config.walk_safest)   
        
        if choice_user == "bike": 
            G = ox.io.load_graphml(filepath=Config.bike_safest)   

    else:
        

        if choice_user == "drive": 
            G = ox.io.load_graphml(filepath=Config.drive_dangerous)   

        if choice_user == "walk": 
            G = ox.io.load_graphml(filepath=Config.walk_dangerous)   
        
        if choice_user == "bike": 
            G = ox.io.load_graphml(filepath=Config.bike_dangerous)   

    G = change_type(G)


    edges = list(G.edges(keys=True, data=True))

    max_travel_time = 1
    max_danger = 1

    for i in range(len(edges)):
        danger_score = edges[i][3]["danger"]
        travel_time_score = edges[i][3]["travel_time"]

        if danger_score > max_danger :
            max_danger = danger_score
        
        if travel_time_score > max_travel_time:
            max_travel_time = travel_time_score

    for i in range(len(edges)):
        
        edges[i][3]["danger"] = edges[i][3]["danger"] / max_danger
        edges[i][3]["travel_time"] = edges[i][3]["travel_time"] / travel_time_score

        edges[i][3]["ratio"] = edges[i][3]["danger"] + edges[i][3]["travel_time"]
    
    osmnx.io.save_graphml(G, filepath="bike_safest_ratio.graphml")

    return G

ratio(True, "bike")
