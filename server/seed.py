#!/usr/bin/env python3

from random import choice as rc
from faker import Faker
from app import app
from models import db, Message

fake = Faker()

usernames = [fake.first_name() for i in range(4)]
if "Duane" not in usernames:
    usernames.append("Duane")

def make_messages():
    print("Running make_messages...")  # Debugging print
    Message.query.delete()
    print("Deleted existing messages.")  # Debugging print

    messages = []

    for i in range(20):
        message = Message(
            body=fake.sentence(),
            username=rc(usernames),
        )
        messages.append(message)

    print(f"Prepared {len(messages)} messages.")  # Debugging print
    db.session.add_all(messages)
    db.session.commit()
    print("Messages committed to the database.")  # Debugging print

if __name__ == '__main__':
    with app.app_context():
        print("App context initialized.")  # Debugging print
        make_messages()


