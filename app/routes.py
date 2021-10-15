from app import app, db, mail
from flask import render_template, url_for, redirect, flash
from flask_mail import Message
from app.forms import LoginForm, UserInfoForm,  PostForm
from app.models import Post, User
from flask_login import login_user, logout_user, current_user, login_required

@app.route('/')
def index():
    title = "My First App"
    posts = Post.query.all()
    return render_template('index.html', title=title, posts=posts)


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

        welcome_message = Message('Welcome to my blog', [email])
        welcome_message.body = f'Dear {username}, thanks for signing up for my blog'
        mail.send(welcome_message)

        return redirect(url_for('index'))

    return render_template('register.html', form=register_form)

@app.route('/login', methods =['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        #grab data from form
        username = form.username.data
        password = form.password.data

        #query user table for username
        user = User.query.filter_by(username=username).first()

        # check if user in None or if password is incorrect
        if user is None or not user.check_password(password):
            flash('wrong username or password', 'danger')
            return redirect(url_for('login'))

        #login user if username/password is correct
        login_user(user)
        flash(f'Welcome {user.username}, you have successfully logged in.', 'success')
        return redirect(url_for('index'))



    return render_template('login.html', login_form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))



@app.route('/createpost', methods=['GET', 'POST'])
@login_required
def createpost():
    form = PostForm()
    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data

        new_post = Post(title, content, current_user.id)
        db.session.add(new_post)
        db.session.commit()

        flash(f'Your post {title} has been created', 'primary')
        return redirect(url_for('index'))
    return render_template('createpost.html', form=form)

@app.route('/myaccount')
@login_required
def my_account():
    return render_template('my_account.html')

@app.route('/myposts')
@login_required
def my_posts():
    posts = current_user.posts
    return render_template('my_posts.html', posts=posts)

@app.route('/posts/<int:post_id>')
def post_detail(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post_detail.html', post=post)

@app.route('/posts/<int:post_id>/update', methods=['GET', 'POST'])
@login_required
def post_update(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author.id != current_user.id:
        flash('This is not your post')
        return redirect(url_for('my_posts'))

    form = PostForm()
    if form.validate_on_submit():
        new_title = form.title.data
        new_content = form.content.data
        post.title = new_title
        post.content = new_content
        db.session.commit()
        
        flash(f'The {post.title} has been updated', 'success')
        return redirect(url_for('post_detail', post_id=post.id))
    return render_template('post_update.html', post=post, form=form)


@app.route('/posts/<int:post_id>/delete', methods=['POST'])
@login_required
def post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        flash("you cannot delete this post", 'danger')
        return redirect(url_for('my_posts'))

    db.session.delete(post)
    db.session.commit()

    flash("you post has been deleted", 'primary')
    return redirect(url_for('my_posts'))