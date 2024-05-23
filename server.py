from fastapi import FastAPI, HTTPException
from connection import setup_database
from classes.handler import Handler

# app = FastAPI()

branch_conns = setup_database()
handler = Handler(branch_conns=branch_conns)


# query = handler.query_konto(5)
# handler.insert_konto("123", "Marta", "Figurska", 100000)
# handler.insert_konto("124", "Marta", "Prądnicka", 2)
# handler.insert_konto("125", "Ala", "Spodhala", 32)
# query = handler.query_konto(5)
# query2 = handler.query_konto(2)

handler.insert_transakcja(5, 2, 1000)

query = handler.query(5, "SELECT * FROM transakcja")
query2 = handler.query(2, "SELECT * FROM transakcja")

# query = handler.query_transakcja(5, 2)
# query2 = handler.query_transakcja(2, 5, False)

print(query)
print(query2)
