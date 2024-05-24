from pydantic import BaseModel

class Transaction(BaseModel):
    ''' 
    Class to handle transactions
    
    Attributes:
    src_account: int
    des_account: int
    amount: float
    '''

    src_account: int
    des_account: int
    amount: float


class Account(BaseModel):
    ''' 
    Class to handle accounts
    
    Attributes:
    pesel: str
    first_name: str
    last_name: str
    balance: float
    password: str
    '''

    pesel: str
    first_name: str
    last_name: str
    balance: float
    password: str