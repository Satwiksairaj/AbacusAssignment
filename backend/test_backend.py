import unittest
from app import app

test_app = app.test_client()

class TodoApiTest(unittest.TestCase):
    def setUp(self):
        test_app.testing = True

    def test_get_todos(self):
        response = test_app.get('/api/todos')
        self.assertEqual(response.status_code, 200)

    def test_create_todo(self):
        response = test_app.post('/api/todos', json={'task': 'Test TODO'})
        self.assertEqual(response.status_code, 201)

    def test_update_todo(self):
        # First create a todo
        test_app.post('/api/todos', json={'task': 'Update Test TODO'})
        response = test_app.put('/api/todos/1', json={'task': 'Updated TODO', 'done': True})
        self.assertEqual(response.status_code, 200)

    def test_delete_todo(self):
        # First create a todo
        test_app.post('/api/todos', json={'task': 'Delete Test TODO'})
        response = test_app.delete('/api/todos/1')
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()