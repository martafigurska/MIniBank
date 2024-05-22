from sqlalchemy.orm import sessionmaker
from tables import Base, Konto, Klient
from sqlalchemy import create_engine, URL

DRIVER_NAME = 'SQL SERVER'
SERVER_NAME = 'DESKTOP-5G3QIOB\SQL_SERVER'
DATATBASE_NAME = 'BANK1'
USERNAME = 'abcd'
PASSWORD = 'abcd@2024'

DATATBASE_STR = f'mssql://{USERNAME}:{PASSWORD}@{SERVER_NAME}/{DATATBASE_NAME}?driver={DRIVER_NAME}'

engine = create_engine(DATATBASE_STR)
connection = engine.connect()

Session = sessionmaker(bind=engine)
session = Session()

new_konto = Konto(nr_konta = 2, saldo=2000)
session.add(new_konto)
session.commit()

new_klient = Klient(
    pesel='122',
    imie='Wojciech',
    nazwisko='Grzyb',
    nr_konta=new_konto.nr_konta
)

session.add(new_klient)
session.commit()
