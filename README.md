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

## Why
Give the possibility to find the safer way in New York according to the mode of transport (bike, drive and walk)

## How

### CSV file used
- Use the [NYC dataset completed] (./CSV/data_100000_out_final.csv)
- Standardize the street names.

### Calcul danger scores
- Create a danger scores per street by mode of transport :  start score with 1 as an accident,  if at least one person was injured we add 1 to the score,  if at least one person was killed we add 2 to the score.  The higher the score is the most dangerous street

### Features
- Graphical interface on a browser to enter coordinates GPS or adress between 2 points, mode of transport (bike, drive and walk) and choose between the least dangerous or most dangerous path
- Create a graph of edges and vertices mapping to roads and intersections
- Apply an algorithm to find the *least dangerous path*  between two streets and/or coordinates.
- Build a graphical interface that shows the *least dangerous path* on a map of New York

### Deployment 
