import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgres://postgres:15000458@localhost:5432/trivia"
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
        self.new_question = {
            'question':'how are you?',
            'answer': 'fine thanks',
            'difficulty': 5,
            'category': 3
        }

    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """
    def test_get_paginated_questions(self):
        res = self.client().get('/api/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['questions'])
        self.assertTrue(data['total_questions'])
        self.assertTrue(data['categories'])

    def test_404_sent_requesting_beyond_valid_page(self):
        res = self.client().get('/api/questions?page=1000')
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success', False])
        self.assertEqual(data['message'], 'resource not found')

    def delete_question_test(self):
        res = self.client().delete('/api/question/1')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['questions'])
        self.assertEqual(data['total_questions'])

    def test_422_if_question_does_not_exist(self):
        res = self.client().delete('/api/questions/100')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message', 'unprocessable'])

    def test_create_new_question(self):
        res = self.client().post('/api/questions/')
        data = json.loads(res.data)  

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['questions'])
        self.assertEqual(data['total_questions'])

    def test_405_if_question_creation_not_allowed(self):
        res = self.client().post('/api/questions/54', json=self.new_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message', 'method not allowed'])

    def test_get_categories(self):
        res = self.client().get('/api/categories')
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['categories'])

    def test_404_if_categories_not_found(self):
        res = self.client().get('/api/categories')
        data = json.loads(res.data)
        models.Category.query().delete()

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success', False])
        self.assertEqual(data['message'], 'resource not found')
    
    def test_get_question_by_id(self):
        res = self.client().get('/api/question/4')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertTrue(data['questions'])
        self.assertTrue(data['total_questions'])
        self.assertTrue(data['current_category'])

    def test_404_if_question_not_found_by_category(self):
        res = self.client().get('/api/question/412')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success', False])
        self.assertEqual(data['message'], 'resource not found')

    def test_search_question(self):
        res = self.client().post('/api/questions/search')
        data = json.loads(res.data)

        self.assertTrue(data['questions'])
        self.assertTrue(data['total_questions'])

    def test_405_if_search_question_not_allowed(self):
        res = self.client().post('/api/questions/search/54', json={'searchTerm':'blablablabla'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message', 'method not allowed'])

    def test_quiz(self):
        res = self.client().post('/api/quizzes')
        data = json.loads(res.data)

        self.assertTrue(data['questions'])
        self.assertTrue(data['total_questions'])

    def test_405_if_quiz_request_not_allowed(self):
        res = self.client().post('/api/quizzes/1')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message', 'method not allowed'])
        
# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()