import pypyodbc as odbc
import random

class Handler:
    """
    Class to handle insertion and queries on multiple databases
    
    Attributes:
    branch_db_conns: list[odbc.Connection] - list of connections to branch databases
    associated_table: dict[int, int] - account_id -> branch_id mapping

    Methods for public use:
    query_transakcja(self, account_id: int, other_account_id: int) -> str
    query_konto(account_id: int) -> str
    insert_transakcja(self, account_id: int, other_account_id: int, amount: float) -> None
    insert_konto(pesel:str, imie:str, nazwisko: str, saldo:float = 0) -> None
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
    
    def query_transakcja(self, account_id: int, other_account_id: int) -> str:
        '''
        Public use\n
        Queries transakcja table for given sender and receiver account_id and returns result\n
        '''
        query_str = f"SELECT * FROM transakcja WHERE nr_konta = {account_id} AND nr_konta_zewnetrzny = {other_account_id}"
        return self.query(account_id, query_str)
        
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

    def insert_to_branch(self, query: str, branch_id: int) -> None:
        '''Executes insert query on database with given branch_id'''
        if not query.startswith("INSERT"):
            raise ValueError("Query must be an insert query")

        try:
            cursor = self.branch_db_conns[branch_id].cursor()
            cursor.execute(query)
            cursor.commit()
        except Exception as e:
            print(f"Error during insert to konto to branch: {e}")

    def query_pesel(self, pesel: int, conn: odbc.Connection) -> str:  # TODO: check type of fetchall
        '''Queries konto table for given pesel and returns result'''
        query_str = f"SELECT * FROM konto WHERE pesel = {pesel}"
        return conn.cursor().execute(query_str).fetchall()

    def insert_konto(self, pesel:str, imie:str, nazwisko: str, saldo:float = 100) -> None:
        '''Executes insert query on konto table'''
        query = f"INSERT INTO konto (pesel, imie, nazwisko, saldo) VALUES ('{pesel}', '{imie}', '{nazwisko}', {saldo})"
        
        in_db = False
        for branch_conn in self.branch_db_conns:
            if self.query_pesel(pesel, branch_conn):
                in_db = True
                break
            
        if not in_db:
            branch_db = random.randint(0, len(self.branch_db_conns) - 1) # TODO: implement load balancing
            self.insert_to_branch(query, branch_db)


    def insert_transakcja(self, account_id: int, other_account_id: int, amount: float) -> None:
        '''Executes insert query on transakcja table'''

        query = f"INSERT INTO transakcja (nr_konta, nr_konta_zewnetrzny, kwota) VALUES "
        query_base = query + f"({account_id}, {other_account_id}, {-amount})"
        query_other = query + f"({other_account_id}, {account_id}, {amount})"

        self.insert(account_id, query_base) 
        self.insert(other_account_id, query_other)
        