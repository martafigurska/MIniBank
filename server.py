from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from connection import setup_database
from transaction_handler import TransactionHandler

app = FastAPI()

branch_conns = setup_database()
transaction_manager = TransactionHandler(branch_conns = branch_conns)  # TODO: finish handler



class Transaction(BaseModel):
    ''' Class to handle transactions'''

    src_account: int
    des_account: int
    amount: float


class Account(BaseModel):
    ''' Class to handle accounts'''

    account_id: int
    balance: float


class Client(BaseModel):
    ''' Class to handle clients'''

    pesel: str
    first_name: str
    last_name: str
    account_id: int

