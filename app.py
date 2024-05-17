"""Authentication and Authorization"""

from flask import Flask, render_template, redirect, session, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import Feedback, connect_db, db, User
from forms import EditFeedbackForm, LoginForm, RegisterForm

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

    return render_template("home.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register a new user."""
    
    form = RegisterForm()
    
    if form.validate_on_submit():
        user_data = {
            "username": form.username.data,
            "pwd": form.password.data,
            "email": form.email.data,
            "first_name": form.first_name.data,
            "last_name": form.last_name.data
        }
           
        new_user = User.register(**user_data)
        
        try:
            db.session.add(new_user)
            db.session.commit()
            
            first_name = user_data["first_name"]      
            session["username"] = new_user.username
            
            flash(f"{first_name}, you are registered!")
            return redirect(f"/users/{new_user.username}")
        
        except:
            db.session.rollback()
            flash("Email/Username already exists. Please choose a different one.", "error")
            return redirect("/register")
        
    else:
        return render_template("register.html", form=form)

@app.route("/login", methods=["GET", "POST"])
def login():
    """User log in page."""
    
    form = LoginForm()
    
    if form.validate_on_submit():
        user_data = {
            "username": form.username.data,
            "pwd": form.password.data,
        }
           
        user = User.authenticate(**user_data)
        
        if user:
            # keep logged in
            session["username"] = user.username
            return redirect(f"/users/{user.username}")

        else:
            form.username.errors = ["Bad name/password"]
    
    # redirect to user_page after form validation and authentication

    return render_template("login.html", form=form)

@app.route("/users/<username>")
def user_page(username):
    """page for logged-in users only."""

    if "username" not in session:
        flash("You must be logged in to view!")
        return redirect("/")

    else:
        user = User.query.get_or_404(username)
        return render_template("user_page.html", user=user)

@app.route("/logout")
def logout():
    """Logs user out and redirects to homepage."""
    
    if "username" in session:
        flash("You've been logged out.")
        session.pop("username")

    return redirect("/login")

@app.route("/feedback/<comment_id>", methods=["GET", "POST"])
def show_feedback(comment_id):
    """Displays user feedback."""
    
    if "username" not in session:
        flash("You must be logged in to view!")
        return redirect("/")

    else:
        comment = Feedback.query.get_or_404(comment_id)
        
        form = EditFeedbackForm(obj=comment)
        
        if form.validate_on_submit():
            feedback_data = {
                "title": form.title.data,
                "comment": form.comment.data
            }
            
            comment.title = feedback_data.get("title")
            comment.comment = feedback_data.get("comment")
            
            db.session.add(comment)
            db.session.commit()
                
            flash(f"You've successfully edited your comment.")
            
            return redirect(f"/feedback/{comment.id}")
        
        else:
            return render_template("feedback_page.html", comment=comment, form=form)
    
@app.route("/feedback/<comment_id>/delete")
def delete_feedback(comment_id):
    """Displays user feedback."""
    
    if "username" not in session:
        flash("You must be logged in to view!")
        return redirect("/")

    else:
        comment = Feedback.query.get_or_404(comment_id)
        username = comment.user.username
        flash("You successfully deleted the comment.")
        db.session.delete(comment)
        db.session.commit()
        return redirect(f"/users/{username}")
    
@app.route("/users/<username>/delete", methods=["POST"])
def delete_user(username):
    """Displays user feedback."""
    
    if "username" not in session:
        flash("You must be logged in to view!")
        return redirect("/")

    else:
        username = User.query.get_or_404(username)
        db.session.delete(username)
        db.session.commit()
        
        flash("You successfully deleted your account.")
        return redirect(f"/")
    
@app.route("/users/<username>/feedback/add", methods=["GET", "POST"])
def add_feedback(username):
    """Adds new user feedback."""
    
    if "username" not in session:
        flash("You must be logged in to view!")
        return redirect("/")

    else:
        user = User.query.get_or_404(username)
        
        form = EditFeedbackForm()
        
        if form.validate_on_submit():
            feedback_data = {
                "title": form.title.data,
                "comment": form.comment.data
            }
            
            comment = Feedback(title=feedback_data.get("title"), comment=feedback_data.get("comment"), username=user.username)
           
            db.session.add(comment)
            db.session.commit()
                
            flash(f"You've successfully added your comment.")
            
            return redirect(f"/users/{user.username}")
        
        else:
            return render_template("feedback_add_page.html", form=form, user=user)