# DISTRIBUTED DATABASE

This is a repository to store a distributed database project.


## Database schema

```mermaid
erDiagram
    klient {
        int pesel PK
        string imie
        string nazwisko
        int nr_konta FK 
    }

    konto {
        serial nr_konta PK
        int saldo 
    }

    transakcja {
        serial nr_transakcji PK
        int nr_konta_nadawcy FK
        int nr_konta_odbiorcy FK
        int kwota
    }

    konto ||--o{ klient : "nr_konta"
    konto ||--o{ transakcje : "nr_konta"

```
