"""Blogly application."""

from flask import Flask, render_template, redirect, request
from models import db, connect_db, User

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True


connect_db(app)
db.create_all()


@app.route("/")
def redirect_to_users():
    """Redirect to users page showing users list"""
    return redirect("/users")


@app.route("/users")
def show_users():
    """Render page showing user list"""
    users = User.query.all()
    return render_template("users.html", users=users)


@app.route("/users/<int:user_id>")
def show_user_info(user_id):
    """Show info on selected user"""
    user = User.query.get_or_404(user_id)
    return render_template("userinfo.html", user=user)


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

    return redirect("/users")


@app.route("/users/<int:user_id>/delete", methods=["POST"])
def del_user(user_id):
    """Delete selected user"""
    user = User.query.get_or_404(user_id)

    db.session.delete(user)
    db.session.commit()

    return redirect("/users")
