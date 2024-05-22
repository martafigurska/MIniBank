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
        int nr_konta PK
        int saldo 
    }

    konto ||--o{ klient : "nr_konta"

```
