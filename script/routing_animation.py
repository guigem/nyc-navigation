import pandas as pd
import geopandas as gpd
from shapely.geometry import Point, LineString

import matplotlib.pyplot as plt
import plotly_express as px

import networkx as nx
import osmnx as ox

import plotly.express as px

from geopy.geocoders import Nominatim

def lat_long_place(place: str) -> float:
    '''
    Get the latitude and longitude from any place.

    Parameters
    ----------
    place : str
        String with the name of a place wanted.

    Returns
    -------
    float
        Latitude and longitude values as float.

    '''
    geolocator = Nominatim(user_agent="nyc-navigation")
    
    #Getting the location
    location = geolocator.geocode(place)
    
    #Getting latitude and longitude
    latitude = location.latitude
    longitude = location.longitude
    
    return latitude, longitude 

def create_graph(loc, dist, transport_mode, loc_type="address"):
    """Transport mode = ‘walk’, ‘bike’, ‘drive’"""
    if loc_type == "address":
        G = ox.graph_from_address(loc, dist=dist, network_type=transport_mode)
    elif loc_type == "points":
        G = ox.graph_from_point(loc, dist=dist, network_type=transport_mode )
    return G

'''
    Show a map with the faster way between two points.

    Parameters
    ----------
    start, end : float
        start and end containts two elements (x et y coordinates the start destination and the final destination) 
        in a tuple for each variables 

    Returns
    -------
    Show a map with the itinary between two points

    '''
def animation_map (start, end) : 
    if type(start) == str :
        start = lat_long_place(start)
    if  type(start) == str :
        end = lat_long_place(end)

    ox.config(use_cache=True, log_console=True)
    G  = create_graph("New York", 10000, "drive")

    # impute missing edge speeds and add travel times
    G = ox.add_edge_speeds(G) 
    G = ox.add_edge_travel_times(G) 
    start_node = ox.get_nearest_node(G, start) 
    end_node = ox.get_nearest_node(G, end)
    route = nx.shortest_path(G, start_node, end_node, weight='travel_time') # nodes between start and end coordinates 


    #see the travel time for the whole route
    travel_time = nx.shortest_path_length(G, start_node, end_node, weight='travel_time')

    #create list 
    node_start = []
    node_end = []
    X_to = []
    Y_to = []
    X_from = []
    Y_from = []
    length = [] 
    travel_time = []

    for u, v in zip(route[:-1], route[1:]):
        node_start.append(u) # add to list all nodes from route except the last
        node_end.append(v) # add to list all nodes from route except the first
        length.append(round(G.edges[(u, v, 0)]['length'])) # calcul length between two nodes
        travel_time.append(round(G.edges[(u, v, 0)]['travel_time'])) # calcul travel_time between two nodes
        X_from.append(G.nodes[u]['x']) # add to list with X coordinate from start node
        Y_from.append(G.nodes[u]['y']) # add to list with y coordinate from start node
        X_to.append(G.nodes[v]['x']) # add to list with x coordinate from end node 
        Y_to.append(G.nodes[v]['y']) # add to list with y coordinate from end node
   
    # create the dataframe from lists 
    df = pd.DataFrame(list(zip(node_start, node_end, X_from, Y_from,  X_to, Y_to, length, travel_time)), 
                columns =["node_start", "node_end", "X_from", "Y_from",  "X_to", "Y_to", "length", "travel_time"]) 

    # reset the index of the DataFrame
    df.reset_index(inplace=True)

    # acess token from mapbox
    px.set_mapbox_access_token("pk.eyJ1Ijoic2hha2Fzb20iLCJhIjoiY2plMWg1NGFpMXZ5NjJxbjhlM2ttN3AwbiJ9.RtGYHmreKiyBfHuElgYq_w")


    fig = px.scatter_mapbox(df, lon= "X_from", lat="Y_from", width=1600, height=800, zoom=12) # create map between start points and end points 
    fig.add_trace(px.line_mapbox(df, lon= "X_from", lat="Y_from").data[0]) # draw lines between nodes 

    fig.show() # show the map

# call the function animation map 
animation_map((40.7518, -73.817314),((40.624958,-74.145775)))