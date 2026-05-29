from flask import Flask, jsonify, request, abort
import sqlite3

app = Flask(__name__)

# Connect to SQLite database
def get_db_connection():
    conn = sqlite3.connect('todo.db')
    conn.row_factory = sqlite3.Row
    return conn

# Create the database and the todo table
with get_db_connection() as conn:
    conn.execute('''CREATE TABLE IF NOT EXISTS todos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    task TEXT NOT NULL,
                    done BOOLEAN NOT NULL DEFAULT 0
                  );''')

# Retrieve all tasks
@app.route('/api/todos', methods=['GET'])
def get_todos():
    conn = get_db_connection()
    todos = conn.execute('SELECT * FROM todos').fetchall()
    conn.close()
    return jsonify([dict(todo) for todo in todos])

# Create a new task
@app.route('/api/todos', methods=['POST'])
def create_todo():
    new_task = request.json.get('task')
    if not new_task:
        abort(400)  # Missing task
    conn = get_db_connection()
    conn.execute('INSERT INTO todos (task) VALUES (?)', (new_task,))
    conn.commit()
    conn.close()
    return jsonify({'status': 'success'}), 201

# Update a task
@app.route('/api/todos/<int:todo_id>', methods=['PUT'])
def update_todo(todo_id):
    update_data = request.json
    conn = get_db_connection()
    conn.execute('UPDATE todos SET task = ?, done = ? WHERE id = ?', (update_data['task'], update_data['done'], todo_id))
    conn.commit()
    conn.close()
    return jsonify({'status': 'success'})

# Delete a task
@app.route('/api/todos/<int:todo_id>', methods=['DELETE'])
def delete_todo(todo_id):
    conn = get_db_connection()
    conn.execute('DELETE FROM todos WHERE id = ?', (todo_id,))
    conn.commit()
    conn.close()
    return jsonify({'status': 'success'})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)