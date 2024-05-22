import pypyodbc as odbc

DRIVER_NAME = 'SQL SERVER'
SERVER_NAME = 'DESKTOP-5G3QIOB\SQL_SERVER'
CENTRAL_DB_NAME = 'CENTRAL'
BRANCH_DB_NAMES = ['BANK1', 'BANK2']


def create_connection(database):
    connection_string = f'''
        DRIVER={{{DRIVER_NAME}}};
        SERVER={{{SERVER_NAME}}};
        DATABASE={{{database}}};
        Trust_Connection=yes;
    '''
    return odbc.connect(connection_string)


def setup_database():
    central_conn = create_connection(CENTRAL_DB_NAME)
    branch_conns = [create_connection(db) for db in BRANCH_DB_NAMES]
    return central_conn, branch_conns
