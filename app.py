"""Blogly application."""

from flask import Flask, request, redirect, render_template
from models import db, connect_db, User
from flask_debugtoolbar import DebugToolbarExtension


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "SECRET!"

# Having the Debug Toolbar show redirects explicitly is often useful;
# however, if you want to turn it off, you can uncomment this line:
#
# app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

toolbar = DebugToolbarExtension(app)

connect_db(app)
db.create_all()

@app.route("/")
def list_users():
    """List users"""

    return redirect("/users")

# User route

@app.route("/users")
def users_index():
    """Show a page with info on all users"""
    users = User.query.order_by(User.last_name, User.first_name).all()
    return render_template("users/index.html", users=users)

@app.route("/users/new", methods=["GET"])
def new_user_form():
    """Show form to create a new user"""
    return render_template("users/new.html")

@app.route("/users/new", methods=["POST"])
def users_new():
    """Handle adding a new user via form submission"""
    new_user = User(
        first_name=request.form["first_name"], 
        last_name=request.form["last_name"], 
        image_url=request.form["image_url"])
    
    db.session.add(new_user)
    db.session.commit()
    
    return redirect("/users")

@app.route('/users/<int:user_id>')
def users_show(user_id):
    """Show info on a specific user"""
    user = User.query.get_or_404(user_id)
    return render_template("users/show.html", user=user)

@app.route('/users/<int:user_id>/edit')
def users_edit(user_id):
    """Show edit form for a specific user"""
    user = User.query.get_or_404(user_id)
    
    return render_template("users/edit.html", user=user)

@app.route('/users/<int:user_id>/edit', methods=["POST"])
def users_update(user_id):
    """Handle edit form submission for a specific user"""
    user = User.query.get_or_404(user_id)
    
    user.first_name = request.form["first_name"]
    user.last_name = request.form["last_name"]
    user.image_url = request.form["image_url"]
    
    db.session.add(user)
    db.session.commit()
    
    return redirect("/users")

@app.route('/users/<int:user_id>/delete', methods=["POST"])
def users_destroy(user_id):
    """Handle form submission for deleting an existing user"""

    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()

    return redirect("/users")
