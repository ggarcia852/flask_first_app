from app import app
from flask import render_template, url_for, redirect, flash
from app.forms import UserInfoForm,  PostForm
from app.models import Post, User
from app import db

@app.route('/')
def index():
    title = "My First App"
    user = "George"
    return render_template('index.html', user=user, title=title)


@app.route('/favs')
def favs():
    title= 'Five Favorite Countries'
    countries= ['Thailand', 'Spain', 'India', 'New Zealand', 'Nepal']
    return render_template('favs.html', title=title, countries=countries)

@app.route('/todo')
def todo():
    title= 'Countries to Visit'
    countries= ['Brazil', 'South Africa', 'Japan', 'Greece', 'Peru']
    return render_template('todo.html', title=title, countries=countries)


@app.route('/register', methods=['GET', 'POST'])
def register():
    register_form = UserInfoForm()
    if register_form.validate_on_submit():
        username = register_form.username.data
        email = register_form.email.data
        password = register_form.password.data

        existing_user = User.query.filter_by(username=username).all()
        if existing_user:
            flash(f'The username {username} is already in use. Please try again.', 'danger')
            return redirect(url_for('register'))

        new_user = User(username, email, password)
        db.session.add(new_user)
        db.session.commit()

        flash(f'Thank you {username}, you have successfully registered!', 'success')
        return redirect(url_for('index'))

    return render_template('register.html', form=register_form)


@app.route('/createpost', methods=['GET', 'POST'])
def createpost():
    form = PostForm()
    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data

        new_post = Post(title, content, user_id=1)
        db.session.add(new_post)
        db.session.commit()

        
        
    return render_template('createpost.html', form=form)