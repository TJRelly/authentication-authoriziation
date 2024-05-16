"""Seed file to make sample data for db."""

from models import db, User

# Create all tables
db.drop_all()
db.create_all()

USERS = [
    {
        "username": "johndoe",
        "password": "password123",
        "email": "johndoe@example.com",
        "first_name": "John",
        "last_name": "Doe"
    },
    {
        "username": "janedoe",
        "password": "doe456",
        "email": "janedoe@example.com",
        "first_name": "Jane",
        "last_name": "Doe"
    },
    {
        "username": "alice_smith",
        "password": "alicepass",
        "email": "alice.smith@example.com",
        "first_name": "Alice",
        "last_name": "Smith"
    }
]

for user_data in USERS:
    user = User(**user_data)
    db.session.add(user)

db.session.commit()

