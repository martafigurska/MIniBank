import aioodbc

DRIVER_NAME = 'ODBC Driver 17 for SQL Server'
SERVER_NAME = 'sql_server'
BRANCH_DB_NAMES = ['BANK1', 'BANK2', 'BANK3']

async def create_connection(database: str) -> aioodbc.Connection:
    '''
    Function to create connection to a database

    Args:
    database (str): name of the database

    Returns:
    aioodbc.Connection
    '''
    connection_string = f'''
        DRIVER={{{DRIVER_NAME}}};
        SERVER={{{SERVER_NAME}}};
        DATABASE={{{database}}};
        Trust_Connection=yes;
    '''
    conn = await aioodbc.connect(dsn=connection_string)
    return conn

async def setup_database() -> list[aioodbc.Connection]:
    ''' 
    Function to create connections to all branch databases

    Returns:
    list[aioodbc.Connection]
    '''
    branch_conns = [await create_connection(db) for db in BRANCH_DB_NAMES]
    return branch_conns
