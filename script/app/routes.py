from flask import render_template,url_for,redirect, render_template_string
import osmnx as ox
import folium


from script.app.location_moderator import verif_user_input, choose_right_network, compute_route
from script.app import navig
from script.app.forms import Location


<<<<<<< HEAD
=======

>>>>>>> defd7fbdc39a01f55af609e2da27c8f8565a8809
@navig.route('/')
@navig.route('/index')
def index():
    return render_template("index.html" , title="Index")

@navig.route("/about")
def about():
    return render_template("about.html", title="About")

@navig.route("/authors")
def authors():
    return render_template("authors.html", title = "The Authors")

@navig.route("/error/<error_type>")
def error(error_type:str):
    return render_template("error.html",title="Error",error_type=error_type)

@navig.route("/nav",methods=["GET", "POST"])
def nav():

    form = Location()
    

    if form.validate_on_submit():
        #forms fields
        location_start = form.location_start.data
        location_to = form.location_to.data
        choice_user = form.transportation.data
        choice_weight = form.pick.data

        print(location_start,location_to,choice_user,choice_weight)
        
        #call error_raiser function:
            #if true: cool
            #if false : return error.html
        return redirect(url_for("error",error_type="TESTING"))

        return redirect(url_for("road",location_start=location_start,
                                        location_to=location_to,
                                        choice_user=choice_user,
                                        choice_weight = choice_weight))

    return render_template("nav.html" , title = "Ny-Nav",form=form)

@navig.route("/road/<location_start>/<location_to>/<choice_user>/<choice_weight>")
def road(location_start:str,location_to:str,choice_user:str,choice_weight:str):
    '''
    

    Parameters
    ----------
    location_start : str
        String with starting point as coordinates or place.
    location_to : str
        String with ending point as coordinates or place.
    choice_user : str
        DESCRIPTION.
    choice_weight : str
        What movement type the user takes.

    Returns
    -------
    Web page
        Returns a html page with the open street map.

    '''
    
    
    #Selecting the right network based on the user choice
    G = choose_right_network(choice_weight,choice_user)

    print('Datas passed : \n{} \n{} \n{} \n{}'.format(location_start,location_to,choice_user,choice_weight))
    
    #Generate the tuples with the right coordinates for the starting and ending points
    start = verif_user_input(location_start, location_to)[0]
    end = verif_user_input(location_start,location_to)[1]
    
    #Computing the nearest node based on the tuples given just above
    start_node = ox.get_nearest_node(G, start) 
    end_node = ox.get_nearest_node(G, end)
    
    #Computing the optimal route for our path
    route = compute_route(G, start_node, end_node, choice_weight)       
    
    #Drawing the path on an open map street 
    folium_map = ox.folium.plot_route_folium(G, route=route, popup_attribute="length", tiles="openstreetmap", route_color="blue")
    
    #DRawing markers to show in green the starting point and in red the ending point
    start = list(start)
    end = list(end)
    folium.Marker(location = start, popup="Start", icon=folium.Icon(color='green')).add_to(folium_map)
    folium.Marker(location = end, popup="End", icon=folium.Icon(color='red')).add_to(folium_map)
    
    #Saving the folium map as html
    folium_map.save("folium_map.html")
    
    
    #return render_template("road.html",title ="Path", div=div)

    #Returning the map in the html
    return render_template_string('''
        <head>
            <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>    
        </head>
            <body>
        {{ div_placeholder|safe }}
            </body>''', div_placeholder=folium_map._repr_html_())
    


    