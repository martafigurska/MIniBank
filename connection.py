import pyodbc
import aioodbc

DRIVER_NAME = 'ODBC Driver 17 for SQL Server'
SERVER_NAME = 'localhost'
PORT = 1433
SA_USER = 'sa'
SA_PASSWORD = '<YourStrong@Passw0rd>'
BRANCH_DB_NAMES = ['BANK1', 'BANK2', 'BANK3']

def create_connection_sync(database: str) -> pyodbc.Connection:
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

def create_database(db_name: str) -> None:
    '''
    Function to create a single database if it doesn't exist

    Args:
    db_name (str): name of the database
    '''
    conn = create_connection_sync('master')
    conn.autocommit = True
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

async def create_tables(conn: aioodbc.Connection, nr: int = 1) -> None:
    try:
        with open(f'base/baza.sql', 'r') as f:
            schema = f.read()
            for el in schema.split(';'):
                if el:
                    await conn.execute(el)
            conn.commit()
    except Exception as e:
        print(f"Error creating tables in branch {nr}: {e}") # TODO: look for a problem with the insertion
        await conn.close()
    
async def setup_database() -> list[aioodbc.Connection]:
    ''' 
    Function to create connections to all branch databases

    Returns:
    list[aioodbc.Connection]
    '''
    create_databases() 
    branch_conns = [await create_connection_async(db) for db in BRANCH_DB_NAMES]
    for i, conn in enumerate(branch_conns):
        await create_tables(conn, i)
    return branch_conns
