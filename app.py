from flask import Flask, request, render_template, redirect, url_for
from models import db, Task
from config import Config
from flask.cli import with_appcontext
import click

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)


# Главная страница - список задач
@app.route('/')
def index():
    tasks = Task.query.order_by(Task.created_at.desc()).all()
    return render_template('tasks.html', tasks=tasks)

# Просмотр одной задачи
@app.route('/tasks/<int:task_id>')
def task_detail(task_id):
    task = Task.query.get_or_404(task_id)
    return render_template('task_detail.html', task=task)

# Создание задачи
@app.route('/tasks/new', methods=['GET', 'POST'])
def create_task():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form.get('content')
        task = Task(title=title, content=content)
        db.session.add(task)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('create_task.html')

# Редактирование задачи
@app.route('/tasks/<int:task_id>/edit', methods=['GET', 'POST'])
def edit_task(task_id):
    task = Task.query.get_or_404(task_id)
    if request.method == 'POST':
        task.title = request.form['title']
        task.content = request.form.get('content')
        db.session.commit()
        return redirect(url_for('task_detail', task_id=task.id))
    return render_template('edit_task.html', task=task)

# Удаление задачи
@app.route('/tasks/<int:task_id>/delete', methods=['POST'])
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    db.session.delete(task)
    db.session.commit()
    return redirect(url_for('index'))

# Пометить как выполненную
@app.route('/tasks/<int:task_id>/done', methods=['POST'])
def mark_done(task_id):
    task = Task.query.get_or_404(task_id)
    task.is_done = True
    db.session.commit()
    return redirect(url_for('index'))

@app.cli.command("init-db")
def init_db():
    db.create_all()


if __name__ == '__main__':
    app.run()
