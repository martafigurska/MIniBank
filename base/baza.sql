IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'konto')
BEGIN
    CREATE TABLE dbo.konto
    (
        pesel varchar(11) PRIMARY KEY,
        nr_konta INT UNIQUE DEFAULT NEXT VALUE FOR nr_konta_,
        imie varchar(20),
        nazwisko varchar(20),
        saldo float,
        CONSTRAINT UC_nr_konta UNIQUE (nr_konta)
    )
END;


IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'transakcja')
BEGIN
    CREATE TABLE dbo.transakcja
    (
        nr_transakcji int IDENTITY PRIMARY KEY, 
        nr_konta int,
        nr_konta_zewnetrzny int,
        kwota float,
        FOREIGN KEY(nr_konta) REFERENCES dbo.konto(nr_konta)
    )
END;
