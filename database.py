from __future__ import print_function, unicode_literals
from PyInquirer import prompt
import mysql.connector as msql
from examples import custom_style_3


def init_db():
    db_conn_params = [
        {
            'type': 'input',
            'qmark': '[*]',
            'name': 'user',
            'message': 'Enter username',
        },
        {
            'type': 'password',
            'qmark': '[*]',
            'name': 'password',
            'message': 'Enter password',
        },
        {
            'type': 'list',
            'qmark': '[*]',
            'name': 'host',
            'message': 'Where\'s your database hosted',
            'choices': [
                'localhost',
                'custom'
            ]
        }
    ]
    db_host = [
        {
            'type': 'input',
            'qmark': '[?]',
            'name': 'host',
            'message': 'Enter the IP Address'
        }
    ]
    answers = prompt(db_conn_params, style=custom_style_3)
    if answers['host'] == 'custom':
        answers['host'] = prompt(db_host, style=custom_style_3)['host']

    mydb = msql.connect(**answers)
    mycursor = mydb.cursor()

    mycursor.execute("SHOW DATABASES")
    databases = [x[0] for x in mycursor.fetchall()]

    db_conn_params = [
        {
            'type': 'list',
            'qmark': '[?]',
            'name': 'database',
            'message': 'What database do you wish to connect to',
            'choices': databases
        },
    ]

    database = prompt(db_conn_params, style=custom_style_3)['database']
    mydb = msql.connect(
        host=answers['host'],
        user=answers['user'],
        password=answers['password'],
        database=database
    )
    return mydb
