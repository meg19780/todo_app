import os
from flask import Flask, render_template, url_for, redirect, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Load database configuration from environment variables
DB_HOST = os.environ.get("DB_HOST", "db")  # Default to 'db' since Docker Compose names it as such
DB_USER = os.environ.get("DB_USER", "root")
DB_PASSWORD = os.environ.get("DB_PASSWORD", "password")
DB_NAME = os.environ.get("DB_NAME", "todo")
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Taskes(db.Model):
    task_id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(255), nullable=False)
    completed = db.Column(db.Boolean, default=False) #default value is important
    date_added = db.Column(db.DateTime, default=datetime.utcnow)
    user_name = db.Column(db.String(255), nullable=True)
    
    def __repr__(self):
        return '<Task %r>' % self.task

# Ensure tables are created before starting the app
with app.app_context():
    db.create_all()
    
@app.route('/', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        try:
            action = request.form.get('action')
            task_description = request.form.get('task')
            task_id = request.form.get('task_id')

            if action == 'add' and task_description:
                new_task = Taskes(task=task_description) #Correctly add task to the database
                db.session.add(new_task)
                db.session.commit()

            elif action == 'delete' and task_id:
                task_to_delete = Taskes.query.get(int(task_id))
                if task_to_delete:
                    db.session.delete(task_to_delete)
                    db.session.commit()

            elif action == 'toggle' and task_id:
                task_to_toggle = Taskes.query.get(int(task_id))
                if task_to_toggle:
                    task_to_toggle.completed = not task_to_toggle.completed
                    db.session.commit()

        except Exception as e:
            db.session.rollback()
            print(f"Database error: {e}") #Log errors for debugging
            return f"Database error: {e}", 500 #Return an error message
    tasks = Taskes.query.all() #Get tasks from database
    return render_template('base2.html', tasks=tasks)



if __name__ == '__main__':
    app.run(debug=True)
