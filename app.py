# flask and sqlalchemy in required for app to work
# render_template needed for html file
# request is something for db
# redirect is for 'refresh'
from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

#config for flask and sqlalchemy/sqlite
app = Flask(__name__)
# this one tell's db where is app
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
# init db
db = SQLAlchemy(app)

# db model
class Todo(db.Model):
    # id int that references to db column for each entery??
    # primary_key is unique identifyer for all data in db
    id = db.Column(db.Integer, primary_key=True)
    #this hold eache task, cant be more then 200 car
    # and supposed to not let user leave blank space for task
    # but does not work
    content = db.Column(db.String(200), nullable=False)
    # i don't know what this is, and why it was in course
    # i just know that it crashes the app
    #completed = db.Column(db.Integer, default=0)
    # to keep track when change or task was added
    # btw for this u need to import datetime
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    # this returns input
    def __repr__(self):
        # this is telling it what to return
        return '<Task %r>' % self.id

# basics of flask, check website
# default method is just GET, now it can be posted
# / is just default route
@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        # variable task content request form...
        task_content = request.form['content']
        # new content = content input in Todo model...
        new_task = Todo(content=task_content)
        try:
            # this one push it to the db
            db.session.add(new_task)
            # this commits
            db.session.commit()
            # return index.html / refreshes page and add new
            # stuff to the db and shows
            return redirect('/')
        except:
            return 'There was an issue adding your task'
    else:
        # this variable put on screen what is taken from db
        # instedef of .all there can be .first to show 
        # just most recent added one
        tasks = Todo.query.order_by(Todo.date_created).all()
        # don't need so specify folder, cuz flask devs
        # did that for me
        return render_template('index.html', tasks=tasks)

@app.route('/delete/<int:id>')
def delete(id):
    # this one is looking for info in db, and if it
    #does't exist it will return 404
    task_to_delete = Todo.query.get_or_404(id)
    try:
        # this delete
        db.session.delete(task_to_delete)
        # this (jesus) saves
        db.session.commit()
        # refresh
        return redirect('/')
    except:
        return 'there was a problem deleting your task'

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    task = Todo.query.get_or_404(id)
    if request.method == 'POST':
        task.content = request.form['content']
        try:
            db.session.commit()
            return redirect('/')
        except: 'there was an issue updating your task'
    else:
        return render_template('update.html', task=task)

# i guess that debug should be false in production site
# bc this shows bug/error on the site
if __name__ == "__main__":
    app.run(debug=True)
