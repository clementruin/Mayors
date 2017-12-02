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
from scrap.base import *


dump_database = "static/database.db"

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

def main(arg, argtype):
    engine = create_engine('sqlite:///{}'.format(dump_database), echo=False)
    Session = sessionmaker(bind=engine)
    session = Session()

    df = pd.DataFrame(session.query(Mairies.__table__).all())
    df[["postal_code", "city"]] = df[["postal_code", "city"]].astype(str) 

    if argtype == "dpt" :
        df = df[df['postal_code'].str.match(arg)]
    elif argtype == "postal_code":
        df = df[df['postal_code'].str.match(arg)]
    else :
        df = df[df['city'].str.match(arg)]
    print(df)
