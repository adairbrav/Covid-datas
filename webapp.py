from flask import Flask, request, render_template, flash
from markupsafe import Markup

import os
import json

app = Flask(__name__)

@app.route('/')
def render_main():
    return render_template('home.html')

@app.route('/Graph')
def render_Graph():
    return render_template('Graph.html')
    
@app.route('/About')
def render_About():
    states = get_state_options()
    #print(states)
    return render_template('About.html', state_options=states)    

@app.route('/showFact')
def render_fact():
    states = get_state_options()
    state = request.args.get('state')
    county = county_most_under_18(state)
    fact = "In " + state + ", the cases in this country is " + county + "."
    return render_template('About.html', state_options=states, funFact=fact)
    
def get_state_options():
    """Return the html code for the drop down menu.  Each option is a state abbreviation from the demographic data."""
    with open('covid.json') as covid_data:
        counties = json.load(covid_data)
    states=[]
    for c in counties:
        if c["State"] not in states:
            states.append(c["State"])
    options=""
    for s in states:
        options += Markup("<option value=\"" + s + "\">" + s + "</option>") #Use Markup so <, >, " are not escaped lt, gt, etc.
    return options

def county_most_under_18(state):
    """Return the name of a county in the given state with the highest percent of under 18 year olds."""
    with open('covid.json') as covid_data:
        counties = json.load(covid_data)
    highest=0
    county = ""
    for c in counties:
        if c["State"] == state:
            if c["Age"]["Percent Under 18 Years"] > highest:
                highest = c["Age"]["Percent Under 18 Years"]
                county = c["County"]
    return county



def is_localhost():
    """ Determines if app is running on localhost or not
    Adapted from: https://stackoverflow.com/questions/17077863/how-to-see-if-a-flask-app-is-being-run-on-localhost
    """
    root_url = request.url_root
    developer_url = 'http://127.0.0.1:5000/'
    return root_url == developer_url


if __name__ == '__main__':
    app.run(debug=False) # change to False when running in production
