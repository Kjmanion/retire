from application import app
from sqlalchemy import create_engine, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey, Float
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import relationship
from geoalchemy2 import Geometry
engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()

class States(Base):
    __tablename__ = 'states'
    gid = Column(Integer, primary_key=True)
    statefp = Column(String)
    statens = Column(String)
    affgeoid = Column(String)
    geoid = Column(String)
    stusps = Column(String)
    name = Column(String)
    lsad = Column(String)
    aland = Column(Float)
    awater = Column(Float)
    geom = Column(Geometry(geometry_type='polygon', srid=4326))