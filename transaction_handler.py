from typing import Any


class TransactionHandler:
    central_db_conn: Any # think if it's necessary
    branch_db_conns: list[Any]
    associated_branches: dict[int, int] # account_id -> branch_id

    def find_branch(self, account_id: int) -> int:
        pass

    def query(self, query: str, db_id: int) -> Any:
        pass

    def commit_transaction(self, db_id: int) -> None:
        try:
            self.central_db_conn.commit()
            conn = self.branch_db_conns[db_id]
            conn.commit()
        except Exception as e:
            print(f"Error during commit: {e}")
            self.rollback_transaction()

    def rollback_transaction(self, db_id: int) -> None:
        try:
            self.central_db_conn.rollback()
            conn = self.branch_db_conns[db_id]
            conn.rollback()
        except Exception as e:
            print(f"Error during rollback: {e}")
