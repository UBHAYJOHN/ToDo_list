from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

def create_table():
    conn = sqlite3.connect('todo.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS tasks
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, task TEXT)''')
    conn.commit()
    conn.close()

def add_task(task):
    conn = sqlite3.connect('todo.db')
    c = conn.cursor()
    c.execute("INSERT INTO tasks (task) VALUES (?)", (task,))
    conn.commit()
    conn.close()

def delete_task(task_id):
    conn = sqlite3.connect('todo.db')
    c = conn.cursor()
    c.execute("DELETE FROM tasks WHERE id=?", (task_id,))
    conn.commit()
    conn.close()

def update_task(task_id, task):
    conn = sqlite3.connect('todo.db')
    c = conn.cursor()
    c.execute("UPDATE tasks SET task=? WHERE id=?", (task, task_id))
    conn.commit()
    conn.close()

def get_tasks():
    conn = sqlite3.connect('todo.db')
    c = conn.cursor()
    c.execute("SELECT * FROM tasks")
    tasks = c.fetchall()
    conn.close()
    return tasks

@app.route('/')
def index():
    tasks = get_tasks()
    return render_template('base.html', tasks=tasks)

@app.route('/add', methods=['POST'])
def add():
    task = request.form['task']
    add_task(task)
    return redirect(url_for('index'))

@app.route('/delete/<int:task_id>', methods=['POST'])
def delete(task_id):
    delete_task(task_id)
    return redirect(url_for('index'))

@app.route('/update/<int:task_id>', methods=['POST'])
def update(task_id):
    task = request.form['task']
    update_task(task_id, task)
    return redirect(url_for('index'))

if __name__ == "__main__":
    create_table()
    app.run(debug=True)
