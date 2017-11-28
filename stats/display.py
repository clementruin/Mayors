import pandas as pd
import sqlalchemy
import csv
import requests
from bs4 import BeautifulSoup
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import sessionmaker
from sqlalchemy import MetaData, Table
from sqlalchemy.orm import mapper
import re
import unidecode
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
import matplotlib.pyplot as plt
import numpy as np
import math

color = dict()
color['PCF'] = "#800000"
color['FG'] = "#800000"
color['PS'] = "#FF0000"
color['DVG'] = "#FF6564"
color['PRG'] = "#F79295"
color['EELV'] = "#1DCD40"
color['MoDem'] = "#9F66C2"
color['UDI'] = "#9F66C2"
color['DVD'] = "#9EA0FF"
color['UMP-LR'] = "#0000FF"
color['FN'] = "#000080"
color['NA'] = "#000000"
color['SE'] = "#E8ECC1"

class Mairies():
    __tablename__ = 'mairies'
    __table_args__ = {'autoload':True}

    def __init__(self, insee_code, postal_code, city, population, latitude, longitude, first_name, last_name, birthdate, first_mandate_date, party):
        self.insee_code = insee_code
        self.postal_code = postal_code
        self.city = city
        self.population = population
        self.latitude = latitude
        self.longitude = longitude
        self.first_name = first_name
        self.last_name = last_name
        self.birthdate = birthdate
        self.first_mandate_date = first_mandate_date
        self.party = party


engine = create_engine('sqlite:///{}'.format(dump_database), echo=False)
metadata = MetaData(engine)
mairies = Table('mairies', metadata, autoload=True)
mapper(Mairies,mairies)
Session = sessionmaker(bind=engine)
session = Session()

def data_frame(query, columns):
    """Takes a sqlalchemy query and a list of columns, returns a dataframe.
    """
    def make_row(x):
        return dict([(c, getattr(x, c)) for c in columns])
    return pd.DataFrame([make_row(x) for x in query])


# dataframe with all fields in the table
def builder():
    query = session.query(Mairies).all()
    print(query)
    df = data_frame(query,
                    ["insee_code",
                     "postal_code",
                     "city",
                     "population",
                     "latitude",
                     "longitude",
                     "last_name",
                     "first_name",
                     "birthdate",
                     "first_mandate_date",
                     "party"])
    df["population"] = df["population"].apply(pd.to_numeric)

