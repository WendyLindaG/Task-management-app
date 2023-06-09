#!/usr/bin/env python3

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import ipdb;


if __name__ == '__main__':
    
   engine = create_engine('sqlite:///tasks.db')
   Session = sessionmaker(bind=engine)
   session = Session()

   from models import User, Task, Comment 


   User1 = User(username="Kiruku", email="kiruku@gmail.com")
   User2= User(username="Wambui", email="lillian@gmail.com")

   Task1 = Task(title="Communication", description="Send out emails", status="Pending", due_date="Tomorrow")
   Task2 = Task(title="Dispatch", description="Dispatch medical cards", status="In progress", due_date="Tomorrow")


   ipdb.set_trace()