"""Blogly application."""

from flask import Flask, render_template, redirect, request, flash
from models import db, connect_db, User, Post, Tag, PostTag

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
    """Show home page with recent posts"""
    posts = Post.query.order_by(Post.created_at.desc()).limit(5).all()
    return render_template("home.html", posts=posts)


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
    return render_template("userinfo.html", user=user, user_posts=user_posts)


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
    tags = Tag.query.all()
    return render_template("postform.html", user=user, tags=tags)


@app.route("/users/<int:user_id>/posts/new", methods=["POST"])
def add_post(user_id):
    """Add new post to table"""
    user = User.query.get_or_404(user_id)
    tag_ids = [int(num) for num in request.form.getlist("tags")]
    tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()

    new_post = Post(
        title=request.form['title'],
        content=request.form['content'],
        user=user,
        tags=tags
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
    tags = Tag.query.all()
    return render_template("postedit.html", post=post, tags=tags)


@app.route("/posts/<int:post_id>/edit", methods=["POST"])
def submit_edit_post(post_id):
    """Edit a current post"""
    post = Post.query.get_or_404(post_id)
    post.title = request.form['title']
    post.content = request.form['content']
    user = post.user
    tag_ids = [int(num) for num in request.form.getlist("tags")]
    post.tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()

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


############################### TAGS ROUTES #####################################
@app.route("/tags")
def show_tags():
    """Show all tags in a list"""
    tags = Tag.query.all()

    return render_template("tags.html", tags=tags)


@app.route("/tags/<int:tag_id>")
def show_tag_info(tag_id):
    """Show list of all posts with selected tag"""
    tag = Tag.query.get_or_404(tag_id)
    posts = tag.posts

    return render_template("taginfo.html", tag=tag, posts=posts)


@app.route("/tags/new")
def new_tag():
    """Show form for creating new tag"""
    return render_template("newtag.html")


@app.route("/tags/new", methods=["POST"])
def add_new_tag():
    """Add new tag to database"""
    new_tag = Tag(
        name=request.form['tagname']
    )

    db.session.add(new_tag)
    db.session.commit()
    return redirect("/tags")


@app.route("/tags/<int:tag_id>/edit")
def edit_tag(tag_id):
    """Edit selected tag"""
    tag = Tag.query.get_or_404(tag_id)

    return render_template("edittag.html", tag=tag)


@app.route("/tags/<int:tag_id>/edit", methods=["POST"])
def submit_edit_tag(tag_id):
    """Edit a current tag"""
    tag = Tag.query.get_or_404(tag_id)
    tag.name = request.form['tagname']

    db.session.add(tag)
    db.session.commit()

    return redirect("/tags")


@app.route("/tags/<int:tag_id>/delete", methods=["POST"])
def delete_tag(tag_id):
    """Delete selected tag from database"""
    tag = Tag.query.get_or_404(tag_id)
    db.session.delete(tag)
    db.session.commit()

    return redirect("/tags")
