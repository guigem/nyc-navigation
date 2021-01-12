
from geopy.geocoders import Nominatim
import geopy.geocoders
import osmnx as ox
import networkx as nx

from script.app.config import Config


def lat_long_place(place: str) -> tuple:
    '''
    Get the latitude and longitude from any place.

    Parameters
    ----------
    place : str
        String with the name of a place wanted.

    Returns
    -------
    tuple
        Tuple with latitude and longitude values as float.

    '''
    geopy.geocoders.options.default_timeout = None
    geolocator = Nominatim(user_agent="nyc-navigation", scheme='http')
    
    #Getting the location
    location = geolocator.geocode(place)
    
    #Getting latitude and longitude
    latitude = location.latitude
    longitude = location.longitude
    
    return latitude, longitude 


def verif_user_input(location_start:str,location_to:str) -> tuple:
    '''
    Function that returns the latitude and longitude of starting and ending points.
    A differentiation is made to accept either places and gps coordonates.

    Parameters
    ----------
    location_start : str
        String that represents our the location of our starting point.
    location_to : str
        String that represents our the location of our ending point..

    Returns
    -------
    tuple
        Tuple with two elements as float:
            - latitude and longitude of the starting point
            - latitude and longitude of the ending point.


    '''

    
    # Detect the first input type and change change it if needed.
    if location_start[0] == "(":
       
        #Spliting latitude an longitude
        location_start = location_start.split(",")
        
        #Removing remaining "(" from longitude and turning it into float for starting point 
        long_start = location_start[1]
        long_start = long_start[:-1]
        long_start = float(long_start)

        #Removing remaining "(" from latitude and turning it into float for starting point 
        lat_start = location_start[0]
        lat_start = lat_start[1:]
        lat_start = float(lat_start)

        coord_start = (lat_start, long_start)

    else:
        
        coord_start = lat_long_place(location_start)
    
    # Detect the second input type and change change it if needed.
    if location_to[0] == "(":

        location_to = location_to.split(",")

        long_to = location_to[1]
        long_to = long_to[:-1]
        long_to = float(long_to)

        #Removing remaining "(" from latitude and turning it into float for ending point
        lat_to = location_to[0]
        lat_to = lat_to[1:]
        lat_to = float(lat_to)

        coord_to = (lat_to, long_to)

    else:

        coord_to = lat_long_place(location_to)
    
    # Make a list with the results.
    result = [coord_start, coord_to]

    return result


def change_type(G: classmethod) -> classmethod:
    '''
    Changing type of attributes of edges for the network because of the graphml import.
    

    Parameters
    ----------
    G : classmethod
        Network of NYC with only strings as types.

    Returns
    -------
    classmethod
        Network of NYC with float for danger, travel_time and ratio (when present) as types.

    '''
    
    #Generate the edges
    edges = list(G.edges(keys=True, data=True))
    
    #Iterate on all edges
    for i in range(len(edges)):
        
        #Change types as float
        edges[i][3]["danger"] = float(edges[i][3]["danger"])
        edges[i][3]["travel_time"] = float(edges[i][3]["travel_time"])
        
        #Change radio only when it is present 
        try:
            edges[i][3]["ratio"] = float(edges[i][3]["ratio"])
        except:
            continue
        
    return G

def error_raiser(entry_one:str , entry_two:str) -> tuple:
    """

    """

    # Dectect if the two entries are the same.
    if entry_one == entry_two:
        return False, "Same entries"
    
    # Detect if the entries are valid.
    if entry_one[0] != "(":
        try:
            coor_sart = lat_long_place(entry_one)
        except AttributeError:
            return False, "Wrong entry"
    
    if entry_two[0] != "(":
        try:
            coor_to = lat_long_place(entry_two)
        except:
            return False, "Wrong entry"
    
    return True

def choose_right_network(choice_weight: str, choice_user: str) -> classmethod:
    '''
    Take the right network based on the weight and movement type chosen.
    All the files are stored as .graphml and are called in Config.py

    Parameters
    ----------
    choice_weight : str
        What type of path the user wants to see.
    choice_user : str
        What movement type the user takes.

    Returns
    -------
    classmethod
        Return the right network.

    '''
    
    
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
        
    #Changing the type of a few attributes    
    G = change_type(G)
    
    return G

def compute_route(G : classmethod, start_node: tuple, end_node: tuple, choice_weight: str) -> list:
    '''
    Computing the right route (or list of nodes) for given starting and ending points and weights.  

    Parameters
    ----------
    G : classmethod
        Network of streets.
    start_node : tuple
        Tuple with coordinates for the starting point.
    end_node : tuple
        Tuple with coordinates for the ending point.
    choice_weight : str
        What type of path the user wants to see..

    Returns
    -------
    list
        List of nodes where our optimal path will go through.

    '''
    
    
    if choice_weight == "do you want to die?" or choice_weight == "safe":

        route = nx.shortest_path(G, start_node, end_node, weight="danger")
        
        
    elif choice_weight == "fast":
    #see the travel time for the whole route
        route = nx.shortest_path(G, start_node, end_node, weight="travel_time")
    
    elif choice_weight == "ratio safe-fast":
    
           route = nx.shortest_path(G, start_node, end_node, weight="ratio")  

    return route



