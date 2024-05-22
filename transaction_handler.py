import pypyodbc as odbc


class TransactionHandler:
    ''' Class to handle transactions on multiple databases'''
    branch_db_conns: list[odbc.Connection]
    associated_branches: dict[int, int] # account_id -> branch_id

    def find_branch(self, account_id: int) -> int:
        pass

    def query(self, query: str, db_id: int) -> str:
        pass

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
