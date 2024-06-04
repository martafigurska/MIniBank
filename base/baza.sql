CREATE TABLE konto
(
pesel varchar(11) primary key,
nr_konta INT UNIQUE DEFAULT NEXT VALUE FOR nr_konta_,
imie varchar(20),
nazwisko varchar(20),
saldo float
CONSTRAINT UC_nr_konta UNIQUE (nr_konta)
);
-- Error:
-- [Microsoft][ODBC Driver 17 for SQL Server][SQL Server]Invalid object name 'nr_konta_'. (208) (SQLExecDirectW)
CREATE TABLE transakcja
(
nr_transakcji int identity primary key, 
nr_konta int,
nr_konta_zewnetrzny int,
kwota float,
foreign KEY(nr_konta) references konto(nr_konta),
);
