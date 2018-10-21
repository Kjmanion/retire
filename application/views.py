from application import app
from flask import render_template, jsonify, redirect, url_for, request, jsonify
from .forms import *
from .models import *
import re



@app.route('/', methods=['GET'])
def home():
    return redirect(url_for('getStates'))

@app.route('/getStates', methods=['GET', 'POST'])
def getStates():
    form = StateForm(request.form)
    states = session.query(States).all()
    form.selections.choices = [(state.gid, state.name) for state in states]
    form.description = 'Select a state'
    if request.method == 'POST':
        print ('Making a post request!')
        state_id = form.selections.data
        state = session.query(States).get(state_id)
        print (state.name)
        statement = "SELECT name, ST_AsText(ST_Centroid('{}')) as geom FROM states WHERE states.name = '{}'".format(state.geom, state.name)
        state2 = session.execute(statement).first()
        print (state2)
        print (state2.geom)
        statement2 = """
        SELECT row_to_json(fc)
            FROM (SELECT 'FeatureCollection' As type, array_to_json(array_agg(f)) as features
            FROM (SELECT 'Feature' As type
	            , ST_AsGEOJSON('{}')::json As geometry
	            , row_to_json((SELECT l FROM (SELECT name) As l
		        )) As properties
	          FROM states as lg    ) As f ) As fc;
        """.format(state.geom)
        stateGeom = session.execute(statement2)
        test = []
        print (stateGeom)
        geoJSON = ''
        for item in stateGeom:
            print (item)
            geoJSON += str(item)
            test.append(dict(item))
        geoJSON2 = str(test[0]['row_to_json'])
        # leng = len(geoJSON)
        # test2 = test[[0]'row_to_json']]
        # geoJSON = geoJSON[1:leng-2]
        newGeo = geoJSON2.replace("'", '"')
        
        
        result = re.search('\W\d+\W\d+\W\d+\W\d+', state2.geom)
        latLng = result[0].split(' ')
        print (latLng)

        
        return render_template('base.html', form=form, lng=latLng[0], lat=latLng[1], geomJson = newGeo)


    return render_template('base.html', form=form)

@app.route('/test', methods=['GET'])
def test():
    a = 5
    b = 10
    print (a + b)
    print (jsonify(a))
    return jsonify(result=a)