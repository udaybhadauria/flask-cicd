import unittest
import json
from app import app

class WeatherAPITestCase(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_ping(self):
        response = self.client.get('/ping')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'pong', response.data)

    def test_post_weather_unauth(self):
        response = self.client.post('/weather', json={
            'city': 'delhi',
            'temperature': 35
        })
        self.assertEqual(response.status_code, 401)

if __name__ == '__main__':
    unittest.main()
