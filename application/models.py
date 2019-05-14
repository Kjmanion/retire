from application import app
from sqlalchemy import create_engine, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey, Float
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import relationship
from geoalchemy2 import Geometry
#engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
engine = create_engine('postgresql+psycopg2://postgres:postgres@localhost:5432/flaskapp')
#engine = create_engine('postgresql+psycopg2://kevinjmanion1:RhinoPanda31#@tornado.ccbdcmchyxvb.us-east-2.rds.amazonaws.com:5432/tornado')
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()


class States(Base):
    __tablename__ = 'states2'
    gid = Column(Integer, primary_key=True)
    statefp = Column(String)
    stusps = Column(String, ForeignKey('Cities.stateabb'))
    name = Column(String)
    geom = Column(Geometry(geometry_type='polygon', srid=4269))
    
    
class Tornadoes(Base):
    __tablename__ = 'tornadoes'
    gid = Column(Integer, primary_key=True)
    om = Column(Integer)
    yr = Column(Integer)
    mo = Column(Integer)
    date = Column(String)
    time = Column(String)
    tz = Column(Integer)
    st = Column(String)
    stf = Column(Integer)
    mag = Column(Integer)
    inj = Column(Integer)
    fat = Column(Integer)
    loss = Column(Float)
    closs = Column(Float)
    slon = Column(Float)
    slat = Column(Float)
    elon = Column(Float)
    elat = Column(Float)
    len = Column(Float)
    wid = Column(Integer)
    kind = Column(String)
    stroke = Column(String)
    geom = Column(Geometry(geometry_type='line', srid=4269))

class Cities(Base):
    __tablename__ = 'cities'
    id = Column(Integer, primary_key=True)
    cityname = Column(String)
    stateabb = Column(String, ForeignKey("States.stusps"))
    lat= Column(Float)
    lon = Column(Float)
