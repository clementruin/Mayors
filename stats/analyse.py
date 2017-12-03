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


engine = create_engine('sqlite:///{}'.format(dump_database), echo=False)
Session = sessionmaker(bind=engine)
session = Session()


def builder():
    """Build panda statframe
    """
    df = pd.DataFrame(session.query(Mairies.__table__).all())
    return df


def city_map(df):
    """Draw map of the cities with the color of their party
    """
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


def pop_per_party(range, df):
    """population under each party
    """
    pop = df.loc[:, ['population', 'party', 'city']]
    pop = pop[pop.population >= range[0]][pop.population <=
                                          range[1]].groupby("party").sum().sort_values("population")
    total_pop = pop['population'].sum()
    pop["percentage"] = pop["population"].apply(lambda x: x / total_pop * 100)
    print(pop)


def party_vs_citysize1(df):
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
    df_pop = df.loc[:, ['city', 'party', 'population']]
    for k in range(0, len(Sizes) - 1):
        L = []
        total_mairies = df_pop['city'][df_pop.population >=
                                       Sizes[k]][df_pop.population < Sizes[k + 1]].count()
        for p in Parties:
            n_pop = df_pop[df_pop.population >= Sizes[k]
                           ][df_pop.population < Sizes[k + 1]][df_pop.party == p]
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
    for k in range(0, len(Sizes) - 1):
        L = []
        total_pop = df_pop['population'][df_pop.population >=
                                         Sizes[k]][df_pop.population < Sizes[k + 1]].sum()
        for p in Parties:
            n_pop = df_pop[df_pop.population >= Sizes[k]
                           ][df_pop.population < Sizes[k + 1]][df_pop.party == p]
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
# pop_per_party(population_threshold)
# party_vs_citysize1(df)

def main(arg):
    assert arg in ['pop_per_party', 'party_vs_citysize1', 'party_vs_citysize2', 'city_map'], \
        'Argument is not one of pop_per_party, party_vs_citysize1, party_vs_citysize2, city_map: ' + arg
    df = builder()
    if arg == "pop_per_party":
        pop_per_party([0, 10000000], df)
    if arg == "party_vs_citysize1":
        party_vs_citysize1(df)
    if arg == "party_vs_citysize2":
        party_vs_citysize2(df)
    if arg == "city_map":
        city_map(df)
