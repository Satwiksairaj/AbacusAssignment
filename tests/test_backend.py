import unittest
import json
from backend.app import app

class TodoTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_add_todo(self):
        response = self.app.post('/todos', data=json.dumps({'title': 'Test Todo'}), content_type='application/json')
        self.assertEqual(response.status_code, 201)
        self.assertIn(b'Todo added!', response.data)

    def test_get_todos(self):
        response = self.app.get('/todos')
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(json.loads(response.data), list)

    def test_update_todo(self):
        self.app.post('/todos', data=json.dumps({'title': 'Test Todo'}), content_type='application/json')
        response = self.app.put('/todos/1', data=json.dumps({'completed': True}), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Todo updated!', response.data)

    def test_delete_todo(self):
        self.app.post('/todos', data=json.dumps({'title': 'Test Todo'}), content_type='application/json')
        response = self.app.delete('/todos/1')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Todo deleted!', response.data)

if __name__ == '__main__':
    unittest.main()