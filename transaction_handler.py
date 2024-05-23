import pypyodbc as odbc


class TransactionHandler:
    ''' Class to handle transactions on multiple databases'''
    branch_db_conns: list[odbc.Connection]
    associated_branches: dict[int, int] # account_id -> branch_id

    def find_branch(self, account_id: int) -> int:
        try:
            for branch_id, branch_conn in enumerate(self.branch_db_conns):
                cursor = branch_conn.cursor()
                cursor.execute(f"SELECT * FROM konto WHERE nr_konta = {account_id}")
                if cursor.fetchone():
                    return branch_id
        except Exception as e:
            print(f"Error during branch search: {e}")

    def insert(self, query: str, db_id: int) -> None:
        try:
            conn = self.branch_db_conns[db_id]
            cursor = conn.cursor()
            cursor.execute(query)
        except Exception as e:
            print(f"Error during insert: {e}")
            self.rollback_transaction()

    def query(self, query: str, db_id: int) -> str:
        try:
            conn = self.branch_db_conns[db_id]
            cursor = conn.cursor()
            cursor.execute(query)
            result = cursor.fetchall()
            return result
        except Exception as e:
            print(f"Error during query: {e}")

    def commit_transaction(self, db_id: int) -> None:
        try:
            conn = self.branch_db_conns[db_id]
            conn.commit()
        except Exception as e:
            print(f"Error during commit: {e}")
            self.rollback_transaction()

    def rollback_transaction(self, db_id: int) -> None:
        try:
            conn = self.branch_db_conns[db_id]
            conn.rollback()
        except Exception as e:
            print(f"Error during rollback: {e}")
