import click
from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship


Base = declarative_base()
engine = create_engine('sqlite:///tasks.db', echo=True)

task_user = Table(
    'task_user', Base.metadata,
    Column('task_id', Integer, ForeignKey('tasks.id')),
    Column('user_id', Integer, ForeignKey('users.id'))
)


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String)
    email = Column(String)
    tasks = relationship("Task", secondary=task_user, back_populates="users")

    def __init__(self, username, email):
        self.username = username
        self.email = email

class Task(Base):
    __tablename__ = 'tasks'
    id = Column(Integer, primary_key=True)
    title = Column(String)
    description = Column(String)
    status = Column(String)
    due_date = Column(DateTime)
    project_id = Column(Integer, ForeignKey('projects.id'))
    users = relationship("User", secondary=task_user, back_populates="tasks")
    comments = relationship("Comment", back_populates="task")
                            

class Comment(Base):
    __tablename__ = 'comments'
    id = Column(Integer, primary_key=True)
    content = Column(String)
    created_at = Column(DateTime, default=datetime.now)
    task_id = Column(Integer, ForeignKey('tasks.id'))
    task = relationship("Task", backref="all_comments")


class TaskManager:
    def __init__(self):
        self.tasks = []
        engine = create_engine('sqlite:///tasks.db')
        Base.metadata.create_all(engine)
        Session = sessionmaker(bind=engine)
        self.session = Session()

    def add_task(self, title, description, status, due_date):
        new_task = Task(title=title, description=description, status=status, due_date=due_date)
        self.session.add(new_task)
        self.session.commit()
        self.tasks.append(new_task)

    def get_all_tasks(self):
        return self.session.query(Task).all()



    def delete_task(self, task_id):
        task = self.session.query(Task).filter_by(id=task_id).first()
        if task:
            self.session.delete(task)
            self.session.commit()
            self.tasks.remove(task)

    def __del__(self):
        self.session.close()


@click.group()
def cli():
    """Task Management CLI"""
    pass 

@click.command()
@click.option('--title', prompt='Task title')
@click.option('--description', prompt='Task description')
@click.option('--status', prompt='Task status')
@click.option('--due_date', prompt='Task due date')
def add_task(title, description, status, due_date):
    task_manager = TaskManager()
    task_manager.add_task(title, description, status, datetime.strptime(due_date, '%Y-%m-%d'))
    click.echo('Task added successfully.')

@click.command()
def get_all_tasks():
    task_manager =TaskManager()
    tasks = task_manager.get_all_tasks()
    for task in tasks:
        click.echo(task.title)

@click.command()
@click.option('--task_id', prompt='Task ID')
def delete_task(task_id):
    task_manager = TaskManager()
    task_manager.delete_task(int(task_id))
    click.echo('Task deleted successfully.')

cli.add_command(add_task)
cli.add_command(get_all_tasks)
cli.add_command(delete_task)


if __name__ == '__main__':
    cli()