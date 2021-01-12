from flask import render_template,url_for,redirect, render_template_string
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point, LineString
import matplotlib.pyplot as plt
import plotly_express as px
import networkx as nx
import osmnx as ox


from script.app.location_moderator import verif_user_input, change_type
from script.app import navig
from script.app.forms import Location
from script.app.routing_animation import create_line_gdf,create_graph
from script.app.config import Config



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

@navig.route("/error/<error_type>")
def error(error_type:str):
    return render_template("error.html",title="Error",error_type=error_type)

@navig.route("/nav",methods=["GET", "POST"])
def nav():
    """[summary]
    Returns:
        [type]: [description]
    """    
    form = Location()
    

    if form.validate_on_submit():
        #forms fields
        location_start = form.location_start.data
        location_to = form.location_to.data
        choice_user = form.transportation.data
        choice_weight = form.pick.data

        print(location_start,location_to,choice_user,choice_weight)
        
        #call error_raiser function:
            #if true: cool
            #if false : return error.html
        return redirect(url_for("error",error_type="TESTING"))

        return redirect(url_for("road",location_start=location_start,
                                        location_to=location_to,
                                        choice_user=choice_user,
                                        choice_weight = choice_weight))

    return render_template("nav.html" , title = "Ny-Nav",form=form)

@navig.route("/road/<location_start>/<location_to>/<choice_user>/<choice_weight>")
def road(location_start:str,location_to:str,choice_user:str,choice_weight:str):
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
    if choice_weight == "safe" or choice_weight == "fast":
        
        if choice_user == "drive": 
            G = ox.io.load_graphml(filepath=Config.drive_safest)   

        if choice_user == "walk": 
            G = ox.io.load_graphml(filepath=Config.walk_safest)   
        
        if choice_user == "bike": 
            G = ox.io.load_graphml(filepath=Config.bike_safest)   


    elif choice_weight == "do you want to die?":
        

        if choice_user == "drive": 
            G = ox.io.load_graphml(filepath=Config.drive_dangerous)   

        if choice_user == "walk": 
            G = ox.io.load_graphml(filepath=Config.walk_dangerous)   
        
        if choice_user == "bike": 
            G = ox.io.load_graphml(filepath=Config.bike_dangerous)   

    elif choice_weight == "ratio safe-fast":
        
        if choice_user == "drive": 
            G = ox.io.load_graphml(filepath=Config.drive_safest_ratio)   

        if choice_user == "walk": 
            G = ox.io.load_graphml(filepath=Config.walk_safest_ratio)   
        
        if choice_user == "bike": 
            G = ox.io.load_graphml(filepath=Config.bike_safest_ratio)    
        
             
    G = change_type(G)


    print('Datas passed : \n{} \n{} \n{} \n{}'.format(location_start,location_to,choice_user,choice_weight))
    #Conversions to float
    
    start = verif_user_input(location_start, location_to)[0]
    end = verif_user_input(location_start,location_to)[1]
    

    start_node = ox.get_nearest_node(G, start) 
    end_node = ox.get_nearest_node(G, end)
    
    if choice_weight == "do you want to die?" or choice_weight == "safe":

        route = nx.shortest_path(G, start_node, end_node, weight="danger")
        
        
    elif choice_weight == "fast":
    #see the travel time for the whole route
        route = nx.shortest_path(G, start_node, end_node, weight="travel_time")
    
    elif choice_weight == "ratio safe-fast":
    
           route = nx.shortest_path(G, start_node, end_node, weight="ratio")         
    
    folium_map = ox.folium.plot_route_folium(G, route=route)
    folium_map.save("folium_map.html")
    
    
    #return render_template("road.html",title ="Path", div=div)

    
    return render_template_string('''
        <head>
            <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>    
        </head>
            <body>
        {{ div_placeholder|safe }}
            </body>''', div_placeholder=folium_map._repr_html_())
    


    