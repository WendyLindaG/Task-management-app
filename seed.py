from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Task, User
from datetime import datetime


engine = create_engine('sqlite:///tasks.db')
Session = sessionmaker(bind=engine)
session = Session()

def seed_data():
    users = [
        User(username="user1", email='user1@example.com'),
        User(username='user2', email='user2@example.com'),
        User(username='user3', email='user3@example.com')
    ]
    session.add_all(users)

    tasks = [
        Task(title='Task 1', description='Description of Task 1', status='Pending', due_date=datetime.now()),
        Task(title='Task 2', description='Description of Task 2', status='In Progress', due_date=datetime.now())
    ]
    session.add_all(tasks)

    session.commit()
    session.close()

seed_data()
