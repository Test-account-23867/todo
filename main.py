from flask import Flask, render_template, redirect, url_for, abort,request
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_required, UserMixin, login_user, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from forms import LoginForm,RegisterForm,ItemForm
from flask_bootstrap import Bootstrap
import os 

app=Flask(__name__)
app.secret_key='J8*s0)*srdBTSt7TGA685q667^%^&*^T^*T^†®¥´®¨ˆßªœˆ9hfbw7yerb'
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URI','sqlite:///../user-database.db')
Bootstrap(app)

db=SQLAlchemy(app)

# db models
class User(db.Model, UserMixin):
    id=db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String(250))
    email = db.Column(db.Text, unique=True, nullable=False)
    password = db.Column(db.Text, nullable=False)    
    items = db.relationship('Todo', backref='user')



class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    item = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


# with app.app_context():
#     db.create_all()

# login manager

login_manager=LoginManager(app)


@login_manager.user_loader
def get_user_id(user_id):
    return User.query.get(user_id)


@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('todo'))
    return render_template('index.html')

@app.route('/login', methods=['GET','POST'])
def login():
    form=LoginForm()
    if form.validate_on_submit():
        email=form.email.data
        password=form.password.data
        user=User.query.filter_by(email=email).first()
        
        if user:
            if check_password_hash(user.password, password):
                login_user(user)
                return redirect(url_for('todo'))
            return redirect(url_for('login'))
        
        return redirect(url_for('register'))

    return render_template('login.html', form=form)

@app.route('/register', methods=['GET','POST'])
def register():
    form=RegisterForm()
    if form.validate_on_submit():
        name=form.name.data
        email=form.email.data
        password=form.password.data
        
        user=User(
            name=name,
            email=email, 
            password= generate_password_hash(password)
            )
        db.session.add(user)
        db.session.commit()

        login_user(user)
        return redirect(url_for('login'))

    return render_template('register.html', form=form)

@login_required
@app.route('/todo',methods=['GET','POST'])
def todo():
    items=Todo.query.filter_by(user_id=current_user.id)
    if request.method=='POST':
        item=request.form.get('item')
        new_item=Todo(
            item=item,
            user_id=current_user.id
            )
        db.session.add(new_item)
        db.session.commit()
        return redirect(url_for('todo'))
    return render_template('todo.html', items=items)


@app.route('/delete')
@login_required
def delete():
    id=request.args.get('id')
    todo_item=Todo.query.get(id)
    db.session.delete(todo_item)
    db.session.commit()
    return redirect(url_for('todo'))


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True, host=0.0.0.0)


