from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

# Database setup
conn = sqlite3.connect('todo.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS todos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    completed BOOLEAN NOT NULL DEFAULT 0
)''')
conn.commit()
conn.close()

@app.route('/todos', methods=['GET'])
def get_todos():
    conn = sqlite3.connect('todo.db')
    c = conn.cursor()
    c.execute('SELECT * FROM todos')
    todos = c.fetchall()
    conn.close()
    return jsonify(todos)

@app.route('/todos', methods=['POST'])
def add_todo():
    new_todo = request.get_json()
    title = new_todo['title']
    conn = sqlite3.connect('todo.db')
    c = conn.cursor()
    c.execute('INSERT INTO todos (title) VALUES (?)', (title,))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Todo added!'}), 201

@app.route('/todos/<int:todo_id>', methods=['PUT'])
def update_todo(todo_id):
    updated_todo = request.get_json()
    completed = updated_todo['completed']
    conn = sqlite3.connect('todo.db')
    c = conn.cursor()
    c.execute('UPDATE todos SET completed = ? WHERE id = ?', (completed, todo_id))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Todo updated!'}), 200

@app.route('/todos/<int:todo_id>', methods=['DELETE'])
def delete_todo(todo_id):
    conn = sqlite3.connect('todo.db')
    c = conn.cursor()
    c.execute('DELETE FROM todos WHERE id = ?', (todo_id,))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Todo deleted!'}), 200

if __name__ == '__main__':
    app.run(debug=True)