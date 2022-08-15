# Write your code here
from datetime import datetime, timedelta
from sys import exit

from colorama import init, Fore, Style
from pyfiglet import figlet_format
from sqlalchemy.ext.declarative import declarative_base   # used to give orm features to classes
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String, Date
from sqlalchemy import create_engine


Base = declarative_base()       # function return a DeclarativeMeta class which all model class should inherit
init(autoreset=True)

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
        self.engine = create_engine('sqlite:///data/todo.db?check_same_thread=False')
        Base.metadata.create_all(self.engine)   # create the table in the database
        Session = sessionmaker(bind=self.engine)
        self.session = Session()                # to access the database in orm
        self.today = datetime.today().date()

    def all_tasks(self):
        rows = self.session.query(Table).order_by(Table.deadline).all()
        print(Style.BRIGHT + Fore.BLACK + '> All Tasks')
        if rows:
            for index, row in enumerate(rows, start=1):
                print(f'{Fore.RED + str(index)}. {Fore.WHITE + row.task}. - {Fore.YELLOW + row.deadline.strftime("%d %b %Y")}')
        else:
            print('Nothing to do 🙂!')
        print()

    def today_tasks(self):
        rows = self.session.query(Table).filter(Table.deadline == self.today).all()
        print(Style.BRIGHT + Fore.BLACK + self.today.strftime('> Today - %d %b %Y'))
        if rows:
            for index, row in enumerate(rows, start=1):
                print(f'{index}. {row.task}')
        else:
            print('Nothing to Do 🙂!')
        print()

    def weeks_tasks(self):
        print(Style.BRIGHT + Fore.BLACK + "> Week's Tasks Details")
        for i in range(7):
            day_date = self.today + timedelta(days=i)
            rows = self.session.query(Table).filter(Table.deadline == day_date).all()
            print(Fore.LIGHTYELLOW_EX + day_date.strftime('%A %d %b'))
            if rows:
                for index, row in enumerate(rows, start=1):
                    print(f'{Fore.RED + str(index)}. {Fore.WHITE + row.task}')
            else:
                print('Nothing to Do 🙂!')
            print()

    def missed_tasks(self):
        rows = self.session.query(Table).filter(Table.deadline < self.today).order_by(Table.deadline).all()
        print(Style.BRIGHT + Fore.BLACK + '> Missed Tasks')
        if rows:
            for index, row in enumerate(rows, start=1):
                print(f'{Fore.RED + str(index)}. {Fore.WHITE + row.task}. - {Fore.YELLOW + row.deadline.strftime("%d %b %Y")}')
        else:
            print('Nothing to Do 🙂!')
        print()

    def add_task(self):
        try:
            print(Style.BRIGHT + Fore.BLACK + '> Enter Task Details')

            task_todo = input('Task Description: ')
            task_deadline = input('Task Deadline[yyyy-mm-dd]: ')

            deadline = datetime.strptime(task_deadline, '%Y-%m-%d').date()
        except ValueError:
            print(Fore.RED + 'Invalid or No deadline was set!')
            print()
        else:
            new_row = Table(task=task_todo, deadline=deadline)
            self.session.add(new_row)
            self.session.commit()
            print(Fore.GREEN + 'Task has been added!')
            print()

    def delete_task(self):
        rows = self.session.query(Table).order_by(Table.deadline).all()
        print(Style.BRIGHT + Fore.BLACK + '> Choose the number of the task you want to delete:')
        if rows:
            for index, row in enumerate(rows, start=1):
                print(f'{Fore.RED + str(index)}. {Fore.WHITE + row.task}. - {Fore.YELLOW + row.deadline.strftime("%d %b %Y")}')

            print()
            del_index = int(input('Task: ')) - 1
            self.session.delete(rows[del_index])
            self.session.commit()
            print(Fore.GREEN + 'The task has been deleted!')
        else:
            print('Nothing to Delete 🙂!')
        print()

    def interface(self):
        """Provide interface for user to view, add tasks"""

        TITLE = figlet_format('TODO TASKS', 'slant')
        while True:
            print(Style.BRIGHT + Fore.LIGHTBLUE_EX + TITLE)
            print("1] Today's tasks")
            print("2] Week's tasks")
            print("3] All tasks")
            print("4] Missed tasks")
            print("5] Add task")
            print("6] Delete task")
            print("0] Exit\n")

            try:
                user_input = int(input('Action: '))
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
                    print('Bye👋!')
                    break


my_list = TodoList()
my_list.interface()










