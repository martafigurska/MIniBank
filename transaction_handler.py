from typing import Any


class TransactionHandler:
    central_db_conn: Any
    branch_db_conns: list[Any]

    def find_branch(self, account_id: int) -> int:
        pass

    def commit_transaction(self, db_id: int):
        try:
            self.central_db_conn.commit()
            conn = self.branch_db_conns[db_id]
            conn.commit()
        except Exception as e:
            print(f"Error during commit: {e}")
            self.rollback_transaction()

    def rollback_transaction(self, db_id: int):
        try:
            self.central_db_conn.rollback()
            conn = self.branch_db_conns[db_id]
            conn.rollback()
        except Exception as e:
            print(f"Error during rollback: {e}")
