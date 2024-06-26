from fastapi import FastAPI, status, HTTPException
from connection import setup_database
from classes.handler import Handler
from classes.pydantic_classes import Account, Transaction
from fastapi.middleware.cors import CORSMiddleware
import json
import time
from fastapi.responses import RedirectResponse


app = FastAPI()

handler = None
login_table = {}

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

login_data_path = "login_data.json"

def load_login_data():
    try:
        with open(login_data_path, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

def save_login_data(login_data):
    with open(login_data_path, "w") as file:
        json.dump(login_data, file)

@app.on_event("startup")
async def on_startup():
    global handler, login_table
    branch_conns = await setup_database()
    handler = Handler(branch_conns=branch_conns)
    login_table = load_login_data()

@app.on_event("shutdown")
async def on_shutdown():
    try:
        for conn in handler.branch_db_conns:
            await conn.close()
            
    except Exception as e:
        print(f"Error closing connections: {e}")
    time.sleep(1)

@app.get("/", include_in_schema=False)
async def root():
    return RedirectResponse(url="/docs")

@app.post("/new_account", status_code=status.HTTP_201_CREATED)
async def create_account(account: Account):
    '''Creates new account in distributed database and returns account details'''
    pesel = account.pesel
    imie = account.first_name
    nazwisko = account.last_name
    saldo = account.balance
    password = account.password
    try:
        res = await handler.insert_konto(pesel, imie, nazwisko, saldo)
        if "error" in res:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Account already exists")
        login_table[str(res['nr_konta'])] = password
        save_login_data(login_table)
        return res
    except HTTPException as e:
        raise e
    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
        

@app.post("/new_transaction", status_code=status.HTTP_201_CREATED)
async def create_transaction(transaction: Transaction) -> dict:
    '''Creates new transaction in distributed database and returns transaction details'''
    src_account = transaction.src_account
    des_account = transaction.des_account
    amount = transaction.amount
    try:
        await handler.insert_transakcja(src_account, des_account, amount)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

    return {"src_account": src_account, "des_account": des_account, "amount": amount}

@app.get("/login/{account_id}/{password}", status_code=status.HTTP_200_OK)
async def login(account_id: str, password: str):
    '''Checks if account_id and password are correct'''
    if account_id not in login_table:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Account not found")
    elif login_table[account_id] != password:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect password")
    return {"login": "success"}

@app.get("/accounts", status_code=status.HTTP_200_OK)
async def get_accounts():
    '''Returns all account details(from table konto)'''
    try:
        return await handler.query_all_accounts()
    except HTTPException as e: 
        raise e
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Accounts not found: {e}")

@app.get("/account/{account_id}", status_code=status.HTTP_200_OK)
async def get_account(account_id: int):
    '''Returns account details(from table konto) for given account_id'''
    try:
        return await handler.query_konto(account_id)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Account not found: {e}")

@app.get("/transactions/{account_id}", status_code=status.HTTP_200_OK)
async def get_transaction(account_id: int):
    '''Returns transactions details(from table transakcja) for given account_id'''
    try:
        return await handler.query_transakcja(account_id)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Transaction not found : {e}")
    
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port= 8080)
    