from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class Konto(Base):
    __tablename__ = "konto"

    nr_konta = Column(Integer, primary_key=True)
    saldo = Column(Float, nullable=False)

    # Define the relationship in the Konto class
    klient = relationship("Klient", back_populates="konto")

class Klient(Base):
    __tablename__ = "klient"

    pesel = Column(String, primary_key=True)
    imie = Column(String, nullable=False)
    nazwisko = Column(String, nullable=False)
    nr_konta = Column(Integer, ForeignKey("konto.nr_konta"), nullable=False)

    konto = relationship("Konto", back_populates="klient")
