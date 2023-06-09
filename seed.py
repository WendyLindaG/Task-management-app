from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Task, User, Project
from datetime import datetime


# Create the engine and session
engine = create_engine('sqlite:///tasks.db')
Session = sessionmaker(bind=engine)
session = Session()

def seed_data():
    # Create users
    users = [
        User(username='user1', email='user1@example.com'),
        User(username='user2', email='user2@example.com'),
        User(username='user3', email='user3@example.com')
        # Add more users as needed
    ]
    session.add_all(users)

    # Create projects
    projects = [
        Project(name='Project A', description='Description of Project A'),
        Project(name='Project B', description='Description of Project B')
        # Add more projects as needed
    ]
    session.add_all(projects)

    # Create tasks
    tasks = [
        Task(title='Task 1', description='Description of Task 1', status='Pending', due_date=datetime.now(), project_id=1),
        Task(title='Task 2', description='Description of Task 2', status='In Progress', due_date=datetime.now(), project_id=2)
        # Add more tasks as needed
    ]
    session.add_all(tasks)

    session.commit()
    session.close()

# Seed the data
seed_data()
