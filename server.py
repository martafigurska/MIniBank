from fastapi import FastAPI, status, HTTPException
from connection import setup_database
from classes.handler import Handler
from classes.pydantic_classes import Account, Transaction

app = FastAPI()

login_table = {}
handler = None

@app.on_event("startup")
async def on_startup():
    global handler
    branch_conns = await setup_database()
    handler = Handler(branch_conns=branch_conns)

@app.post("/new_account/", status_code=status.HTTP_201_CREATED)
async def create_account(account: Account) -> dict:
    '''Creates new account in distributed database and returns account details'''
    pesel = account.pesel
    imie = account.first_name
    nazwisko = account.last_name
    saldo = account.balance
    password = account.password
    login_table[pesel] = password
    try:
        await handler.insert_konto(pesel, imie, nazwisko, saldo)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    
    return {"pesel": pesel, "imie": imie, "nazwisko": nazwisko, "saldo": saldo}

@app.post("/new_transaction/", status_code=status.HTTP_201_CREATED)
async def create_transaction(transaction: Transaction) -> dict:
    '''Creates new transaction in distributed database and returns transaction details'''
    src_account = transaction.src_account
    des_account = transaction.des_account
    amount = transaction.amount
    try:
        await handler.insert_transakcja(src_account, des_account, amount)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

    return {"src_account": src_account, "des_account": des_account, "amount": amount}

@app.get("/accounts/", status_code=status.HTTP_200_OK)
async def get_accounts():
    '''Returns all account details(from table konto)'''
    try:
        return await handler.query_all_accounts()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Accounts not found: {e}")

@app.get("/account/{account_id}", status_code=status.HTTP_200_OK)
async def get_account(account_id: int):
    '''Returns account details(from table konto) for given account_id'''
    try:
        return await handler.query_konto(account_id)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Account not found: {e}")

@app.get("/transaction/{account_id}", status_code=status.HTTP_200_OK)
async def get_transaction(account_id: int):
    '''Returns transactions details(from table transakcja) for given account_id'''
    try:
        return await handler.query_transakcja(account_id)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Transaction not found : {e}")
    