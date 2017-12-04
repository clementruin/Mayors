import pandas as pd
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
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


def dist_cities_vs_party(df):
    """graph of the distribultion of city halls under each party for different city sizes
    """
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
    Parties = [
        "FN",
        "UMP-LR",
        "DVD",
        "UDI",
        "MoDem",
        "SE",
        "EELV",
        "PRG",
        "DVG",
        "PS",
        "FG",
        "PCF",
        "NA"]
    colors = [color[p] for p in Parties]
    n = len(Sizes)
    A = []
    df_pop = df.loc[:, ['city', 'party', 'population']]
    for k in range(0, len(Sizes) - 1):
        L = []
        total_mairies = df_pop['city'][df_pop.population >=
                                       Sizes[k]][df_pop.population < Sizes[k + 1]].count()
        for p in Parties:
            n_pop = df_pop[(df_pop.population >= Sizes[k]) & (
                df_pop.population < Sizes[k + 1]) & (df_pop.party == p)]
            n_pop = n_pop['city'].count() * 100 / total_mairies
            L.append(n_pop)
        A.append(L)

    df = pd.DataFrame(
        A,
        index=[
            "0-200",
            "200-600",
            "600-1000",
            "1000-5000",
            "5000-10000",
            "10000-30000",
            "30000-70000",
            "70000-100000",
            "100000-300000",
            "300000-1000000",
            "1000000-2000000"],
        columns=Parties)
    df.plot.bar(color=colors)
    plt.gca().yaxis.grid(True, linestyle='dashed')
    plt.xticks(rotation=0)
    plt.title("Mairies sous chaque parti, selon les tailles de villes")
    plt.xlabel("taille des villes")
    plt.xticks(rotation=45)
    plt.ylabel("nombre de mairies (%)")
    plt.show()


def dist_pop_vs_party(df):
    """graph of the distribultion of population under each party for different city sizes
    """
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
    Parties = [
        "FN",
        "UMP-LR",
        "DVD",
        "UDI",
        "MoDem",
        "SE",
        "EELV",
        "PRG",
        "DVG",
        "PS",
        "FG",
        "PCF",
        "NA"]
    colors = [color[p] for p in Parties]
    n = len(Sizes)
    A = []
    df_pop = df.loc[:, ['population', 'party']]
    for k in range(0, len(Sizes) - 1):
        L = []
        total_pop = df_pop['population'][df_pop.population >=
                                         Sizes[k]][df_pop.population < Sizes[k + 1]].sum()
        for p in Parties:
            n_pop = df_pop[(df_pop.population >= Sizes[k])
                           & (df_pop.population < Sizes[k + 1])
                           & (df_pop.party == p)]
            n_pop = n_pop['population'].sum() / total_pop * 100
            L.append(n_pop)
        A.append(L)
    #df = pd.DataFrame(A, index=Sizes[:-1], columns=Parties)
    df = pd.DataFrame(
        A,
        index=[
            "0-200",
            "200-600",
            "600-1000",
            "1000-5000",
            "5000-10000",
            "10000-30000",
            "30000-70000",
            "70000-100000",
            "100000-300000",
            "300000-1000000",
            "1000000-2000000"],
        columns=Parties)
    df.plot.bar(color=colors)
    plt.gca().yaxis.grid(True, linestyle='dashed')
    plt.xticks(rotation=45)
    plt.title("Population sous chaque parti, selon les tailles de villes")
    plt.xlabel("taille des villes")
    plt.ylabel("pourcentage de la population par parti")
    plt.show()


def main(arg):
    assert arg in ['pop_per_party', 'dist_cities_vs_party', 'dist_pop_vs_party', 'city_map'], \
        'Argument is not one of pop_per_party, dist_cities_vs_party, dist_pop_vs_party, city_map: ' + arg
    df = builder()
    if arg == "pop_per_party":
        pop_per_party([0, 10000000], df)
    if arg == "dist_cities_vs_party":
        dist_cities_vs_party(df)
    if arg == "dist_pop_vs_party":
        dist_pop_vs_party(df)
    if arg == "city_map":
        city_map(df)
