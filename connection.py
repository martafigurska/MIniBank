import pypyodbc as odbc

DRIVER_NAME = 'SQL SERVER'
SERVER_NAME = 'DESKTOP-5G3QIOB\SQL_SERVER'
DATATBASE_NAME = 'BANK1'
# uid=<username>
# pwd=<password>

connection_string = f'''
    DRIVER={{{DRIVER_NAME}}};
    SERVER={{{SERVER_NAME}}};
    DATABASE={{{DATATBASE_NAME}}};
    Trust_Connection=yes;
'''

conn = odbc.connect(connection_string)
cursor = conn.cursor()
cursor.execute("INSERT INTO konto VALUES (2, 1000)")
cursor.execute("INSERT INTO klient VALUES ('123', 'Iwo', 'Pinowski', 2)")

cursor.execute('SELECT * FROM klient')
print(cursor.fetchall())