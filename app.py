from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
# import pkg_resources.py2_warn #will be used when we make .exe file of app.py
from flaskwebgui import FlaskUI
from datetime import datetime

app = Flask(__name__)

ui = FlaskUI(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(200))
    complete = db.Column(db.Boolean)

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(20))
    content = db.Column(db.String(1000))
    date_created = db.Column(db.DateTime)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/note/<int:id>')
def note(id):
    note = Note.query.filter_by(id=id).one()

    return render_template("note.html", note=note)

@app.route('/notes')
def notes():
    notes = Note.query.order_by(Note.date_created.desc()).all()

    return render_template("notes.html", notes=notes)

@app.route('/add_note', methods=["GET", "POST"])
def add_note():
    if request.method == "POST":
        title = request.form['title']
        content = request.form['content']
        note = Note(title=title, content=content, date_created=datetime.now())
        db.session.add(note)
        db.session.commit()

        return redirect(url_for("notes"))
    return render_template("add_note.html")

@app.route('/todo')
def todo():
    #show all todo
    todo_list = Todo.query.all()
    return render_template("todo.html", todo_list=todo_list)


@app.route('/add', methods=["POST", "GET"])
def add():
    task = request.form.get("task")
    new_todo = Todo(task=task, complete=False)
    db.session.add(new_todo)
    db.session.commit()
    return redirect(url_for("todo"))

@app.route('/update/<int:todo_id>')
def update(todo_id):
    todo = Todo.query.filter_by(id=todo_id).first()
    todo.complete = not todo.complete
    db.session.commit()
    return redirect(url_for("todo"))

@app.route('/delete/<int:todo_id>')
def delete(todo_id):
    todo = Todo.query.filter_by(id=todo_id).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for("todo"))


db.create_all()
ui.run()
    