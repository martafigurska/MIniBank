import pypyodbc as odbc
import random

class Handler:
    """
    Class to handle insertion and queries on multiple databases
    
    Attributes:
    branch_db_conns: list[odbc.Connection] - list of connections to branch databases
    associated_table: dict[int, int] - account_id -> branch_id mapping

    Methods for public use:
    query_transakcja(sender_account_id: int, receiver_account_id: int, return_sender:bool = True) -> str
    query_konto(account_id: int) -> str
    insert_konto(pesel:str, imie:str, nazwisko: str, saldo:float = 0) -> None
    insert_transakcja(sender_account_id: int, receiver_account_id: int, amount: float) -> None
    """

    branch_db_conns: list[odbc.Connection]
    associated_table: dict[int, int]

    def __init__(self, branch_conns: list[odbc.Connection]):
        self.branch_db_conns = branch_conns
        self.associated_table = {}

    def id_from_associated_table(self, account_id: int) -> int:
        '''Returns branch_id from associated_table if it exists, otherwise returns -1'''
        if account_id in self.associated_table:
            return self.associated_table[account_id]
        return -1

    def search_branch_id(self, account_id: int) -> int:
        '''Searches for branch_id in branch_db_conns and returns it if found, otherwise returns -1'''
        for branch_id, branch_conn in enumerate(self.branch_db_conns):
            query_str = f"SELECT * FROM konto WHERE nr_konta = {account_id}"
            if branch_conn.cursor().execute(query_str).fetchall():
                self.associated_table[account_id] = branch_id
                return branch_id
        return -1

    def find_branch(self, account_id: int) -> int:
        '''Finds branch_id for given account_id'''
        try:
            id = self.id_from_associated_table(account_id)
            return id if id != -1 else self.search_branch_id(account_id)
        except Exception as e:
            print(f"Error during branch search: {e}")

    def get_cursor(self, account_id: int) -> odbc.Cursor:
        '''Returns cursor for given account_id'''
        try:
            db_id = self.find_branch(account_id)
            if db_id == -1:
                raise ValueError("Branch not found")
            conn = self.branch_db_conns[db_id]
            return conn.cursor()
        except Exception as e:
            print(f"Error during cursor creation: {e}")

    def query(self, account_id: int,  query: str) -> str:
        '''Executes query on database and returns result'''
        if not query.startswith("SELECT"):
            raise ValueError("Query must be a select query")

        try:
            cursor = self.get_cursor(account_id)
            cursor.execute(query)
            result = cursor.fetchall()
            return result
        except Exception as e:
            print(f"Error during query: {e}")

    def query_konto(self, account_id: int) -> str:
        '''
        Public use\n
        Queries konto table for given account_id and returns result
        '''
        query_str = f"SELECT * FROM konto WHERE nr_konta = {account_id}"
        return self.query(account_id, query_str)
    
    def query_transakcja(self, sender_account_id: int, receiver_account_id: int, return_sender:bool = True) -> str:
        '''
        Public use\n
        Queries klient table for given account_id and returns result
        '''
        query_str = f"SELECT * FROM transakcja WHERE nr_konta_nadawcy = {sender_account_id} AND nr_konta_odbiorcy = {receiver_account_id}"
        
        if return_sender:
            return self.query(sender_account_id, query_str)
        else:
            return self.query(receiver_account_id, query_str)
    
    def insert(self, account_id: int, query: str) -> None:
        '''Executes insert query on database'''
        if not query.startswith("INSERT"):
            raise ValueError("Query must be an insert query")

        try:
            cursor = self.get_cursor(account_id)
            cursor.execute(query)
            cursor.commit()
        except Exception as e:
            print(f"Error during insert: {e}")

    def insert_konto(self, pesel:str, imie:str, nazwisko: str, saldo:float = 100) -> None:
        '''Executes insert query on konto table'''
        query = f"INSERT INTO konto (pesel, imie, nazwisko, saldo) VALUES ('{pesel}', '{imie}', '{nazwisko}', {saldo})"
        db_id = random.randint(0, len(self.branch_db_conns) - 1) # TODO: implement load balancing
        try:
            cursor = self.branch_db_conns[db_id].cursor()
            cursor.execute(query)
            cursor.commit()
        except Exception as e:
            print(f"Error during insert to konto: {e}")

    def insert_transakcja(self, sender_account_id: int, receiver_account_id: int, amount: float) -> None:
        '''Executes insert query on transakcja table'''

        query = f"INSERT INTO transakcja (nr_konta_nadawcy, nr_konta_odbiorcy, kwota) VALUES ({sender_account_id}, {receiver_account_id}, {amount})"

        sender_branch_id = self.find_branch(sender_account_id)
        receiver_branch_id = self.find_branch(receiver_account_id)
        
        self.insert(sender_account_id, query) # gets error
        
        if sender_branch_id != receiver_branch_id: # if different branches, add to both
            self.insert(receiver_account_id, query)
