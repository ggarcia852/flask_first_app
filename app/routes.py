from re import U
from app import app
from flask import render_template, url_for
from app.forms import UserInfoForm

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
        print("Form submitted correctly")
        username = register_form.username.data
        email = register_form.email.data
        password = register_form.password.data
        print(username, email, password)
    return render_template('register.html', form=register_form)