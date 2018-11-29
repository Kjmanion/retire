from application import app
from flask import render_template, jsonify, redirect, url_for, request, jsonify
from .forms import *
from .models import *
import re



@app.route('/', methods=['GET'])
def home():
    form = StateForm(request.form)
    statement = 'SELECT gid, name FROM states2 ORDER BY name'
    states = session.execute(statement)
    form.selections.choices = [(state.gid, state.name) for state in states]
    form.description = 'Select a state'
    return render_template('base.html', form=form)


@app.route('/test', methods=['GET', 'POST'])
def test():
    req = request.get_json()
    print (req)
    statement = "SELECT name, ST_AsGeoJson(states2.geom) as geom, ST_AsGeoJSON(ST_AsText(ST_Centroid(states2.geom))) as centroid FROM states2 WHERE states2.name = '{}'".format(req['state'])
    tornadoStatement = "SELECT ST_AsGeoJson(tornadoes.geom) as geom FROM tornadoes INNER JOIN states2 ON ST_Intersects(states2.geom, tornadoes.geom) WHERE states2.name = '{}' AND tornadoes.yr > {} AND tornadoes.yr < {}".format(req['state'], req['afterYear'], req['beforeYear'])
    state2 = session.execute(statement).first()
    tornadoes = session.execute(tornadoStatement).fetchall()
    #return jsonify(result=state2.geom, name=state2.name, center=state2.centroid)
    return jsonify(result2=[dict(row) for row in tornadoes], result=state2.geom, name=state2.name, center=state2.centroid)