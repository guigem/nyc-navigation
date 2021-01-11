

def guillaume(location:str):
    return "longitude/latitude"


def verif_user_input(location_start:str,location_to:str):#(45.2 75.2)
    """Function to determine if the types of user input

    Args:
        location_start (str): a location or two numbers separated by a space
        location_to (str): a location or two numbers separated by a space
    
    return a list two tuples [(lat_start,long_start),(lat_to,long_to)]
    """
#regex
    if location_start[0]=="(":
        location_start = location_start.split(" ")
        long_start = location_start[0]
        lat_start = location_start[1]
        return (long_start,lat_start)
    else:
        coord = guillaume(location_start)
        return coord

print(verif_user_input("(45.24546 45.2)","é"))