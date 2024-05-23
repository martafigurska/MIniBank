import pypyodbc as odbc

DRIVER_NAME = 'SQL SERVER'
SERVER_NAME = 'DESKTOP-5G3QIOB\SQL_SERVER'
BRANCH_DB_NAMES = ['BANK1', 'BANK2']

def create_connection(database: str) -> odbc.Connection:
    '''
    Function to create connection to a database\n

    Args:
    database (str): name of the database

    Returns:
    odbc.Connection: connection to the database
    '''
    connection_string = f'''
        DRIVER={{{DRIVER_NAME}}};
        SERVER={{{SERVER_NAME}}};
        DATABASE={{{database}}};
        Trust_Connection=yes;
    '''
    return odbc.connect(connection_string)


def setup_database() -> list[odbc.Connection]:
    ''' 
    Function to create connections to all branch databases\n

    Returns:
    list[odbc.Connection]: list of connections to all branch databases
    '''
    branch_conns = [create_connection(db) for db in BRANCH_DB_NAMES]
    return branch_conns
