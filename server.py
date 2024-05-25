from fastapi import FastAPI, status, HTTPException
from connection import setup_database
from classes.handler import Handler
from classes.pydantic_classes import Account, Transaction
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# TODO: remove login_table content
login_table = {1: 'admin', 2: 'admin', 3:'admin', 4:'admin', 5:'admin', 6:'admin', 7:'admin', 8:'admin', 9:'admin', 10:'admin'}
handler = None

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change this to your specific frontend URL in production
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def on_startup():
    global handler
    branch_conns = await setup_database()
    handler = Handler(branch_conns=branch_conns)

@app.post("/new_account", status_code=status.HTTP_201_CREATED)
async def create_account(account: Account):
    '''Creates new account in distributed database and returns account details'''
    pesel = account.pesel
    imie = account.first_name
    nazwisko = account.last_name
    saldo = account.balance
    password = account.password
    login_table[pesel] = password
    try:
        return await handler.insert_konto(pesel, imie, nazwisko, saldo)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    
@app.post("/new_transaction", status_code=status.HTTP_201_CREATED)
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

@app.get("/login/{account_id}/{password}", status_code=status.HTTP_200_OK)
async def login(account_id: int, password: str):
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
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Accounts not found: {e}")

@app.get("/account/{account_id}", status_code=status.HTTP_200_OK)
async def get_account(account_id: int):
    '''Returns account details(from table konto) for given account_id'''
    try:
        return await handler.query_konto(account_id)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Account not found: {e}")

@app.get("/transactions/{account_id}", status_code=status.HTTP_200_OK)
async def get_transaction(account_id: int):
    '''Returns transactions details(from table transakcja) for given account_id'''
    try:
        return await handler.query_transakcja(account_id)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Transaction not found : {e}")

@app.get("/transactions_to/{transaction_id}", status_code=status.HTTP_200_OK)
async def get_transaction_to(transaction_id: int):
    '''Returns transactions incoming for given transaction_id'''
    try:
        return await handler.query_transakcja_to(transaction_id)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Transaction not found : {e}")