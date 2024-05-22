from sqlalchemy.orm import sessionmaker
from tables import Base, Konto, Klient
from sqlalchemy import create_engine
import pypyodbc as odbc

DRIVER_NAME = 'SQL SERVER'
SERVER_NAME = ''
DATATBASE_NAME = ''
# uid=<username>
# pwd=<password>

connection_string = f'''
    DRIVER={{{DRIVER_NAME}}};
    SERVER={{{SERVER_NAME}}};
    DATABASE={{{DATATBASE_NAME}}};
    Trust_Connection=yes;
'''

conn = odbc.connect(connection_string)
print(conn)

# engine = create_engine(connection_string)
# Base.metadata.create_all(engine)
# 
# Session = sessionmaker(bind=engine)
# session = Session()
# 
# new_konto = Konto(saldo=1000.0)
# session.add(new_konto)
# session.commit()
# 
# new_klient = Klient(
#     pesel='12345678901',
#     imie='Jan',
#     nazwisko='Kowalski',
#     nr_konta=new_konto.nr_konta
# )
# session.add(new_klient)
# session.commit()
