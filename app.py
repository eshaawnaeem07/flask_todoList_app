from flask import Flask, redirect , request, render_template    
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Todo(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False) # Title of the todo item
    desc = db.Column(db.String(200), nullable=True) # Description of the todo item

    def __repr__(self)->str:
        return f"<Todo {self.title}-{self.sno}>"

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        title = request.form['title']           # Get the title from the form
        desc = request.form['desc']             # Get the description from the form
        todo = Todo(title=title, desc=desc)     # Create a new Todo object
        db.session.add(todo)                     # Add the new todo item to the session
        db.session.commit()                      # Commit the session to save the item to the database

    allTodo = Todo.query.all() # Retrieve all todo items from the database
    return render_template('index.html' , allTodo=allTodo)
@app.route('/delete/<int:sno>')
def delete(sno):
    allTodo = Todo.query.filter_by(sno=sno).first() # Retrieve all todo items from the database
    db.session.delete(allTodo)
    db.session.commit()
    return redirect('/')

@app.route('/update/<int:sno>', methods=['GET', 'POST'])
def update(sno):
    todo = Todo.query.filter_by(sno=sno).first()  # Fetch the specific ToDo item

    if request.method == 'POST':
        todo.title = request.form['title']
        todo.desc = request.form['desc']
        db.session.commit()
        return redirect('/')

    return render_template('update.html', todo=todo)


@app.route('/about')
def about():
    print("This is about page")
    return redirect('/about')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=50100, debug=True)