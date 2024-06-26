import unittest
from app import app
from unittest.mock import patch, MagicMock

class TestFlightAPI(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    @patch('app.get_db_connection')
    def test_get_flights(self, mock_get_db_connection):
        # Mocking the database connection and cursor
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_conn.execute.return_value = mock_cursor
        mock_cursor.fetchall.return_value = [
            {
                "flight_number": "2325",
                "airline": "LH",
                "origin": "VIE",
                "destination": "MUC",
                "scheduled_departure_at": "2024-06-19T10:05",
                "actual_departure_at": "2024-06-19T10:39",
                "delay_code1": "1",
                "delay_time1": 20,
                "delay_description1": "Aircraft problem",
                "delay_code2": "2",
                "delay_time2": 10,
                "delay_description2": "Slow baggage handling",
                "delay_code3": None
            }
        ]
        mock_get_db_connection.return_value = mock_conn

        response = self.app.get('/api/flights?destination=MUC')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['flight_number'], '2325')
        self.assertEqual(data[0]['airline'], 'LH')
        self.assertEqual(data[0]['origin'], 'VIE')
        self.assertEqual(data[0]['destination'], 'MUC')
        self.assertEqual(len(data[0]['delays']), 2)

if __name__ == '__main__':
    unittest.main()
