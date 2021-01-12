# nyc-navigation

## Team members - Contributors

* [Lise Amen](https://github.com/lise-amen)
* [Jonathan Decleire](https://github.com/JonathanDecleire)
* [Guillaume Gémis](https://github.com/guigem)
* [Melvin Leroy](https://github.com/Melvin-Leroy)
* [Christian Melot](https://github.com/Ezamey)

## Purpose
To create a Python script/application that, given two addresses (or coordinates) in New York city, can give the *least dangerous* path between those two points according to a client request. 

## Objectives
- Learn and apply graph theory
- Learn and apply graph traversal algorithms
- Apply basic statistics on a dataset
- Work with geolocalized data
- Work in a dev-client relationship

## How
The project consists of using the below dataset that is a snapshot of data created everyday by the police departments of NYC. This dataset includes the traffic accidents that occurred, their location, time, vehicles involved, etc. With this dataset we are able to define a danger score to each street as explained in the below section.
Based on that information and our map we have our environment of streets with their danger scores.
Our application is able to calculate different routes based on the criterias that are defined in the navigation panel and calculate the most appropriate path based on those.

### CSV file used
- Use the [NYC dataset completed](CSV/data_100000_out_final.csv)
- Standardize the street names.

### Define danger scores
- Create a danger scores per street by mode of transport :  start score with 1 as an accident,  if at least one person was injured we add 1 to the score,  if at least one person was killed we add 2 to the score.  The higher the score for a street the mpre dangerous it is.

### Features
- Graphical interface on a browser to enter GPS coordinates or address between 2 points, mode of transport (bike, drive and walk) and choice between the least dangerous, most dangerous path, and hybrid path between fastest and safest.
- Create a graph of edges and vertices mapping the roads and intersections
- Apply an algorithm to find the *least dangerous path*  between two streets and/or coordinates
- Build a graphical interface that shows the *least dangerous path* on a map of New York

### Deployment 
TO BE COMPLETED

## Run
To run this application, launch
```python
python main.py
```

## Requirements
[See requirements.txt](requirements.txt)

## When
5 days to complete (06/01/2021 PM -- 13/01/2021 AM)
