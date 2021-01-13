
from geopy.geocoders import Nominatim
<<<<<<< HEAD
from geopy.extra.rate_limiter import RateLimiter


import geopy.geocoders
import reverse_geocoder as rg
=======
import geopy.geocoders
import osmnx as ox
import networkx as nx
>>>>>>> 8a9dbf678e2df3507f910f755eb11d9ab30a570a

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
    try:
        latitude = location.latitude
        longitude = location.longitude
    except AttributeError:
        return False
    
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

<<<<<<< HEAD
    return a list two tuples [(lat_start,long_start),(lat_to,long_to)]
    """
    
    # Detect the first input type and change change it if needed.
    if location_start[0] == "(":
        
=======
    
    # Detect the first input type and change change it if needed.
    if location_start[0] == "(":
       
        #Spliting latitude an longitude
>>>>>>> 8a9dbf678e2df3507f910f755eb11d9ab30a570a
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
<<<<<<< HEAD

def change_type(G):
    edges = list(G.edges(keys=True, data=True))

    for i in range(len(edges)):
        
        edges[i][3]["danger"] = float(edges[i][3]["danger"])
        edges[i][3]["travel_time"] = float(edges[i][3]["travel_time"])
        try:
            edges[i][3]["ratio"] = float(edges[i][3]["ratio"])
        except:
            continue
        
    return G

def error_raiser(entry_one:str , entry_two:str) -> tuple:
    """ Check the user's entries. If there will be a problem, return False and the problem.
    param :
        entry_one(str) : First user's entry
        entry_two(str) : Second user's entry

    return :
        bool : False if there will be an error
               True if everything is fine
        str : The name of the error
=======

def error_raiser(entry_one:str , entry_two:str) -> tuple:
    """Function to catch possible errors

    Args:
        entry_one (str): [description]
        entry_two (str): [description]
>>>>>>> 8a9dbf678e2df3507f910f755eb11d9ab30a570a

    Returns:
        tuple: [description]
    """

    # Dectect if the two entries are the same.
    if entry_one == entry_two:
        return False, "Départ et Arrivée doivent être différents"
    
    # Detect if the entries are valid.
    if entry_one[0] != "(":
        try:
<<<<<<< HEAD
            coor_start = lat_long_place(entry_one)

            if reverseGeocode(coor_start) != "New York":
                return False, "Not in NYC"
            
        except AttributeError:
            return False, "Wrong entry"

    if entry_two[0] != "(":
        try:
            coor_to = lat_long_place(entry_two)

            if reverseGeocode(coor_to) != "New York":
                return False, "Not in NYC"
            
        except AttributeError:
            return False, "Wrong entry"
    
    if reverseGeocode(entry_one) != "New York":
        return False, "Not in NYC"

    if reverseGeocode(entry_two) != "New York":
        return False, "Not in NYC"
    
    return True
=======
            coor_sart = lat_long_place(entry_one)
            if not coor_sart:
                return False, "Entrez des coordonnées au format (lat,long)"
        except AttributeError:
            return False, "Entrez des coordonnées au format (lat,long)"
    
    if entry_two[0] != "(":
        try:
            coor_to = lat_long_place(entry_two)
            if not coor_sart:
                return False, "Entrez des coordonnées au format (lat,long)"
        except:
            return False, "Entrez des coordonnées au format (lat,long)"
    
    return True,True

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
            #G = ox.io.load_graphml(filepath=Config.drive_safest)
            G = Config.G_drive_safest   
    
        if choice_user == "walk": 
            #G = ox.io.load_graphml(filepath=Config.walk_safest)   
            G = Config.G_walk_safest
        
        if choice_user == "bike": 
            #G = ox.io.load_graphml(filepath=Config.bike_safest)   
            G = Config.G_bike_safest


    elif choice_weight == "do you want to die?":
    
        if choice_user == "drive": 
            #G = ox.io.load_graphml(filepath=Config.drive_dangerous)   
            G = Config.G_drive_dangerous
    
        if choice_user == "walk": 
            #G = ox.io.load_graphml(filepath=Config.walk_dangerous)   
            G = Config.G_walk_dangerous

        if choice_user == "bike": 
            #G = ox.io.load_graphml(filepath=Config.bike_dangerous)   
            G = Config.G_bike_dangerous

    elif choice_weight == "ratio safe-fast":
    
        if choice_user == "drive": 
            #G = ox.io.load_graphml(filepath=Config.drive_safest_ratio) 
            G = Config.G_drive_safest_ratio  
    
        if choice_user == "walk": 
            #G = ox.io.load_graphml(filepath=Config.walk_safest_ratio)   
            G = Config.G_walk_safest_ratio
        
        if choice_user == "bike": 
            #G = ox.io.load_graphml(filepath=Config.bike_safest_ratio)  
            G = Config.G_bike_safest_ratio
        
    #Changing the type of a few attributes    
    G = change_type(G)
    
    return G

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
    print(type(G))
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


>>>>>>> 8a9dbf678e2df3507f910f755eb11d9ab30a570a

def reverseGeocode(coordinates):
    """ Take lat and long coord and give back the name of the place.
    param:
        coordinates(tuple) : lat and long.
    
    return:
        Name of the place.

    """ 
    result = rg.search(coordinates) 
    
    return result[0]["name"]