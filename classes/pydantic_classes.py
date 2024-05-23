from pydantic import BaseModel

class Transaction(BaseModel):
    ''' Class to handle transactions'''

    src_account: int
    des_account: int
    amount: float


class Account(BaseModel):
    ''' Class to handle accounts'''

    pesel: str
    first_name: str
    last_name: str
    balance: float
    password: str