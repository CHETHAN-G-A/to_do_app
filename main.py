from flask import Flask, render_template ,request ,redirect ,url_for,flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from forms import LoginForm, RegistrationForm, TodoForm ,UpdateForm
from flask_bcrypt import Bcrypt

app = Flask(__name__)


#Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'SECRET_KEY'
db = SQLAlchemy(app)

bcrypt = Bcrypt(app)

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


##Login page##
@app.route("/login",methods=['GET','POST'])
def login():
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        user = User.query.filter_by(email=form.email.data).first()
        if not user:
            flash("That email does not exist, please try again.")
            return redirect(url_for('login'))
        elif user and bcrypt.check_password_hash(user.password, form.password.data):
            flash(f'welcome {user.email} you are logged in now')
            user = user.id
            return redirect(url_for('todo', id=user))
        else:
            flash('wrong password please try again')
            return redirect(url_for('login'))
    return render_template('login.html', form=form)

##Register page##
@app.route("/register" , methods=['GET','POST'])
def register():
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        hashed_password = bcrypt.generate_password_hash(form.password.data)
        user = User(name=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Thanks for registering')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

## Main page ##
@app.route("/todo/<int:id>" , methods=['GET','POST'])
def todo(id):
    form =TodoForm(request.form)
    if request.method == 'POST':
        new_todo = Todo(title=form.title.data,desc=form.description.data,user_id=id)
        db.session.add(new_todo)
        db.session.commit()
        return redirect(url_for('todo',id=id))
    all_todo = Todo.query.filter_by(user_id=id)
    return render_template("index.html" , all_todo=all_todo ,user=id , form=form)


@app.route("/delete/<int:sno>/<int:user_id>")
def delete(sno,user_id):
    todo = Todo.query.filter_by(sno=sno).first()
    db.session.delete(todo)
    db.session.commit()

    user = user_id
    return redirect(url_for('todo',id=user))


@app.route("/update/<int:sno>",methods=['GET','POST'])
def update(sno):
    form = UpdateForm(request.form)
    if request.method == 'POST':
        title = form.title.data
        desc = form.description.data
        todo = Todo.query.filter_by(sno=sno).first()
        todo.title = title
        todo.desc = desc
        db.session.add(todo)
        db.session.commit()
        user = todo.user_id
        return redirect(url_for('todo',id=user))
    todo = Todo.query.filter_by(sno=sno).first()
    return render_template("update.html",todo=todo ,form=form)


if __name__=='__main__':
    app.run(debug=True)