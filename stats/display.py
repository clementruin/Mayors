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


def main(arg, argtype):
    engine = create_engine('sqlite:///{}'.format(dump_database), echo=False)
    Session = sessionmaker(bind=engine)
    session = Session()

    df = pd.DataFrame(session.query(Mairies.__table__).all())
    df[["postal_code", "city"]] = df[["postal_code", "city"]].astype(str)

    if argtype == "dpt":
        df = df[df['postal_code'].str.match(arg)]
    elif argtype == "postal_code":
        df = df[df['postal_code'].str.match(arg)]
    else:
        df = df[df['city'].str.match(arg)]
    print(df)
