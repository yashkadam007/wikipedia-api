import unittest
from flask import json
from api import app,db

class TestWordFrequencyAPI(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test_wikipedia_search.db'
        self.app = app.test_client()
        
        with app.app_context():
            db.create_all()

    def tearDown(self):
        with app.app_context():
            db.drop_all()

    def test_word_frequency_api(self):
        # CASE: Make a simple request to the API endpoint
        response = self.app.get('/api/word-frequency?topic=color&n=5')
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.get_data(as_text=True))
        self.assertIsInstance(response_data.get("top_n_words"), list)
        self.assertEqual(len(response_data.get("top_n_words")), 5)

        #CASE: Empty topic
    def test_word_frequency_empty_topic(self):
        response = self.app.get('/api/word-frequency?topic=&n=5')
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.get_data(as_text=True))
        self.assertEqual(response_data.get("status"), "error")
        self.assertEqual(response_data.get("message"), "Topic can not be empty")
        
        #CASE: nagative n value
    def test_word_frequency_negative_n_value(self):
        response = self.app.get('/api/word-frequency?topic=color&n=-5')
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.get_data(as_text=True))
        self.assertEqual(response_data.get("status"), "error")
        self.assertEqual(response_data.get("message"), "Invalid value for n. provide non negative integer")
        
        #CASE: DisambiguationError check
    def test_word_frequency_disambiguation_error(self):
        response = self.app.get('/api/word-frequency?topic=dexter&n=5')
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.get_data(as_text=True))
        self.assertEqual(response_data.get("status"), "error")
        self.assertTrue(response_data.get("message").startswith("DisambiguationError:"))

        #CASE: Test SearchHistoryAPI
    def test_search_history(self):
        response = self.app.get('/api/search-history')
        self.assertEqual(response.status_code, 200)

        #CASE: Topic not found
    def test_word_frequency_topic_not_found_api(self):
        response = self.app.get('/api/word-frequency?topic=dajkjfjskjr&n=5')
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.get_data(as_text=True))
        self.assertEqual(response_data.get("status"), "error")
        self.assertEqual(response_data.get("message"), "Topic not found on Wikipedia")

    def test_invalid_url_api(self):
        response = self.app.get('/api/word-frequenci')
        self.assertEqual(response.status_code, 404)
        response_data = json.loads(response.get_data(as_text=True))
        self.assertEqual(response_data.get("status"), "error")
        self.assertEqual(response_data.get("message"), "Invalid route. Please check the URL.")


if __name__ == '__main__':
    unittest.main()
