"""Seed file to make sample data for db."""

from models import db, User, Feedback

# Drop existing tables and create new ones
db.drop_all()
db.create_all()

# Sample user data
USERS = [
    {
        "username": "johndoe",
        "pwd": "password123",
        "email": "johndoe@example.com",
        "first_name": "John",
        "last_name": "Doe",
    },
    {
        "username": "janedoe",
        "pwd": "doe456",
        "email": "janedoe@example.com",
        "first_name": "Jane",
        "last_name": "Doe",
    },
    {
        "username": "alice_smith",
        "pwd": "alicepass",
        "email": "alice.smith@example.com",
        "first_name": "Alice",
        "last_name": "Smith",
    }
]

# Sample comments data
COMMENTS = [
    {"username": "johndoe", "title": "First Comment", "comment": "This is John's first comment."},
    {"username": "johndoe", "title": "Second Comment", "comment": "This is John's second comment."},
    {"username": "janedoe", "title": "First Comment", "comment": "This is Jane's first comment."},
    {"username": "janedoe", "title": "Second Comment", "comment": "This is Jane's second comment."},
    {"username": "alice_smith", "title": "First Comment", "comment": "This is Alice's first comment."},
    {"username": "alice_smith", "title": "Second Comment", "comment": "This is Alice's second comment."},
]

# Seed users
for user_data in USERS:
    user = User.register(**user_data)
    db.session.add(user)

# Seed comments and associate them with users
for comment_data in COMMENTS:
    user = User.query.filter_by(username=comment_data["username"]).first()
    if user:
        comment = Feedback(title=comment_data["title"], comment=comment_data["comment"], user=user)
        db.session.add(comment)

# Commit changes
db.session.commit()


