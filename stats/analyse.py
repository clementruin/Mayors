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


######### Input #########
dump_database = "static/database.db"
#########################

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


def pop_per_party(range):
    # population under each party
    pop = df.loc[:, ['population', 'party', 'city']]
    pop = pop[pop.population >= range[0]][pop.population <=
                                          range[1]].groupby("party").sum().sort_values("population")
    total_pop = pop['population'].sum()
    pop["percentage"] = pop["population"].apply(lambda x: x / total_pop * 100)
    print(pop)

def party_vs_citysize1(df):
    print('Donne le nombre de mairies (%) en fonction de la taille de la ville')
    Sizes = [
        0,
        200,
        600,
        1000,
        5000,
        10000,
        30000,
        70000,
        100000,
        300000,
        1000000,
        2000000]
    Parties = ["UMP-LR", "PS", "DVD", "NA", "DVG", "SE"]
    colors = [color[p] for p in Parties]
    n = len(Sizes)
    A = []
    df_pop = df.loc[:, ['city', 'party','population']]
    for k in range(0,len(Sizes)-1):
        L = []
        total_mairies = df_pop['city'][df_pop.population >= Sizes[k]][df_pop.population < Sizes[k+1]].count()
        for p in Parties:
            n_pop = df_pop[df_pop.population >= Sizes[k]][df_pop.population < Sizes[k+1]][df_pop.party == p]
            n_pop = n_pop['city'].count() / total_mairies * 100
            L.append(n_pop)
        A.append(L)

    df = pd.DataFrame(A, index=Sizes[:-1], columns=Parties)
    df.plot.bar(color=colors)
    plt.xticks(rotation=0)
    plt.title("Parties VS city size")
    plt.xlabel("taille des villes")
    plt.ylabel("nombre de mairies (%)")
    plt.show()


def party_vs_citysize2(df):
    print('Donne le % de la population par partie en fonction de la taille de la ville')
    Sizes = [
        0,
        200,
        600,
        1000,
        5000,
        10000,
        30000,
        70000,
        100000,
        300000,
        1000000,
        2000000]
    Parties = ["UMP-LR", "PS", "DVD", "NA", "DVG", "SE"]
    colors = [color[p] for p in Parties]
    n = len(Sizes)
    A = []
    df_pop = df.loc[:, ['population', 'party']]
    for k in range(0,len(Sizes)-1):
        L = []
        total_pop = df_pop['population'][df_pop.population >= Sizes[k]][df_pop.population < Sizes[k+1]].sum()
        for p in Parties:
            n_pop = df_pop[df_pop.population >= Sizes[k]][df_pop.population < Sizes[k+1]][df_pop.party == p]
            n_pop = n_pop['population'].sum() / total_pop * 100
            L.append(n_pop)
        A.append(L)
    df = pd.DataFrame(A, index=Sizes[:-1], columns=Parties)
    df.plot.bar(color=colors)
    plt.xticks(rotation=0)
    plt.title("Parties VS city size")
    plt.xlabel("taille des villes")
    plt.ylabel("pourcentage de la population par parti")
    plt.show()


#----- main -----#
#population_threshold = [0, 1000000]
#pop_per_party(population_threshold)
#party_vs_citysize1(df)

def main(arg):
    builder()
    print("analyse")
