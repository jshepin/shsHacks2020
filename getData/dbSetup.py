## script to build and establish structure of zipcodes and relevant carbon emisions data
## written by johnny burrer

from sqlalchemy import Column,Integer,String,Boolean,create_engine
from sqlalchemy.ext.declarative import declarative_base
Base=declarative_base()

## class to define 'data' table in database

class Zipcode(Base):
    __tablename__='data'
    zipcode=Column(String(15),primary_key=True)
    emissions=Column(String(20),primary_key=True)
    pop=Column(String(20),primary_key=True)
    popDensity=Column(String(20),primary_key=True)
    income=Column(String(10),primary_key=True)
    latitude=Column(String(10),primary_key=True)
    longitude=Column(String(10),primary_key=True)

## creates database

#engine=create_engine('mysql+pymysql://garageapp:nega5897@localhost/shshacks2020')
engine=create_engine('mysql+pymysql://root:R0man5 0416@localhost/zipcodeDB')
Base.metadata.create_all(engine)
