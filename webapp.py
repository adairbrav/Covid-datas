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
    Country = get_Countrys_options()
    #print(Country)
    return render_template('About.html', Country_options=Country)    

@app.route('/showFact')
def render_fact():
    Counts = get_Countrys_options()
    Country = request.args.get('Country')
    county = cases(Country)
    fact = "In " + Country + ", the cases in this country is " +str(county) + "."
    return render_template('About.html', Country_options=Counts, funFact=fact)
    
def get_Countrys_options():
    """Return the html code for the drop down menu.  Each option is a state abbreviation from the demographic data."""
    with open('covid.json') as covid_data:
        counties = json.load(covid_data)
    Countrys=[]
    for c in counties:
        if c["Location"] ["Country"] not in Countrys:
            Countrys.append(c["Location"] ["Country"])
    options=""
    for s in Countrys:
        options += Markup("<option value=\"" + s + "\">" + s + "</option>") #Use Markup so <, >, " are not escaped lt, gt, etc.
    return options

def cases(Country):
    """Return the name of a county in the given state with the highest percent of under 18 year olds."""
    with open('covid.json') as covid_data:
        counties = json.load(covid_data)
    total=0
    for c in counties:
        if c["Location"] ["Country"] == Country:
            total = total+ c ["Data"] ["Cases"]
    return total
    


def is_localhost():
    """ Determines if app is running on localhost or not
    Adapted from: https://stackoverflow.com/questions/17077863/how-to-see-if-a-flask-app-is-being-run-on-localhost
    """
    root_url = request.url_root
    developer_url = 'http://127.0.0.1:5000/'
    return root_url == developer_url


if __name__ == '__main__':
    app.run(debug=False) # change to False when running in production
