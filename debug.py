#!/usr/bin/env python3

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import ipdb;


if __name__ == '__main__':
    
   engine = create_engine('sqlite:///tasks.db')
   Session = sessionmaker(bind=engine)
   session = Session()

   from models import User, Task, Comment 


   User1 = User("Kate", "Kiruku")
   User2= User("Lillian", "Wambui")

   Task1 = Task("Send out emails")
   Task2 = Task("Dispatch medical cards")