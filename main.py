from __future__ import print_function, unicode_literals
from q_delete import delete
from q_insert import insert
from q_select import select
from database import init_db
from pyfiglet import Figlet
from PyInquirer import prompt, Separator
from pprint import pprint
import names
from random import (randint, choice)
import datetime
import base64
import mysql.connector as msql
import os


log = ''


commands = [
    {
        'type': 'list',
        'name': 'command',
        'message': 'Pick an operation',
        'choices': [
            'SELECT',
            'SELECT WHERE',
            'INSERT',
            'DELETE',
            'Show Log'
        ]
    }
]


if __name__ == '__main__':
    os.system('cls')
    f = Figlet(font='roman')
    print(f.renderText('myDB\n'))

    mydb = init_db()

    run_command = {
        'SELECT': lambda cursor: select(cursor),
        'SELECT WHERE': lambda cursor: select(cursor, where=True),
        'INSERT': lambda cursor: insert(cursor),
        'DELETE': lambda cursor: delete(cursor),
        'Show Log': lambda cursor: print(log)
    }

    while True:
        mycursor = mydb.cursor()
        os.system('cls')
        command = prompt(commands)['command']

        output = run_command[command](mycursor)
        log += f'\n>> {output}'
        input('Press (enter) to continue...')
