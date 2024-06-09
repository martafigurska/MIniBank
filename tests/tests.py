import unittest
from unittest.mock import MagicMock, AsyncMock, patch
import sys
sys.path.append('../classes')
from classes.handler import Handler
import aioodbc

class TestHandler(unittest.IsolatedAsyncioTestCase):
    
    def setUp(self):
        self.mock_conn_1 = MagicMock(spec=aioodbc.Connection)
        self.mock_conn_2 = MagicMock(spec=aioodbc.Connection)
        self.mock_cursor_1 = AsyncMock()
        self.mock_cursor_2 = AsyncMock()
        self.mock_conn_1.cursor.return_value = self.mock_cursor_1
        self.mock_conn_2.cursor.return_value = self.mock_cursor_2

        self.handler = Handler([self.mock_conn_1, self.mock_conn_2])

    async def test_id_from_associated_table_exists(self):
        self.handler.associated_table = {1: 0}
        result = self.handler.id_from_associated_table(1)
        self.assertEqual(result, 0)

    async def test_search_branch_id_found(self):
        self.mock_cursor_1.fetchall.return_value = [(1,)]
        account_id = 1
        result = await self.handler.search_branch_id(account_id)
        self.assertEqual(result, 0)
        self.assertIn(account_id, self.handler.associated_table)
        self.assertEqual(self.handler.associated_table[account_id], 0)

    async def test_find_branch(self):
        account_id = 1
        with patch.object(self.handler, 'id_from_associated_table', return_value=-1), \
             patch.object(self.handler, 'search_branch_id', return_value=0):
            result = await self.handler.find_branch(account_id)
            self.assertEqual(result, 0)

    async def test_query(self):
        account_id = 1
        query_str = "SELECT * FROM konto WHERE nr_konta = 1"
        self.mock_cursor_1.fetchall.return_value = [(1,)]
        with patch.object(self.handler, 'get_cursor', return_value=self.mock_cursor_1):
            result = await self.handler.query(account_id, query_str)
            self.assertEqual(result, [(1,)])

    async def test_insert_konto(self):
        pesel = '12345678901'
        self.mock_cursor_1.fetchall.return_value = [(1,)]
        with patch.object(self.handler, 'query_pesel', return_value=[(1,)]):
            result = await self.handler.insert_konto(pesel, 'name', 'surname', 100.0)
            self.assertEqual(result, {"error": "Account already exists"})

    async def test_insert_transakcja(self):
        account_id = 1
        other_account_id = 2
        amount = 50.0
        with patch.object(self.handler, 'insert', return_value=None):
            await self.handler.insert_transakcja(account_id, other_account_id, amount)
            self.handler.insert.assert_any_await(account_id, 
                "INSERT INTO transakcja (nr_konta, nr_konta_zewnetrzny, kwota) VALUES (1, 2, -50.0)")
            self.handler.insert.assert_any_await(other_account_id, 
                "INSERT INTO transakcja (nr_konta, nr_konta_zewnetrzny, kwota) VALUES (2, 1, 50.0)")

if __name__ == "__main__":
    unittest.main()
