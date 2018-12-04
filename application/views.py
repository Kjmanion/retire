from application import app
from flask import render_template, jsonify, redirect, url_for, request, jsonify
from .forms import *
from .models import *
import re
import psycopg2



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
    tornadoStatement = """SELECT row_to_json(fc)
        FROM ( SELECT 'FeatureCollection' AS type, array_to_json(array_agg(f)) As features
        FROM (SELECT 'Feature'  as type
        , ST_AsGeoJSON(tor.geom)::json as geometry
        , row_to_json((SELECT t FROM (SELECT mag, date) AS t
            )) AS properties
            FROM tornadoes as tor INNER JOIN states2 
            ON ST_Intersects(states2.geom, tor.geom)
            WHERE states2.name = '{}' AND tor.yr > {} AND tor.yr < {}
        ) AS f ) AS fc""".format(req['state'], req['afterYear'], req['beforeYear'])
    state2 = session.execute(statement).first()
    tornadoes = session.execute(tornadoStatement).fetchall()
    return jsonify(result2=[dict(row) for row in tornadoes], result=state2.geom, name=state2.name, center=state2.centroid)