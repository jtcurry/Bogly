"""Blogly application."""

from flask import Flask, render_template, redirect, request, flash
from models import db, connect_db, User, Post

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'newKey'


connect_db(app)
db.create_all()

############################### HOME ROUTES #####################################
@app.route("/")
def redirect_to_users():
    """Redirect to users page showing users list"""
    return redirect("/users")


@app.route("/users")
def show_users():
    """Render page showing user list"""
    users = User.query.all()
    return render_template("users.html", users=users)

############################### USER ROUTES #####################################
@app.route("/users/<int:user_id>")
def show_user_info(user_id):
    """Show info on selected user"""
    user = User.query.get_or_404(user_id)
    user_posts = Post.query.filter_by(user_id=user.id)
    return render_template("userinfo.html", user=user,user_posts=user_posts)


@app.route("/users/<int:user_id>/edit")
def show_user_edit(user_id):
    """Show edit page for a specific user"""
    user = User.query.get_or_404(user_id)
    return render_template("useredit.html", user=user)


@app.route("/users/<int:user_id>/edit", methods=["POST"])
def edit_user(user_id):
    """Edit a current user"""
    user = User.query.get_or_404(user_id)
    user.first_name = request.form['first_name']
    user.last_name = request.form['last_name']
    user.image_url = request.form['image_url']

    db.session.add(user)
    db.session.commit()

    return redirect("/users")


@app.route("/users/new")
def new_user():
    """Show new user form"""
    return render_template("newuser.html")


@app.route("/users/new", methods=["POST"])
def add_new_user():
    """Add new user to database"""
    new_user = User(
        first_name=request.form['first_name'],
        last_name=request.form['last_name'],
        image_url=request.form['image_url'] or None
    )

    db.session.add(new_user)
    db.session.commit()
    flash("New User Created!")
    return redirect("/users")


@app.route("/users/<int:user_id>/delete", methods=["POST"])
def del_user(user_id):
    """Delete selected user"""
    user = User.query.get_or_404(user_id)

    db.session.delete(user)
    db.session.commit()

    return redirect("/users")

############################### POSTS ROUTES #####################################
@app.route("/users/<int:user_id>/posts/new")
def show_post_form(user_id):
    """Show form for adding a new post"""
    user = User.query.get_or_404(user_id)
    return render_template("postform.html", user = user)


@app.route("/users/<int:user_id>/posts/new", methods=["POST"])
def add_post(user_id):
    """Add new post to table"""
    user = User.query.get_or_404(user_id)
    new_post = Post(
        title=request.form['title'],
        content=request.form['content'],
        user = user
    )

    db.session.add(new_post)
    db.session.commit()
    flash("New Post Added!")
    return redirect(f"/users/{user_id}")


@app.route("/posts/<int:post_id>")
def show_post(post_id):
    """Show info on current post"""
    post = Post.query.get_or_404(post_id)
    user = post.user

    return render_template("postdetail.html", post=post, user=user)


@app.route("/posts/<int:post_id>/edit")
def edit_post(post_id):
    """Show form to edit current post"""
    post = Post.query.get_or_404(post_id)

    return render_template("postedit.html", post=post)


@app.route("/posts/<int:post_id>/edit", methods=["POST"])
def submit_edit_post(post_id):
    """Edit a current post"""
    post = Post.query.get_or_404(post_id)
    post.title = request.form['title']
    post.content = request.form['content']
    user = post.user

    db.session.add(post)
    db.session.commit()

    return redirect(f"/users/{user.id}")


@app.route("/posts/<int:post_id>/delete", methods=["POST"])
def delete_post(post_id):
    """Delete selected post from database"""
    post = Post.query.get_or_404(post_id)
    user = post.user
    db.session.delete(post)
    db.session.commit()

    return redirect(f"/users/{user.id}")