from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from connection import setup_database
from transaction_handler import TransactionHandler

app = FastAPI()

central_conn, branch_conns = setup_database()
transaction_manager = TransactionHandler(central_conn = central_conn, branch_conns = branch_conns)  # TODO: finish handler


class Transaction(BaseModel):
    ''' Class to handle transactions creation'''

    account_id: int
    balance: float


class Account(BaseModel):
    ''' Class to handle accounts creation'''

    account_id: int
    pesel: str
    first_name: str
    last_name: str
