from fastapi import FastAPI, status, HTTPException
from connection import setup_database
from classes.handler import Handler
from classes.pydantic_classes import Account, Transaction

app = FastAPI()

branch_conns = setup_database()
handler = Handler(branch_conns=branch_conns)
login_table = {}

# post konta
@app.post("/new_account/", status_code=status.HTTP_201_CREATED)
async def create_account(account: Account) -> dict:
    pesel = account.pesel
    imie = account.first_name
    nazwisko = account.last_name
    saldo = account.balance
    password = account.password
    login_table[pesel] = password
    try:
        handler.insert_konto(pesel, imie, nazwisko, saldo)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    
    return {"pesel": pesel, "imie": imie, "nazwisko": nazwisko, "saldo": saldo}


# post transakcji
@app.post("/new_transaction/", status_code=status.HTTP_201_CREATED)
async def create_transaction(transaction: Transaction) -> dict:
    src_account = transaction.src_account
    des_account = transaction.des_account
    amount = transaction.amount
    try:
        handler.insert_transakcja(src_account, des_account, amount)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

    return {"src_account": src_account, "des_account": des_account, "amount": amount}

# get konta
@app.get("/account/{account_id}", status_code=status.HTTP_200_OK)
async def get_account(account_id: int) -> dict:
    try:
        return handler.query_konto(account_id) # it should be json
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Account not found: {e}")

# get transakcji
@app.get("/transaction/{account_id}", status_code=status.HTTP_200_OK)
async def get_transaction(account_id: int) -> dict:
    try:
        return handler.query_transakcja(account_id) # it should be json
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Transaction not found : {e}")
