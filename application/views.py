from application import app
from flask import render_template, jsonify, redirect, url_for, request, jsonify
from .forms import *
from .models import *
import re



@app.route('/', methods=['GET'])
def home():
    form = StateForm(request.form)
    states = session.query(States).all()
    form.selections.choices = [(state.gid, state.name) for state in states]
    form.description = 'Select a state'
    return render_template('base.html', form=form)


@app.route('/test', methods=['GET', 'POST'])
def test():
    req = request.get_json()
    print (req)
    statement = "SELECT name, ST_AsGeoJson(states.geom) as geom, ST_AsGeoJSON(ST_AsText(ST_Centroid(states.geom))) as centroid FROM states WHERE states.name = '{}'".format(req['data'])
    state2 = session.execute(statement).first()
    return jsonify(result=state2.geom, name=state2.name, center=state2.centroid)