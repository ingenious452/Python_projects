# Write your code here
from sqlalchemy.ext.declarative import declarative_base   # used to give orm features to classes
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String, Date
from sqlalchemy import create_engine
from datetime import datetime, timedelta
from sys import exit

Base = declarative_base()       # function return a DeclarativeMeta class which all model class should inherit


class Table(Base):
    __tablename__ = 'task'
    id = Column(Integer, primary_key=True)
    task = Column(String)
    deadline = Column(Date, default=datetime.today())

    def __repr__(self):
        return f'{self.id}: Integer, {self.task}: String, {self.deadline}: Date'


class TodoList:
    def __init__(self):
        # connect to the database
        self.engine = create_engine('sqlite:///todo.db?check_same_thread=False')
        Base.metadata.create_all(self.engine)   # create the table in the database
        Session = sessionmaker(bind=self.engine)
        self.session = Session()                # to access the database in orm
        self.today = datetime.today().date()

    def all_tasks(self):
        rows = self.session.query(Table).order_by(Table.deadline).all()
        print('All tasks:')
        if rows:
            for index, row in enumerate(rows, start=1):
                print(f'{index}. {row.task}. {row.deadline.day} {row.deadline.strftime("%b")}')
        else:
            print('Nothing to do!')
        print()

    def today_tasks(self):
        rows = self.session.query(Table).filter(Table.deadline == self.today).all()
        print(self.today.strftime('Today %d %b:'))
        if rows:
            for index, row in enumerate(rows, start=1):
                print(f'{index}. {row.task}')
        else:
            print('Nothing to do!')
        print()

    def weeks_tasks(self):
        for i in range(7):
            day_date = self.today + timedelta(days=i)
            rows = self.session.query(Table).filter(Table.deadline == day_date).all()
            print(day_date.strftime('%A %d %b:'))
            if rows:
                for index, row in enumerate(rows, start=1):
                    print(f'{index}. {row.task}')
            else:
                print('Nothing to do!')
            print()

    def missed_tasks(self):
        rows = self.session.query(Table).filter(Table.deadline < self.today).order_by(Table.deadline).all()
        print('Missed tasks:')
        if rows:
            for index, row in enumerate(rows, start=1):
                print(f'{index}. {row.task}. {row.deadline.day} {row.deadline.strftime("%b")}')
        else:
            print('Nothing to do!')
        print()

    def add_task(self):
        print('Enter task')
        task_todo = input()
        print('Enter deadline(%Y-%m-%d)')
        try:
            deadline = datetime.strptime(input(), '%Y-%m-%d').date()
        except ValueError as e:
            print(e)
            print('No deadline was set!')
        else:
            new_row = Table(task=task_todo, deadline=deadline)

        self.session.add(new_row)
        self.session.commit()
        print('The task has been added!\n')

    def delete_task(self):
        rows = self.session.query(Table).order_by(Table.deadline).all()
        print('Choose the number of the task you want to delete:')
        if rows:
            for index, row in enumerate(rows, start=1):
                print(f'{index}. {row.task}. {row.deadline.day} {row.deadline.strftime("%b")}')

            del_index = int(input()) - 1
            self.session.delete(rows[del_index])
            self.session.commit()
            print('The task has been deleted!')
        else:
            print('Nothing to delete')
        print()

    def interface(self):
        """Provide interface for user to view, add tasks"""
        while True:
            print("1) Today's tasks")
            print("2) Week's tasks")
            print("3) All tasks")
            print("4) Missed tasks")
            print("5) Add task")
            print("6) Delete task")
            print("0) Exit\n")

            try:
                user_input = int(input())
                print()
            except ValueError as ve:
                print(ve)
                exit()
            else:
                actions = {1: self.today_tasks,
                           2: self.weeks_tasks,
                           3: self.all_tasks,
                           4: self.missed_tasks,
                           5: self.add_task,
                           6: self.delete_task,
                           0: None}
                action = actions.get(user_input)      # assuming people will enter the choices given to them.
                if action is not None:
                    action()
                else:
                    print('Bye!')
                    break


my_list = TodoList()
my_list.interface()










