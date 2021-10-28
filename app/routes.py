from app import app, db, mail
from flask import render_template, url_for, redirect, flash, jsonify, request
from flask_mail import Message
from app.forms import LoginForm, UserInfoForm,  PostForm
from app.models import Post, User
from flask_login import login_user, logout_user, current_user, login_required
from flask_httpauth import HTTPBasicAuth

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
        
        flash(f'{post.title} has been updated', 'success')
        return redirect(url_for('post_detail', post_id=post.id))
    return render_template('post_update.html', post=post, form=form)


@app.route('/posts/<int:post_id>/delete', methods=['POST'])
@login_required
def post_delete(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        flash("You cannot delete this post", 'danger')
        return redirect(url_for('my_posts'))

    db.session.delete(post)
    db.session.commit()

    flash("Your post has been deleted", 'success')
    return redirect(url_for('my_posts'))




################    Start of JSON/API     #######################


@app.route('/api/users')
def get_users():
    """
    [GET] /api/users - Returns all users
    """
    users = User.query.all()
    return jsonify([u.to_dict() for u in users])


@app.route('/api/users/<id>')
def get_user(id):
    """
    [GET] /api/users/<user_id> - Returns 1 user
    """
    user = User.query.get_or_404(id)
    return jsonify(user.to_dict())


@app.route('/api/users', methods=['POST'])
def create_user():
    data = request.json
    for field in ['username', 'email', 'password']:
        if field not in data:
            return jsonify({'error': f'You are missing the {field} field'}), 400

    # Grab data from request body     
    username = data['username']
    email = data['email']
    password = data['password']

    #Check if existing user
    existing_user = User.query.filter_by(username=username).all()
    if existing_user:
        return jsonify({'error': f'The username {username} is already in use. Please try again.'}), 400

    #Create new user
    new_user = User(username, email, password)
    new_user.save()


    return jsonify(new_user.to_dict())


@app.route('/api/users/<id>', methods=['PUT'])
def update_user(id):
    user = User.query.get_or_404(id)
    data = request.json
    user.update_user(data)
    return jsonify(user.to_dict())


@app.route('/api/users/<id>', methods=['DELETE'])
def delete_user(id):
    pass



# basic_auth = HTTPBasicAuth()

# @basic_auth.verify_password
# def verify(username, password):
#     user = User.query.filter_by(username=username).first()
#     if user and user.check_password(password):
#         return user


# @app.route('/api/token', methods=['POST'])
# @basic_auth.login_required
# def get_token():
#     token = basic_auth.current_user().get_token()
#     return jsonify({'token': token})




@app.route('/api/posts')
def get_posts():
    """
    [GET] /api/posts - Returns all posts
    """
    posts = Post.query.all()
    return jsonify([p.to_dict() for p in posts])


@app.route('/api/posts/<id>')
def get_post(id):
    """
    [GET] /api/posts/<user_id> - Returns 1 post
    """
    post = Post.query.get_or_404(id)
    return jsonify(post.to_dict())


@app.route('/api/posts', methods=['POST'])
def create_post():
    data = request.json
    for field in ['title', 'content', 'user_id']:
        if field not in data:
            return jsonify({'error': f'You are missing the {field} field'}), 400
     
    title = data['title']
    content = data['content']
    user_id = data['user_id']

    new_post = Post(title, content, user_id)
    new_post.save()

    return jsonify(new_post.to_dict())


@app.route('/api/posts/<id>', methods=['PUT'])
def update_post(id):
    post = Post.query.get_or_404(id)
    data = request.json
    post.update_post(data)
    return jsonify(post.to_dict())


@app.route('/api/posts/<id>', methods=['DELETE'])
def delete_post(id):
    pass