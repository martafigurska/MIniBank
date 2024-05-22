from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class Konto(Base):
    __tablename__ = "Konto"

    nr_konta = Column(Integer, primary_key=True, autoincrement=True)
    saldo = Column(Float, nullable=False)


class Klient(Base):
    __tablename__ = "Klient"

    pesel = Column(String, primary_key=True)
    imie = Column(String, nullable=False)
    nazwisko = Column(String, nullable=False)
    nr_konta = Column(Integer, ForeignKey("Konto.nr_konta"), nullable=False)

    konto = relationship("Konto")
