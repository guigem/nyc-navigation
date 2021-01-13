import osmnx as ox
import osmnx

from app.config import Config

from app.location_moderator import change_type


def ratio(safe: bool = True, choice_user: str = "drive") -> classmethod:
    """
    Create graphs of New York with a new attribute that is a mix between safety and speed to go from A to B.

    Parameters
    ----------
    safe : bool, optional
        If true, the user wants the safest path. The default is True.
    choice_user : str, optional
        What movement type the user takes. The default is "drive".

    Returns
    -------
    classmethod
        Returns a network with a score updates.

    """
    if safe:

        if choice_user == "drive":
            G = ox.io.load_graphml(filepath=Config.drive_safest)

        if choice_user == "walk":
            G = ox.io.load_graphml(filepath=Config.walk_safest)

        if choice_user == "bike":
            G = ox.io.load_graphml(filepath=Config.bike_safest)

    else:

        if choice_user == "drive":
            G = ox.io.load_graphml(filepath=Config.drive_dangerous)

        if choice_user == "walk":
            G = ox.io.load_graphml(filepath=Config.walk_dangerous)

        if choice_user == "bike":
            G = ox.io.load_graphml(filepath=Config.bike_dangerous)

    # Changing type of a few attributes
    G = change_type(G)

    # Generate list of edges
    edges = list(G.edges(keys=True, data=True))

    # Initiate the maximums values
    max_travel_time = 1
    max_danger = 1

    # Finding the max value for each attribute
    for i in range(len(edges)):
        danger_score = edges[i][3]["danger"]
        travel_time_score = edges[i][3]["travel_time"]

        if danger_score > max_danger:
            max_danger = danger_score

        if travel_time_score > max_travel_time:
            max_travel_time = travel_time_score

    # Dividing attributes danger and travel_time by their maximums, then add them to do a mix score
    for i in range(len(edges)):

        edges[i][3]["danger"] = edges[i][3]["danger"] / max_danger
        edges[i][3]["travel_time"] = edges[i][3]["travel_time"] / travel_time_score

        edges[i][3]["ratio"] = edges[i][3]["danger"] + edges[i][3]["travel_time"]

    # Save the network as a grphml file
    osmnx.io.save_graphml(G, filepath="bike_safest_ratio.graphml")

    return G


ratio(True, "bike")
