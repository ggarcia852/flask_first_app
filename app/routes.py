from app import app
from flask import render_template, url_for

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