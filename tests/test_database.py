import unittest
from unittest.mock import patch
import sqlite3
from app import get_db_connection

class TestDatabaseConnection(unittest.TestCase):

    @patch('app.sqlite3.connect')
    def test_get_db_connection(self, mock_connect):
        mock_conn = mock_connect.return_value
        conn = get_db_connection()
        mock_connect.assert_called_once_with('flight_delays.db')
        self.assertEqual(conn, mock_conn)
        self.assertEqual(conn.row_factory, sqlite3.Row)

if __name__ == '__main__':
    unittest.main()