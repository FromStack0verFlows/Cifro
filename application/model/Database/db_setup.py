import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()
basedir = os.path.abspath(os.path.dirname(__file__))

engine = create_engine('sqlite:///' + basedir + '/tmp/LCT.db')

Base.metadata.create_all(engine)

DBSession = sessionmaker(bind=engine)
session = DBSession()