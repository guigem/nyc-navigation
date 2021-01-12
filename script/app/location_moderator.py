
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

    """Function to determine if the types of user input

    Args:
        location_start (str): a location or two numbers separated by a space
        location_to (str): a location or two numbers separated by a space

    return a list two tuples [(lat_start,long_start),(lat_to,long_to)]
    """
    
    if location_start[0]=="(":
        
        location_start = location_start.split(",")
        
        long_start = location_start[1]
        long_start = long_start[:-1]
        long_start = float(long_start)
        
        lat_start = location_start[0]
        lat_start = lat_start[1:]
        lat_start = float(lat_start)
        
        location_to = location_to.split(",")
        long_to = location_to[1]
        long_to = long_to[:-1]
        long_to = float(long_to)
        
        lat_to = location_to[0]
        lat_to = lat_to[1:]
        lat_to = float(lat_to)

        return (lat_start, long_start), (lat_to, long_to)

    else:
        
        coord_start = lat_long_place(location_start)
        coord_end = lat_long_place(location_to)
        print(coord_start,coord_end)
        return coord_start, coord_end

def change_type(G):
    edges = list(G.edges(keys=True, data=True))

    for i in range(len(edges)):
        
        edges[i][3]["danger"] = int(edges[i][3]["danger"])
        edges[i][3]["travel_time"] = float(edges[i][3]["travel_time"])
        try:
            edges[i][3]["ratio"] = float(edges[i][3]["ratio"])
        except:
            continue
        
    return G


