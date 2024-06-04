import pyodbc
import aioodbc

DRIVER_NAME = 'ODBC Driver 17 for SQL Server'
SERVER_NAME = 'localhost'
PORT = 1433  # Default port for SQL Server
SA_USER = 'sa'
SA_PASSWORD = '<YourStrong@Passw0rd>'
BRANCH_DB_NAMES = ['BANK1', 'BANK2', 'BANK3']

def create_connection_sync(database: str):
    '''
    Function to create a synchronous connection to a database

    Args:
    database (str): name of the database

    Returns:
    pyodbc.Connection
    '''
    connection_string = f'''
        DRIVER={{{DRIVER_NAME}}};
        SERVER={SERVER_NAME},{PORT};
        DATABASE={database};
        UID={SA_USER};
        PWD={SA_PASSWORD};
    '''
    conn = pyodbc.connect(connection_string)
    return conn

def create_database(db_name: str):
    '''
    Function to create a single database if it doesn't exist

    Args:
    db_name (str): name of the database
    '''
    conn = create_connection_sync('master')
    conn.autocommit = True  # Set autocommit to True
    cursor = conn.cursor()
    cursor.execute(f"IF NOT EXISTS (SELECT name FROM sys.databases WHERE name = N'{db_name}') CREATE DATABASE {db_name};")
    cursor.close()
    conn.close()

def create_databases():
    '''
    Function to create databases if they don't exist
    '''
    for db_name in BRANCH_DB_NAMES:
        create_database(db_name)

async def create_connection_async(database: str) -> aioodbc.Connection:
    '''
    Function to create an asynchronous connection to a database

    Args:
    database (str): name of the database

    Returns:
    aioodbc.Connection
    '''
    connection_string = f'''
        DRIVER={{{DRIVER_NAME}}};
        SERVER={SERVER_NAME},{PORT};
        DATABASE={database};
        UID={SA_USER};
        PWD={SA_PASSWORD};
    '''
    conn = await aioodbc.connect(dsn=connection_string)
    return conn

async def setup_database() -> list[aioodbc.Connection]:
    ''' 
    Function to create connections to all branch databases

    Returns:
    list[aioodbc.Connection]
    '''
    create_databases() 
    branch_conns = [await create_connection_async(db) for db in BRANCH_DB_NAMES]
    return branch_conns
