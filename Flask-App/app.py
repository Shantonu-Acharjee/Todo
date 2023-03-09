from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import date


app = Flask(__name__)
todayDate = date.today()
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)



class Todo(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    status = db.Column(db.String(5), nullable=False)
    date_created = db.Column(db.DateTime, default = todayDate)
    

    def __repr__(self) -> str:
        return f"{self.sno} - {self.title}"

#with app.app_context():
#   db.create_all()




@app.route('/', methods = ['GET', 'POST'])
def index():
    if request.method == 'POST':
        title = request.form["title"]
        status = 'N'
        print(title)

        todo = Todo(title = title, status = status)
        db.session.add(todo)
        db.session.commit()

    allTodo = Todo.query.all()   
    return render_template('home.html', todayDate = todayDate, allTodo = allTodo)



@app.route('/delete/<int:sno>')
def delete(sno):
    todo = Todo.query.filter_by(sno=sno).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect("/")





if __name__ == '__main__':
    app.run(debug = True)