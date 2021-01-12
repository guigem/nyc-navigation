
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
import geopy.geocoders


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
<<<<<<< HEAD
    
    # Detect the first input type and change change it if needed.
    if location_start[0] == "(":
=======
    if location_start[0]=="(":
>>>>>>> b58ed62d051870b56a7f415ef21f406ed21d947a
        
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
<<<<<<< HEAD

        coord_to = lat_long_place(location_to)
    
    # Make a list with the results.
    result = [coord_start, coord_to]

    return result
=======
        coord_start = lat_long_place(location_start)
        coord_end = lat_long_place(location_to)
        print(coord_start,coord_end)
        return coord_start, coord_end
>>>>>>> b58ed62d051870b56a7f415ef21f406ed21d947a

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

