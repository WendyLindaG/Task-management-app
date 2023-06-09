from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
import random 
import sys
import re

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String)
    project_id = Column(Integer, ForeignKey('projects.id'))
    project = relationship("Project")



class Task(Base):
    __tablename__ = 'tasks'
    id = Column(Integer, primary_key=True)
    title = Column(String)
    description = Column(String)
    status = Column(String)
    due_date = Column(DateTime)
    project_id = Column(Integer, ForeignKey('projects.id'))


class Project(Base):
    __tablename__ = 'projects'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)
    tasks = relationship("Task")


class Comment(Base):
    __tablename__ = 'comments'
    id = Column(Integer, primary_key=True)
    content = Column(String)
    created_at = Column(DateTime)
    task_id = Column(Integer, ForeignKey('tasks.id'))
    task = relationship("Task", backref="comments")


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

    def update_task(self, task_id, title, description, status, due_date):
        task = self.session.query(Task).filter_by(id=task_id).first()
        if task:
            task.title = title
            task.description = description
            task.status = status
            task.due_date = due_date
            self.session.commit()

    def delete_task(self, task_id):
        task = self.session.query(Task).filter_by(id=task_id).first()
        if task:
            self.session.delete(task)
            self.session.commit()
            self.tasks.remove(task)

    def __del__(self):
        self.session.close()


class ProjectManager:
    def __init__(self):
        engine = create_engine('sqlite:///tasks.db')
        Base.metadata.create_all(engine)
        Session = sessionmaker(bind=engine)
        self.session = Session()

    def add_project(self, name, description):
        new_project = Project(name=name, description=description)
        self.session.add(new_project)
        self.session.commit()

    def get_all_projects(self):
        return self.session.query(Project).all()

    def update_project(self, project_id, name, description):
        project = self.session.query(Project).filter_by(id=project_id).first()
        if project:
            project.name = name
            project.description = description
            self.session.commit()

    def delete_project(self, project_id):
        project = self.session.query(Project).filter_by(id=project_id).first()
        if project:
            self.session.delete(project)
            self.session.commit()

    def __del__(self):
        self.session.close()


# Example usage
if __name__ == '__main__':
    task_manager = TaskManager()
    project_manager = ProjectManager()
    
    task_manager.add_task("Finish project", "Complete the remaining tasks", "In Progress", datetime.now())
    task_manager.add_task("Meeting with team", "Discuss project updates", "Pending", datetime.now())

    tasks = task_manager.get_all_tasks()
    for task in tasks:
        print(task.title)

    task_manager.update_task(1, "New title", "Updated description", "Completed", datetime.now())
    task_manager.delete_task(2)

    project_manager.add_project("Project A", "Description of Project A")
    project_manager.add_project("Project B", "Description of Project B")

    projects = project_manager.get_all_projects()
    for project in projects:
        print(project.name)


       # Create engine and session
engine = create_engine('sqlite:///tasks.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session() 

