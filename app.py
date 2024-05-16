"""Authentication and Authorization"""

from flask import Flask, render_template, redirect, session, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import connect_db, db, User

app = Flask(__name__)
app.app_context().push()

app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///authentication"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True

app.config["SECRET_KEY"] = "abc123"
app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False

connect_db(app)
db.create_all()

toolbar = DebugToolbarExtension(app)


@app.route("/")
def homepage():
    """Show homepage with links to site areas."""

    return redirect("/register")

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register a new user."""
    
    # redirect to secret after form validation

    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    """User log in page."""
    
    # redirect to secret after form validation and authentication

    return render_template("login.html")

@app.route("/secret")
def secret():
    """This is a secrect.
    Only available to registered users"""
    
    # redirect to secret after form validation and authentication

    return render_template("secret.html")