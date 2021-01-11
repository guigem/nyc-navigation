from flask import render_template,url_for,redirect, render_template_string
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point, LineString
import matplotlib.pyplot as plt
import plotly_express as px
import networkx as nx
import osmnx as ox
import osmnx

from script.app import navig
from script.app.forms import Location
from script.app.routing_animation import create_line_gdf,create_graph


#W = create_graph("New York",2500,'walk')

@navig.route('/')
@navig.route('/index')
def index():
    return render_template("index.html" , title="Index")

@navig.route("/about")
def about():
    return render_template("about.html", title="About")

@navig.route("/authors")
def authors():
    return render_template("authors.html", title = "The Authors")

@navig.route("/nav",methods=["GET", "POST"])
def nav():
    """[summary]

    Returns:
        [type]: [description]
    """    
    form = Location()

    if form.validate_on_submit():
        #forms fields
        location = form.location.data
        start_long = form.starting_point_long.data
        start_lat = form.starting_point_lat.data
        arrived_long = form.dest_point_long.data
        arrived_lat = form.dest_point_lat.data
        choice_user = form.transportation.data

        if location=="":
            location = "NONE"

        return redirect(url_for("road",start_long=start_long,
                                        start_lat=start_lat,
                                        arrived_long=arrived_long,
                                        arrived_lat=arrived_lat,
                                        choice_user=choice_user,
                                        location=location))

    return render_template("nav.html" , title = "Ny-Nav",form=form)

@navig.route("/road/<start_lat>/<start_long>/<arrived_lat>/<arrived_long>/<choice_user>/<location>")
def road(start_lat :float,start_long : float,arrived_lat:float,arrived_long:float,choice_user:str,location:str):
    """[summary]

    Args:
        start_long (float): [description]
        start_lat (float): [description]
        arrived_long (float): [description]
        arrived_lat (float): [description]
        choice_user(str): [description]

    Returns:
        [type]: [description]
    """  
    #Network Creation en fonction de choice_user

    G = osmnx.io.load_graphml(filepath=r'C:\Users\Guillaume\Documents\git\nyc-navigation\CSV\test.graphml')    #G = ox.add_edge_speeds(G) 
    #G = ox.add_edge_travel_times(G) 
    
    #call csv.file and build network

    print('Datas passed : \n{} \n{} \n{} \n{}'.format(start_lat,start_long,arrived_lat,arrived_long,choice_user,location))
    #Conversions to float
    start_lat = float(start_lat)
    start_long = float(start_long)
    arrived_lat = float(arrived_lat)
    arrived_long = float(arrived_long)

    #if location is not none > create a function to find lat/long of this location
        #start_lat ,start_long,arrived_lat,arrived_long = thatfunction(location)

    start = (start_long,start_lat)
    end = (arrived_long,arrived_lat)

    start_node = ox.get_nearest_node(G, start) 
    end_node = ox.get_nearest_node(G, end)
    route = nx.shortest_path(G, start_node, end_node, weight=choice_user)
    
    #see the travel time for the whole route
    travel_time = nx.shortest_path_length(G, start_node, end_node, weight=choice_user)

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
        travel_time.append(G.edges[(u, v, 0)]['danger'])
        X_from.append(G.nodes[u]['x']) # create a list with X from start
        Y_from.append(G.nodes[u]['y']) # create a list with y from start
        X_to.append(G.nodes[v]['x']) # create a list with x from end
        Y_to.append(G.nodes[v]['y']) # create a list with y from end

    df = pd.DataFrame(list(zip(node_start, node_end, X_from, Y_from,  X_to, Y_to, length, travel_time)), 
                columns =["node_start", "node_end", "X_from", "Y_from",  "X_to", "Y_to", "length", "travel_time"]) 

    df.reset_index(inplace=True)
    print(df.head())
    #line_gdf = create_line_gdf(df)

    #line_gdf.plot()
    

    start = df[df["node_start"] == start_node]
    end = df[df["node_end"] == end_node]

    px.set_mapbox_access_token("pk.eyJ1IjoiZXphbWV5IiwiYSI6ImNramxnaXBmczBudmsyc3MyOXF1YnNrY2IifQ.EpHSD0OIJkZUICkuQA-gtQ")
    px.scatter_mapbox(df, lon= "X_from", lat="Y_from", zoom=12)


    fig = px.scatter_mapbox(df, lon= "X_from", lat="Y_from", zoom=13, width=1600, height=800, animation_frame="index",mapbox_style="dark")
    fig.data[0].marker = dict(size = 12, color="black")
    fig.add_trace(px.scatter_mapbox(start, lon= "X_from", lat="Y_from").data[0])
    fig.data[1].marker = dict(size = 15, color="red")
    fig.add_trace(px.scatter_mapbox(end, lon= "X_from", lat="Y_from").data[0])
    fig.data[2].marker = dict(size = 15, color="green")
    fig.add_trace(px.line_mapbox(df, lon= "X_from", lat="Y_from").data[0])

    div = fig.to_html(full_html=False)
    fig.write_html("calculated_path.html")
    
    
    #return render_template("road.html",title ="Path", div=div)

    
    return render_template_string('''
        <head>
            <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>    
        </head>
            <body>
        {{ div_placeholder|safe }}
            </body>''', div_placeholder=div)
    


    