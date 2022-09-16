from flask import Flask, render_template ,request ,redirect ,url_for,flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

#CONNECT TO DB

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

#users db

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

#CONFIGURE TABLES
class Todo(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    desc = db.Column(db.String(500), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow())
    user_id = db.Column(db.Integer, nullable=False)
db.create_all()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))
db.create_all()

@app.route("/login",methods=['GET','POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email_add')
        password = request.form.get('password')
        user = User.query.filter_by(email=request.form["email_add"]).first()
        if not user:
            flash("That email does not exist, please try again.")
            return redirect(url_for('login'))
        elif user.password != request.form["password"]:
            flash("Incorrect Password")
            return redirect(url_for('login'))
        if user.password==request.form["password"]:
            x = user.id
            return redirect(url_for('home',id=x))

    return render_template("login.html")

@app.route("/<int:id>" , methods=['GET','POST'])
def home(id):
    if request.method == 'POST':
        new_todo = Todo(title=request.form["title"],desc=request.form["desc"],user_id=id)
        db.session.add(new_todo)
        db.session.commit()
    all_todo = Todo.query.filter_by(user_id=id)

    return render_template("index.html" , all_todo=all_todo ,user=id)


@app.route("/delete/<int:sno>")
def delete(sno):
    todo = Todo.query.filter_by(sno=sno).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for("home"))

@app.route("/update/<int:sno>",methods=['GET','POST'])
def update(sno):
    if request.method == 'POST':
        title = request.form["title"]
        desc = request.form["desc"]
        todo = Todo.query.filter_by(sno=sno).first()
        todo.title = title
        todo.desc = desc
        db.session.add(todo)
        db.session.commit()
        user = todo.user_id
        return redirect(url_for('home',id=user))
    todo = Todo.query.filter_by(sno=sno).first()
    return render_template("update.html",todo=todo)



@app.route("/register" , methods=['GET','POST'])
def register():
    if request.method == 'POST':
        new_user = User(email=request.form["email_add"], password=request.form["password"],name=request.form["name"])
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template("register.html")

if __name__=='__main__':
    app.run(debug=True)