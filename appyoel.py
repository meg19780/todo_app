
import os
from flask import Flask, render_template, url_for, redirect, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

# Load database configuration from environment variables
DB_HOST = os.environ.get("DB_HOST", "db")  # Default to 'db' since Docker Compose names it as such
DB_USER = os.environ.get("DB_USER", "root")
DB_PASSWORD = os.environ.get("DB_PASSWORD", "password")
DB_NAME = os.environ.get("DB_NAME", "todo")

# Configure SQLAlchemy connection to MySQL
app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Define the Task model
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# Ensure tables are created before starting the app
with app.app_context():
    db.create_all()

@app.route('/', methods=["GET"])
def main():
    tasks = Task.query.all()  # Get all tasks from the database
    return render_template('base1.html', tasks=tasks)

@app.route('/', methods=["POST"])
def add():
    if "task" in request.form:
        task_content = request.form["task"]
        new_task = Task(content=task_content)
        db.session.add(new_task)  # Add the new task to the session
        db.session.commit()  # Commit the session to save changes
    elif "delete" in request.form:
        task_id = request.form.get("task_id")
        if task_id:
            task_to_delete = Task.query.get(task_id)
            if task_to_delete:
                db.session.delete(task_to_delete)
                db.session.commit()
    return redirect(url_for('main'))

if __name__ == '__main__':
    app.run(debug=True)
