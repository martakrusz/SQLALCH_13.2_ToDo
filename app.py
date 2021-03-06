from flask import (
    Flask, 
    render_template, 
    request, 
    redirect, 
    url_for,
)
from flask_sqlalchemy import SQLAlchemy
from config import Config

app = Flask(__name__)

app.config.from_object(Config)
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(100), nullable=False)
    complete = db.Column(db.Boolean)

@app.route('/')
def index():
    todo_list = Todo.query.all()
    print(todo_list)
    return render_template('base.html', todo_list=todo_list)

@app.route('/add', methods =["POST"] )
def add():
    #add new item
    try:
        title = request.form.get("title")
        description = request.form.get("description")
        new_todo = Todo(title=title, description=description, complete=False)
        db.session.add(new_todo)
        db.session.commit()
        return redirect(url_for("index"))
    except ValueError as error:
        return render_template("base.html", message=str(error))

@app.route('/update/<int:todo_id>')
def update(todo_id):
    #update item
    todo = Todo.query.filter_by(id=todo_id).first()
    todo.complete = not todo.complete
    db.session.commit()
    return redirect(url_for("index"))

@app.route('/delete/<int:todo_id>')
def delete(todo_id):
    #delete item
    todo = Todo.query.filter_by(id=todo_id).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for("index"))
db.create_all()
if __name__=="__main__":
    app.run(debug=True)
