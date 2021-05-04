from PyInquirer import prompt
from pprint import pprint
from examples import custom_style_3
from terminaltables import AsciiTable
from random import (randint, choice)
import uuid
import names
import datetime
import pprint
import base64


input_type = [
    'none',
    'static custom',
    '<foreign key>',
    '<id>',
    '<choice array> (choose from an array of values)',
    '<choice binary> (0 or 1)',
    '<choice number range> (choose from a range of numbers)',
    '<name>',
    '<email>',
    '<static password> (same password for everyone)',
    '<phone>',
    '<address>',
    '<long text>',
    '<gender>',
    '<datetime>'
]


def insert(mydb):
    cursor = mydb.cursor()
    cursor.execute("SHOW TABLES")
    tables = [x[0] for x in cursor.fetchall()]

    q_table = [
        {
            'type': 'list',
            'qmark': '[?]',
            'name': 'table',
            'message': 'Insert to which table',
            'choices': tables
        }
    ]
    table = prompt(q_table, style=custom_style_3)['table']

    cursor.execute(f"DESCRIBE {table}")
    fields = cursor.fetchall()
    field_names = [{'name': x[0]} for x in fields]

    q_fields = [
        {
            'type': 'checkbox',
            'qmark': '[?]',
            'name': 'fields',
            'message': 'Choose fields to insert',
            'choices': field_names,
            'validate': lambda answer: 'You must choose at least one column.' if len(answer) == 0 else True
        },
        {
            'type': 'input',
            'qmark': '[?]',
            'name': 'num_of_recods',
            'message': 'Enter number of recods to add',
        }
    ]
    answerrrr = prompt(q_fields, style=custom_style_3)
    fields_choice = answerrrr['fields']
    colunms = ', '.join(fields_choice)
    fields_choice_desc = [x for x in fields if x[0] in fields_choice]

    field_type_mapper = {}

    for field in fields_choice_desc:
        field_value = ''
        # field_type_mapper[field[0]]

        q_input_type = [
            {
                'type': 'list',
                'qmark': '[----]',
                'name': 'input_type',
                'message': f'Choose input type for {field[0]}',
                'choices': input_type
            }
        ]

        input_type_choice = prompt(
            q_input_type, style=custom_style_3)['input_type']

        if input_type_choice == 'none':
            field_value = None

        elif input_type_choice == 'static custom':
            q_input = [
                {
                    'type': 'input',
                    'qmark': '[----]',
                    'name': 'value',
                    'message': 'Enter static value',
                }
            ]
            field_value = prompt(
                q_input, style=custom_style_3)['value']

        elif input_type_choice == '<foreign key>':
            q_table = [
                {
                    'type': 'list',
                    'qmark': '[----]',
                    'name': 'table',
                    'message': 'Foreign key to which table',
                    'choices': tables
                }
            ]
            table = prompt(q_table, style=custom_style_3)['table']

            cursor.execute(f"DESCRIBE {table}")
            fields = cursor.fetchall()
            field_names = [{'name': x[0]} for x in fields]

            q_fields = [
                {
                    'type': 'list',
                    'qmark': '[----]',
                    'name': 'field',
                    'message': 'Choose field to link to',
                    'choices': field_names,
                }
            ]
            field_choice = prompt(q_fields, style=custom_style_3)['field']

            cursor.execute(f"SELECT {field_choice} FROM {table}")
            foreign_choice = [x[0] for x in cursor.fetchall()]

            field_value = foreign_choice

        elif input_type_choice == '<id>' \
                or input_type_choice == '<name>' \
                or input_type_choice == '<email>' \
                or input_type_choice == '<phone>' \
                or input_type_choice == '<address>' \
                or input_type_choice == '<long text>' \
                or input_type_choice == '<datetime>':
            field_value = input_type_choice

        elif input_type_choice == '<choice array> (choose from an array of values)':
            q_input = [
                {
                    'type': 'input',
                    'qmark': '[----]',
                    'name': 'value',
                    'message': 'Enter array values. Seperate values by a comma (,)',
                }
            ]
            field_value = str(prompt(
                q_input, style=custom_style_3)['value']).replace(' ', '').split(',')

        elif input_type_choice == '<choice binary> (0 or 1)':
            field_value = [0, 1]

        elif input_type_choice == '<choice number range> (choose from a range of numbers)':
            q_input = [
                {
                    'type': 'input',
                    'qmark': '[----]',
                    'name': 'min',
                    'message': 'Enter min',
                },
                {
                    'type': 'input',
                    'qmark': '[----]',
                    'name': 'max',
                    'message': 'Enter max',
                }
            ]
            answer = prompt(q_input, style=custom_style_3)
            minn = int(answer['min'])
            maxx = int(answer['max'])

            field_value = [x for x in range(minn, maxx+1)]

        elif input_type_choice == '<static password> (same password for everyone)':
            q_input = [
                {
                    'type': 'password',
                    'qmark': '[----]',
                    'name': 'value',
                    'message': 'Enter static password',
                }
            ]
            field_value = prompt(
                q_input, style=custom_style_3)['value']

        elif input_type_choice == '<gender>':
            field_value = ['male', 'female']

        field_type_mapper[field[0]] = {
            'type': input_type_choice,
            'value': field_value
        }

    query = f"INSERT INTO `{table}` ({colunms}) VALUES ({('%s,'*len(fields_choice)).rstrip(',')})"
    values = []
    # cursor.executemany(query, values)
    # mydb.commit()

    name = names.get_full_name()

    type_function = {
        'none': None,
        'static custom': lambda static: static,
        '<foreign key>': lambda choices: choice(choices),
        '<id>': lambda typ: str(uuid.uuid4().fields[-1])[:5],
        '<choice array> (choose from an array of values)': lambda choices: choice(choices),
        '<choice binary> (0 or 1)': lambda choices: choice(choices),
        '<choice number range> (choose from a range of numbers)': lambda choices: choice(choices),
        '<name>': lambda typ: name,
        '<email>': lambda typ: name.replace(' ', '.').lower() + '@email.com',
        '<static password> (same password for everyone)': lambda static: base64.b64encode(static.encode('ascii')).decode('ascii'),
        '<phone>': lambda typ: '+' + str(randint(100, 999)) + '-' +
        str(randint(100, 999)) + '-' + str(randint(100, 999)) +
        '-' + str(randint(1000, 9999)),
        '<address>': lambda typ: str(randint(10, 99)) + ' ' +
        names.get_first_name() + ' Street, Lagos, Nigeria.',
        '<long text>': lambda typ: 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nam hendrerit nisi sed sollicitudin pellentesque. Nunc posuere purus rhoncus pulvinar aliquam. Ut aliquet tristique nisl vitae volutpat. Nulla aliquet porttitor venenatis. Donec a dui et dui fringilla consectetur id nec massa. Aliquam erat volutpat. Sed ut dui ut lacus dictum fermentum vel tincidunt neque. Sed sed lacinia lectus. Duis sit amet sodales felis. Duis nunc eros, mattis at dui ac, convallis semper risus. In adipiscing ultrices tellus, in suscipit massa vehicula eu.',
        '<gender>': lambda choices: choice(choices),
        '<datetime>': lambda typ: datetime.datetime.now()
    }

    for i in range(int(answerrrr['num_of_recods'])):
        field_value = []

        for field in fields_choice:
            field_value.append(type_function[field_type_mapper[field]['type']](
                field_type_mapper[field]['value']))
        name = names.get_full_name()
        values.append(tuple(field_value))

    cursor.executemany(query, values)
    mydb.commit()
