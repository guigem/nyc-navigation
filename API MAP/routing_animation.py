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
    """Transport mode = ‘walk’, ‘bike’, ‘drive’, ‘drive_service’, ‘all’, ‘all_private’, ‘none’"""
    if loc_type == "address":
        G = ox.graph_from_address(loc, dist=dist, network_type=transport_mode)
    elif loc_type == "points":
        G = ox.graph_from_point(loc, dist=dist, network_type=transport_mode )
    return G

def animation_map (start, end) : 
    if type(start) == str :
        start = lat_long_place(start)
    if  type(start) == str :
        end = lat_long_place(end)

    ox.config(use_cache=True, log_console=True)
    G  = create_graph("New York", 100, "drive")

    # impute missing edge speeds and add travel times
    G = ox.add_edge_speeds(G) 
    G = ox.add_edge_travel_times(G) 
    start_node = ox.get_nearest_node(G, start) 
    end_node = ox.get_nearest_node(G, end)
    route = nx.shortest_path(G, start_node, end_node, weight='travel_time') 

    nx.shortest_path_length

    #see the travel time for the whole route
    travel_time = nx.shortest_path_length(G, start_node, end_node, weight='travel_time')
    print(round(travel_time))

    #create list 
    node_start = []
    node_end = []
    X_to = []
    Y_to = []
    X_from = []
    Y_from = []
    length = [] # distance
    travel_time = []


    for u, v in zip(route[:-1], route[1:]):
        node_start.append(u) 
        node_end.append(v)
        length.append(round(G.edges[(u, v, 0)]['length']))
        travel_time.append(round(G.edges[(u, v, 0)]['travel_time']))
        X_from.append(G.nodes[u]['x']) # create a list with X from start
        Y_from.append(G.nodes[u]['y']) # create a list with y from start
        X_to.append(G.nodes[v]['x']) # create a list with x from end
        Y_to.append(G.nodes[v]['y']) # create a list with y from end

    df = pd.DataFrame(list(zip(node_start, node_end, X_from, Y_from,  X_to, Y_to, length, travel_time)), 
                columns =["node_start", "node_end", "X_from", "Y_from",  "X_to", "Y_to", "length", "travel_time"]) 

    df.reset_index(inplace=True)

    # create a LineString Geodataframe that connects all these nodes coordinates
    def create_line_gdf(df):
        gdf = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df.X_from, df.Y_from))
        gdf["geometry_to"] = [Point(xy) for xy in zip(gdf.X_to, gdf.Y_to)]
        gdf['line'] = gdf.apply(lambda row: LineString([row['geometry_to'], row['geometry']]), axis=1)
        line_gdf = gdf[["node_start","node_end","length","travel_time", "line"]].set_geometry('line')
        return line_gdf

    line_gdf = create_line_gdf(df)

    line_gdf.plot()

    start = df[df["node_start"] == start_node]
    end = df[df["node_end"] == end_node]

    px.set_mapbox_access_token("pk.eyJ1Ijoic2hha2Fzb20iLCJhIjoiY2plMWg1NGFpMXZ5NjJxbjhlM2ttN3AwbiJ9.RtGYHmreKiyBfHuElgYq_w")
    px.scatter_mapbox(df, lon= "X_from", lat="Y_from", zoom=12)


    fig = px.scatter_mapbox(df, lon= "X_from", lat="Y_from", width=800, height=400, zoom=12)
    fig.add_trace(px.line_mapbox(df, lon= "X_from", lat="Y_from").data[0])

    fig.show()

    fig = px.scatter_mapbox(df, lon= "X_from", lat="Y_from", zoom=13, width=1000, height=800, animation_frame="index",mapbox_style="dark")
    fig.data[0].marker = dict(size = 12, color="black")
    fig.add_trace(px.scatter_mapbox(start, lon= "X_from", lat="Y_from").data[0])
    fig.data[1].marker = dict(size = 15, color="red")
    fig.add_trace(px.scatter_mapbox(end, lon= "X_from", lat="Y_from").data[0])
    fig.data[2].marker = dict(size = 15, color="green")
    fig.add_trace(px.line_mapbox(df, lon= "X_from", lat="Y_from").data[0])

    fig.show()

# call the function animation map 
animation_map((40.7518, -73.817314),((40.624958,-74.145775)))