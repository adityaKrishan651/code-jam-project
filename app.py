from flask import Flask, render_template, redirect, url_for, send_file, request
from flask_sqlalchemy import SQLAlchemy
# import pkg_resources.py2_warn #will be used when we make .exe file of app.py
from flaskwebgui import FlaskUI
from datetime import datetime
from win10toast import ToastNotifier
import random
from flask_uploads import UploadSet, configure_uploads, ALL

toaster = ToastNotifier()

app = Flask(__name__)

ui = FlaskUI(app)

all = UploadSet(name='files', extensions=('txt', '.py', 'rtf', 'odf', 'ods', 'gnumeric', 'abw', 'doc', 'docx', 'xls', 'xlsx', 'jpg', 'jpe', 'jpeg', 'png', 'gif', 'svg', 'bmp', 'csv', 'ini', 'json', 'plist', 'xml', 'yaml', 'yml', 'pdf'))

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///datebase.db"
app.config['UPLOADED_FILES_DEST'] = 'uploads'
db = SQLAlchemy(app)
configure_uploads(app, all)


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(200))
    time = db.Column(db.String(20))
    complete = db.Column(db.Boolean)

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(20))
    content = db.Column(db.String(1000))
    date_created = db.Column(db.DateTime)


class File(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    file_name = db.Column(db.String(50))
    path = db.Column(db.String(20))

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

@app.route('/delete_note/<int:id>')
def delete_note(id):
    note = Note.query.get_or_404(id)
    db.session.delete(note)
    db.session.commit()
    return redirect(url_for("notes"))

@app.route('/todo')
def todo():
    #show all todo
    todo_list = Todo.query.all()
    return render_template("todo.html", todo_list=todo_list)


@app.route('/add', methods=["POST", "GET"])
def add():
    task = request.form["task"]
    time = request.form["time"]
    new_todo = Todo(task=task, time=time, complete=False)
    toaster.show_toast(f"Reminder for {task}", f"You have to do {task} by {time} today!")
    db.session.add(new_todo)
    db.session.commit()
    return redirect(url_for("todo"))

@app.route('/update/<int:id>')
def update(id):
    todo = Todo.query.get_or_404(id)
    todo.complete = not todo.complete
    db.session.commit()
    return redirect(url_for("todo"))

@app.route('/delete/<int:id>')
def delete(id):
    todo = Todo.query.get_or_404(id)
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for("todo"))

@app.route('/cal')
def cal():
    return render_template("calculator.html")

@app.route('/quote')
def quote():
    with open("quotes.txt", "r") as q:
        q = q.readlines()
        q = random.choice(q)
    return render_template("quote.html", quote=q)

@app.route('/upload', methods=["POST", "GET"])
def upload():
    files = File.query.all()
    if request.method == "POST":
        filename = all.save(request.files['file'])
        path = "uploads/" + filename
        files = File(file_name=filename, path=path)
        db.session.add(files)
        db.session.commit()
        files = File.query.all()
        return render_template("upload.html", files=files)
    return render_template("upload.html", files=files)

@app.route('/download/<int:id>', methods=['GET', 'POST'])
def download(id):
    file_ = File.query.get_or_404(id)

    return send_file(file_.path, as_attachment=True, attachment_filename=file_.file_name)

@app.route('/clock')
def clock():
    return render_template("clock.html")

db.create_all()
ui.run()
