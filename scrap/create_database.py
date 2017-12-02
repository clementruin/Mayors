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
import unidecode
import re
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
from scrap.base import *


######### Input #########
source_database = "static/insee.csv"
dump_database = "static/database.db"
dump_database_csv = "export/database.csv"
#########################


def load_session():
    """Connect with table mairies
    """
    engine = create_engine('sqlite:///{}'.format(dump_database), echo=False)
    Session = sessionmaker(bind=engine)
    session = Session()
    return session

class TableError(Exception):
    pass

# Link insee_code with postal_code and coordinates 

code_converter = {}
outfile = open('static/code_postaux_insee.csv', 'r')
reader = csv.DictReader(outfile, delimiter=';')
for line in reader:
    code_converter[line["Code_commune_INSEE"]] = [
        line["Code_postal"], line["coordonnees_gps"]]


def get_dict(code):
    try:
        return (code_converter[code][0],
                code_converter[code][1].split(',')[0],
                code_converter[code][1].split(', ')[1])
    except BaseException:
        return ("None", "None", "None")


def no_accent(string):
    string = string.replace('é','e')
    string = string.replace('è','e')
    string = string.replace('ë','e')
    string = string.replace('ï','i')
    string = string.replace('É','e')
    string = string.replace('È','e')
    return string


# Populate table 

def build_db(user_arg, user_argtype):
    """Retrieves data from the source_database and scraping function. 
    Creates rows in the Mairies table 
    """
    session = load_session()
    outfile = open(source_database, 'r')
    reader = csv.DictReader(outfile, delimiter=';')
    for line in reader:
        get = get_dict(line["codeinsee"])
        if useful_line(get[0], line["libsubcom"], user_arg, user_argtype):
            scrap = scrap_party_date(
                get[0],
                line["libsubcom"],
                line["prepsn"],
                line["nompsn"])
            print(line["codeinsee"])
            new_mayor = Mairies(insee_code= line["codeinsee"],
                postal_code=get[0],
                city=line["libsubcom"],
                population=int(line["popsubcom"]),
                latitude=get[1],longitude=get[2],
                first_name=line["prepsn"],
                last_name=line["nompsn"],
                birthdate=line["naissance"],
                first_mandate_date=scrap[0],
                party=scrap[1])
            session.add(new_mayor)
    session.commit()
    outfile.close()


def useful_line(postal_code, city, user_arg, user_argtype):
    """Check whether this city was requested by the user by comparing
    with user_arg and user_argtype
    """
    if user_argtype == 'dpt':
        return user_arg == postal_code[:-3]
    elif user_argtype == 'postal_code':
        return user_arg == postal_code
    else :
        return user_arg == city


def scrap_party_date(postal_code, city, first_name, last_name):
    """Scraps party and first mandate year of the corresponding mayor in the "Liste des maires"
    Wikitable, available on every french city's Wikipedia page
    """
    try:
        # open Wiki page of the city 
        city = unidecode.unidecode(city)
        url = "https://www.google.fr/search?q={}+{}+{}".format(
            'wikipedia', city, postal_code)
        r = requests.get(url)
        soup = BeautifulSoup(r.text, "html.parser")

        tag = soup.find_all("div", class_="kv", limit=1)
        link = tag[0].cite.text

        r = requests.get(link)
        soup = BeautifulSoup(r.text, "lxml")
        mayor_table = soup.find_all(
            "table", class_="wikitable centre communes")
        # retrieves Wikitable "Liste des maires"
        data = []
        for tables in mayor_table:
            for row in tables.find_all("tr"):
                L = row.find_all("td")
                if len(L) > 2:
                    data.append([ele.text for ele in L])
        # first date and party search 
        min_date = 4000
        min_index = None
        for i in range(len(data)):
            if fuzz.token_sort_ratio(no_accent(data[i][2]), no_accent(first_name +" "+last_name)) > 80:
                curr_date = re.search(r"(\d{4})", data[i][0]).group(1)
                if int(curr_date) < min_date:
                    min_date = int(curr_date)
                    min_index = i
        if min_index == None:
            raise TableError()
        else :
            date = re.search(r"(\d{4})", data[min_index][0]).group(1)
            party = data[min_index][3]
            return (date, clean_party_attribute(party))
    except TableError:
        print("Impossible Match in WikiTable")
        return ("NA", "NA")
    except BaseException:
        return("NA", "NA")


# Clean party name previously scrapped

def clean_party_attribute(string):
    string = no_accent(string)
    L = []
    se = ["SE", "sans etiquette", "Sans etiquette"]
    fn = ["FN", "fn", "National"]
    ump = ["UMP", "Republicains", "LR"]
    dvd = ["DVD", "Divers Droite", "divers droite", "Divers droite"]
    udi = ["UDI", "Indep"]
    modem = ["MoDem", "modem", "MODEM"]
    prg = ["PRG", "Radical"]
    eelv = ["EELV", "Ecologie", "ecologie"]
    dvg = ["DVG", "Divers Gauche", "divers gauche", "Divers gauche"]
    ps = ["PS", "Socialiste", "socialiste", "ps"]
    fg = ["FG", "fg", "Front de Gauche", "front de gauche", "Front de gauche"]
    pcf = ["PCF", "Communiste", "communiste"]

    if any(i in string for i in se):
        L.append("SE")
    if any(i in string for i in fn):
        L.append("FN")
    if any(i in string for i in ump):
        L.append("UMP-LR")
    if any(i in string for i in dvd):
        L.append("DVD")
    if any(i in string for i in udi):
        L.append("UDI")
    if any(i in string for i in eelv):
        L.append("EELV")
    if any(i in string for i in modem):
        L.append("MoDem")
    if any(i in string for i in dvg):
        L.append("DVG")
    if any(i in string for i in ps):
        L.append("PS")
    if any(i in string for i in fg):
        L.append("FG")
    if any(i in string for i in pcf):
        L.append("PCF")
    if any(i in string for i in prg):
        L.append("PRG")
    if len(L) == 0:
        return "NA"
    else:
        return L[-1]


# Create a .csv file for the .db created 

def write_csv():
    outfile = open(dump_database_csv, 'w')
    outcsv = csv.writer(outfile)
    outcsv.writerow(['insee_code',
                     'postal_code',
                     'city',
                     'population'
                     'latitude',
                     'longitude',
                     'mayor_first_name',
                     'mayor_last_name',
                     'mayor_birthdate',
                     'first_mandate_date',
                     'party'])
    records = session.query(Mairies).all()
    session.commit()
    [outcsv.writerow([getattr(curr, column.name)
                      for column in Mairies.__table__.columns]) for curr in records]
    outfile.close()

# Correction for cities with undefined party

def party_correction(insee_code, city):
    """Scraps LeMonde.fr in the "Les Élus" section of the city's page.
    Request "Le monde city insee_code" in Google to access the page
    """
    try:
        r = requests.get(
            "https://www.google.fr/search?q={}+{}+{}+{}".format('le', 'monde', city, insee_code))
        soup = BeautifulSoup(r.text, "html.parser")
        head3 = soup.find_all("h3", class_="r", limit=1)
        link = head3[0].a['href']
        link = link.split('=')[1].split('&')[0]
        link = link.split(insee_code)[0] + insee_code

        r = requests.get(link)
        soup = BeautifulSoup(r.text, "lxml")
        div = soup.find_all("div", class_="elu-principal")
        party = div[0].ul.li.br.next_sibling
        return party
    except BaseException:
        return "NA"

def correct():
    rows = session.query(Mairies).filter(Mairies.party == "NA").all()
    count = session.query(Mairies).filter(Mairies.party == "NA").count()
    print("{} cities with undefined party".format(count))
    while count>0:
        answer = input("Do you want to try a potentially long correction? (yes/no) : ")
        try:
            if valid_answer(answer):
                for row in rows :
                    row.party = clean_party_attribute(party_correction(row.insee_code, row.city))
                    print(row.city, row.party, row.population)
            break
        except Illegal:
            print("illegal, answer yes or no")
    session.commit()


def valid_answer(string):
    if string == "yes":
        return True
    elif string == "no":
        return False 
    else :
        raise Illegal 


class Illegal(Exception):
    pass
    

# Run script 

def main(user_arg, user_argtype):
    build_db(user_arg, user_argtype)
    correct()
    write_csv()
    print("Database successfully created")