
USE BANK1
GO
CREATE OR ALTER TRIGGER update_saldo
ON transakcja
AFTER INSERT
AS
BEGIN
    DECLARE @nr_konta int, @nr_konta_zewnetrzny int, @kwota float, @saldo_nadawcy float;

    SELECT @nr_konta = nr_konta,
           @nr_konta_zewnetrzny = nr_konta_zewnetrzny,
           @kwota = kwota
    FROM inserted;

    SELECT @saldo_nadawcy = saldo
    FROM konto
    WHERE nr_konta = @nr_konta;

    IF @saldo_nadawcy < ABS(@kwota)
    BEGIN
        RAISERROR ('Za malo srodkow na koncie aby zrobic przelew', 16, 1);
		THROW 51000, 'Za malo srodkow na koncie aby zrobic przelew', 16;
        ROLLBACK TRANSACTION;
        RETURN;
    END;

    UPDATE konto
    SET saldo = saldo + @kwota
    WHERE nr_konta = @nr_konta;

    UPDATE konto
    SET saldo = saldo + @kwota
    WHERE nr_konta = @nr_konta_zewnetrzny;
END;


CREATE SEQUENCE nr_konta_
   START WITH 1001
   INCREMENT BY 1;

CREATE OR ALTER TRIGGER transfer_to_yourself
ON transakcja
AFTER INSERT
AS
BEGIN
   DECLARE @src_account INT, @dest_account INT;
   SELECT @src_account = nr_konta, @dest_account = nr_konta_zewnetrzny
   FROM inserted;

   IF @src_account = @dest_account
   BEGIN
       RAISERROR ('Nie możesz przelać pieniędzy na swoje konto', 16, 1);
       ROLLBACK TRANSACTION;
       RETURN;
   END;
END;




USE BANK2
GO
CREATE OR ALTER TRIGGER update_saldo
ON transakcja
AFTER INSERT
AS
BEGIN
    DECLARE @nr_konta int, @nr_konta_zewnetrzny int, @kwota float, @saldo_nadawcy float;

    SELECT @nr_konta = nr_konta,
           @nr_konta_zewnetrzny = nr_konta_zewnetrzny,
           @kwota = kwota
    FROM inserted;

    SELECT @saldo_nadawcy = saldo
    FROM konto
    WHERE nr_konta = @nr_konta;

    IF @saldo_nadawcy < ABS(@kwota)
    BEGIN
        RAISERROR ('Za malo srodkow na koncie aby zrobic przelew', 16, 1);
		THROW 51000, 'Za malo srodkow na koncie aby zrobic przelew', 16;
        ROLLBACK TRANSACTION;
        RETURN;
    END;

    UPDATE konto
    SET saldo = saldo + @kwota
    WHERE nr_konta = @nr_konta;

    UPDATE konto
    SET saldo = saldo + @kwota
    WHERE nr_konta = @nr_konta_zewnetrzny;
END;


CREATE SEQUENCE nr_konta_
   START WITH 2001
   INCREMENT BY 1;

CREATE OR ALTER TRIGGER transfer_to_yourself
ON transakcja
AFTER INSERT
AS
BEGIN
   DECLARE @src_account INT, @dest_account INT;
   SELECT @src_account = nr_konta, @dest_account = nr_konta_zewnetrzny
   FROM inserted;

   IF @src_account = @dest_account
   BEGIN
       RAISERROR ('Nie możesz przelać pieniędzy na swoje konto', 16, 1);
       ROLLBACK TRANSACTION;
       RETURN;
   END;
END;



USE BANK3
GO
CREATE OR ALTER TRIGGER update_saldo
ON transakcja
AFTER INSERT
AS
BEGIN
    DECLARE @nr_konta int, @nr_konta_zewnetrzny int, @kwota float, @saldo_nadawcy float;

    SELECT @nr_konta = nr_konta,
           @nr_konta_zewnetrzny = nr_konta_zewnetrzny,
           @kwota = kwota
    FROM inserted;

    SELECT @saldo_nadawcy = saldo
    FROM konto
    WHERE nr_konta = @nr_konta;

    IF @saldo_nadawcy < ABS(@kwota)
    BEGIN
        RAISERROR ('Za malo srodkow na koncie aby zrobic przelew', 16, 1);
		THROW 51000, 'Za malo srodkow na koncie aby zrobic przelew', 16;
        ROLLBACK TRANSACTION;
        RETURN;
    END;

    UPDATE konto
    SET saldo = saldo + @kwota
    WHERE nr_konta = @nr_konta;

    UPDATE konto
    SET saldo = saldo + @kwota
    WHERE nr_konta = @nr_konta_zewnetrzny;
END;


CREATE SEQUENCE nr_konta_
   START WITH 3001
   INCREMENT BY 1;

CREATE OR ALTER TRIGGER transfer_to_yourself
ON transakcja
AFTER INSERT
AS
BEGIN
   DECLARE @src_account INT, @dest_account INT;
   SELECT @src_account = nr_konta, @dest_account = nr_konta_zewnetrzny
   FROM inserted;

   IF @src_account = @dest_account
   BEGIN
       RAISERROR ('Nie możesz przelać pieniędzy na swoje konto', 16, 1);
       ROLLBACK TRANSACTION;
       RETURN;
   END;
END;
