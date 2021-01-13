
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter


import geopy.geocoders
import reverse_geocoder as rg


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
    geopy.geocoders.options.default_timeout = None
    geolocator = Nominatim(user_agent="nyc-navigation", scheme='http')
    
    #Getting the location
    location = geolocator.geocode(place)
    
    #Getting latitude and longitude
    latitude = location.latitude
    longitude = location.longitude
    
    return latitude, longitude 


def verif_user_input(location_start:str,location_to:str):

    """Function to determine the types of user input

    Args:
        location_start (str): a location or two numbers separated by a space
        location_to (str): a location or two numbers separated by a space

    return a list two tuples [(lat_start,long_start),(lat_to,long_to)]
    """
    
    # Detect the first input type and change change it if needed.
    if location_start[0] == "(":
        
        location_start = location_start.split(",")
        
        long_start = location_start[1]
        long_start = long_start[:-1]
        long_start = float(long_start)
        
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
        
        lat_to = location_to[0]
        lat_to = lat_to[1:]
        lat_to = float(lat_to)

        coord_to = (lat_to, long_to)

    else:

        coord_to = lat_long_place(location_to)
    
    # Make a list with the results.
    result = [coord_start, coord_to]

    return result

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

    """

    # Dectect if the two entries are the same.
    if entry_one == entry_two:
        return False, "Same entries"
    
    # Detect if the entries are valid.
    if entry_one[0] != "(":
        try:
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

def reverseGeocode(coordinates):
    """ Take lat and long coord and give back the name of the place.
    param:
        coordinates(tuple) : lat and long.
    
    return:
        Name of the place.

    """ 
    result = rg.search(coordinates) 
    
    return result[0]["name"]