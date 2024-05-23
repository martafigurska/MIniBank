from fastapi import FastAPI, HTTPException
from connection import setup_database
from classes.handler import Handler

# app = FastAPI()

branch_conns = setup_database()
handler = Handler(branch_conns=branch_conns)


# handler.insert_konto("123", "Marta", "Figurska", 100000)
# handler.insert_konto("124", "Marta", "Prądnicka", 2)
# handler.insert_konto("135", "Ala", "Makota", 3123)
# query = handler.query_konto(1)
# query2 = handler.query_konto(3)

# handler.insert_transakcja(1, 2, 10)

# query = handler.query(1, "SELECT * FROM transakcja")
# query2 = handler.query(3, "SELECT * FROM transakcja")

# query = handler.query_transakcja(1, 2)
# query2 = handler.query_transakcja(2, 1)

# print(query)
# print(query2)
