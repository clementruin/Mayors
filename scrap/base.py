from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import sessionmaker
from sqlalchemy import MetaData, Table
from sqlalchemy.orm import mapper

dump_database = "static/database.db"

engine = create_engine('sqlite:///{}'.format(dump_database), echo=False)
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()


class Mairies(Base):
    __tablename__ = 'mairies'
    insee_code = Column(String, primary_key=True)
    postal_code = Column(Integer)
    city = Column(String)
    population = Column(Integer)
    latitude = Column(String)
    longitude = Column(String)
    first_name = Column(String)
    last_name = Column(String)
    birthdate = Column(String)
    first_mandate_date = Column(String)
    party = Column(String)

    def __init__(
            self,
            insee_code,
            postal_code,
            city,
            population,
            latitude,
            longitude,
            first_name,
            last_name,
            birthdate,
            first_mandate_date,
            party):
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

    def __repr__(self):
        return "<Mairies(insee_code='%s', postal_code='%s', city='%s', population='%s',latitude='%s', longitude='%s', first_name='%s', last_name='%s', birthdate='%s', first_mandate_date='%s', party='%s')>" % (
            self.insee_code, self.postal_code, self.city, self.population, self.latitude, self.longitude, self.first_name, self.last_name, self.birthdate, self.first_mandate_date, self.party)


Base.metadata.create_all(engine)
