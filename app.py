import click
from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

Base = declarative_base()


class Task(Base):
    __tablename__ = 'tasks'
    id = Column(Integer, primary_key=True)
    title = Column(String)
    description = Column(String)
    status = Column(String)
    due_date = Column(DateTime)


class Project(Base):
    __tablename__ = 'projects'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)
    tasks = relationship("Task")


@click.group()
def cli():
    """Task Management CLI"""


@cli.command()
@click.argument('title')
@click.argument('description')
@click.argument('status')
def add_task(title, description, status):
    """Add a new task"""
    engine = create_engine('sqlite:///tasks.db')
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()

    new_task = Task(title=title, description=description, status=status, due_date=datetime.now())
    session.add(new_task)
    session.commit()

    click.echo('Task added successfully.')

    session.close()


@cli.command()
def list_tasks():
    """List all tasks"""
    engine = create_engine('sqlite:///tasks.db')
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()

    tasks = session.query(Task).all()
    for task in tasks:
        click.echo(f'Task ID: {task.id}, Title: {task.title}, Description: {task.description}, Status: {task.status}, Due Date: {task.due_date}')

    session.close()


@cli.command()
@click.argument('task_id')
@click.argument('title')
@click.argument('description')
@click.argument('status')
def update_task(task_id, title, description, status):
    """Update a task"""
    engine = create_engine('sqlite:///tasks.db')
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()

    task = session.query(Task).filter_by(id=task_id).first()
    if task:
        task.title = title
        task.description = description
        task.status = status
        session.commit()
        click.echo('Task updated successfully.')
    else:
        click.echo(f'Task with ID {task_id} not found.')

    session.close()


@cli.command()
@click.argument('task_id')
def delete_task(task_id):
    """Delete a task"""
    engine = create_engine('sqlite:///tasks.db')
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()

    task = session.query(Task).filter_by(id=task_id).first()
    if task:
        session.delete(task)
        session.commit()
        click.echo('Task deleted successfully.')
    else:
        click.echo(f'Task with ID {task_id} not found.')

    session.close()


if __name__ == '__main__':
    cli()
