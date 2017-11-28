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

dump_database = "static/database.db"


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

df = pd.DataFrame(session.query(mairies).all())

color = dict()
color['PCF'] = "#DA1016"
color['FG'] = "#DA1016"
color['PS'] = "#F79295"
color['DVG'] = "#F79295"
color['PRG'] = "#F79295"
color['EELV'] = "#1DCD40"
color['MoDem'] = "#9F66C2"
color['UDI'] = "#9F66C2"
color['DVD'] = "#3ECBF9"
color['UMP-LR'] = "#3ECBF9"
color['FN'] = "#3334E1"
color['NA'] = "#D8D8F3"
color['SE'] = "#E8ECC1"

def city_map():
    Latitudes = df.as_matrix(columns=df.columns[4:5])
    Longitudes = df.as_matrix(columns=df.columns[5:6])
    Partys = df.as_matrix(columns=df.columns[10:11])

    fig, ax = plt.subplots()
    for i in range(0, len(Latitudes)):
        if Latitudes[i][0] == "None":
            latitude = (-np.cos(48.8 * np.pi / 180))
        else:
            latitude = -np.cos(float(Latitudes[i][0]) * np.pi / 180)

        if Longitudes[i][0] == "None":
            longitude = np.sin(2.02 * np.pi / 180)
        else:
            longitude = np.sin(float(Longitudes[i][0]) * np.pi / 180)

        colour = color[Partys[i][0]]

        ax.scatter(longitude, latitude, c=colour, alpha=0.8, edgecolors='none')

    plt.show()

df.columns[4:5]
df.columns[5:6]
df.columns[10:11]