# DISTRIBUTED DATABASE

This is a repository to store a distributed database project.


## Database schema

```mermaid
erDiagram
    konto {
        string pesel PK
        unique nr_konta 
        string imie
        string nazwisko
        int saldo
    }

    transakcja {
        serial nr_transakcji PK
        int nr_konta FK
        int nr_konta_zewnetrzny
        int kwota
    }

    konto ||--o{ transakcja : "nr_konta"

```

## Example input

post /new_account/

```json
{
  "pesel": "string",
  "first_name": "string",
  "last_name": "string",
  "balance": 0,
  "password": "string"
}
```


post /new_transaction/
<!-- TODO: change args to REST standard -->

```json 
{
  "src_account": 0,
  "des_account": 0,
  "amount": 0
}
```

get /accounts/

```json
{
  "accounts": [
    1,
    2,
    3,
    5,
    2,
    3,
    4,
    5
  ]
}
```

get /account/account_id

```json
{
  "pesel": "135",
  "nr_konta": 1,
  "imie": "Ala",
  "nazwisko": "Makota",
  "saldo": 3123
}
```


get /transaction/account_id 
<!-- TODO: change to transactions -->

```json
{
  "pesel": "135",
  "nr_konta": 1,
  "imie": "Ala",
  "nazwisko": "Makota",
  "saldo": 3123
}
```