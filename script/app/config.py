import os
import osmnx as ox
from datetime import datetime

basedir = os.path.abspath(os.path.dirname(__file__))
startTime = datetime.now()

class Config(object):
    SECRET_KEY = os.environ.get("SECRET_KEY") or "NY-NAV-BABY"

    bike_dangerous = os.path.join(basedir,"CSV\\bike_dangerous.graphml")
    bike_safest = os.path.join(basedir,"CSV\\bike_safest.graphml")
    bike_safest_ratio = os.path.join(basedir,"CSV\\bike_safest_ratio.graphml")
    drive_dangerous = os.path.join(basedir,"CSV\\drive_dangerous.graphml")
    drive_safest = os.path.join(basedir,"CSV\\drive_safest.graphml")
    drive_safest_ratio = os.path.join(basedir,"CSV\\drive_safest_ratio.graphml")
    walk_dangerous = os.path.join(basedir,"CSV\\walk_dangerous.graphml")
    walk_safest = os.path.join(basedir,"CSV\\walk_safest.graphml")
    walk_safest_ratio = os.path.join(basedir,"CSV\\walk_safest_ratio.graphml")

    print("Building Networks")
    print (datetime.now() - startTime)
    G_drive_safest = ox.io.load_graphml(filepath=drive_safest)   
    G_walk_safest = ox.io.load_graphml(filepath=walk_safest)   
    G_bike_safest = ox.io.load_graphml(filepath=bike_safest)   
    G_drive_dangerous = ox.io.load_graphml(filepath=drive_dangerous)   
    G_walk_dangerous = ox.io.load_graphml(filepath=walk_dangerous)   
    G_bike_dangerous = ox.io.load_graphml(filepath=bike_dangerous)   
    G_drive_safest_ratio = ox.io.load_graphml(filepath=drive_safest_ratio)   
    G_walk_safest_ratio = ox.io.load_graphml(filepath=walk_safest_ratio) 
    G_bike_safest_ratio = ox.io.load_graphml(filepath=bike_safest_ratio)   
    print(datetime.now() - startTime)
    print("Networks Built")

if __name__ == "__main__":
    print(basedir)
    print(Config.bike_dangerous)