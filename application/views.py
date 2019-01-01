from application import app
from flask import render_template, jsonify, redirect, url_for, request, jsonify
from .forms import *
from .models import *



@app.route('/', methods=['GET'])
def home():
    form = StateForm(request.form)
    form2 = StateForm(request.form)
    statement = 'SELECT gid, name FROM states2 ORDER BY name'
    states = session.execute(statement)
    states2 = session.execute(statement)
    form.selections.choices = [(state.gid, state.name) for state in states]
    form2.selections2.choices = [(state.gid, state.name) for state in states2]
    form.description = 'Select a state'
    form2.description = 'Or enter a city and state'
    return render_template('base.html', form=form, form2=form2)


@app.route('/getStateData', methods=['GET', 'POST'])
def getStateData():
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
    print (tornadoes)
    return jsonify(tornadoes=[dict(row) for row in tornadoes], areaOutline=state2.geom, name=state2.name, center=state2.centroid)

@app.route('/getCityData', methods=['GET', 'POST'])
def getCityData():
    req = request.get_json()
    print (type(req))
    print (req['cityChoice'])
    # query = session.query(Cities).filter(Cities.city.like(req['cityChoice']))
    # query = session.query(Cities, States).filter(Cities.state_abb==States.stpostal).filter(Cities.city.like(req['cityChoice']))
    # city = session.execute("SELECT * FROM cities WHERE city = '{}'".format('Washington'))
    # print (query)
    city = session.query(Cities, States.stpostal).join(States, States.stpostal==Cities.state_abb).filter(Cities.city==req['cityChoice'], States.name==req['state']).first()
    if city == None:
        return jsonify(tornadoes=city, areaOutline=None, center=None)
    print (city[0].latitude, city[0].longitude)
    statement = """SELECT row_to_json(fc)
        FROM (SELECT 'FeatureCollection' AS type, array_to_json(array_agg(f)) AS features
        FROM (SELECT 'Feature' AS type
        , ST_AsGeoJSON(tor.geom)::json AS geometry
        , row_to_json((SELECT t FROM (SELECT mag, date) AS t
            )) AS properties
            FROM tornadoes AS tor
            WHERE ST_Intersects(ST_Transform(tor.geom, 4326), ST_Buffer(CAST(ST_SetSRID(ST_MakePoint({},{}), 4326)AS geography), 16093.4))
        ) AS f ) AS fc""".format(city[0].longitude, city[0].latitude)
    tornadoes = session.execute(statement).fetchall()
    print (tornadoes)
    bufferGeom = 'SELECT ST_AsGeoJSON(ST_Buffer(CAST(ST_SetSRID(ST_MakePoint({}, {}), 4326)AS geography), 16093.4)) AS geom, ST_AsGeoJSON(ST_AsText(ST_MakePoint({}, {}))) as center'.format(city[0].longitude, city[0].latitude, city[0].longitude, city[0].latitude)
    buffered = session.execute(bufferGeom).first()
    print (buffered)
    coordinates = [city[0].longitude, city[0].latitude]
    print (coordinates)

    return jsonify(tornadoes=[dict(row) for row in tornadoes], areaOutline=buffered.geom, center=buffered.center)
    

@app.route('/about', methods=['GET'])
def about():
    return render_template('about.html', title='About this page')