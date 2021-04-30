from __future__ import print_function, unicode_literals
from PyInquirer import prompt
from pprint import pprint
from examples import custom_style_3
from terminaltables import AsciiTable


def select(cursor, where: bool = False) -> str:
    cursor.execute("SHOW TABLES")
    tables = [x[0] for x in cursor.fetchall()]

    q_table = [
        {
            'type': 'list',
            'qmark': '[?]',
            'name': 'table',
            'message': 'Select from which table',
            'choices': tables
        }
    ]
    table = prompt(q_table, style=custom_style_3)['table']

    cursor.execute(f"DESCRIBE {table}")
    fields = [{'name': x[0]}
              for x in cursor.fetchall()]

    q_fields = [
        {
            'type': 'checkbox',
            'qmark': '[?]',
            'name': 'fields',
            'message': 'Choose fields to select',
            'choices': fields,
            'validate': lambda answer: 'You must choose at least one column.' if len(answer) == 0 else True
        }
    ]
    colunms = ', '.join(prompt(q_fields, style=custom_style_3)['fields'])

    if not where:
        sql = f'SELECT {colunms} FROM {table}'
        cursor.execute(sql)
        result = [colunms.split(', ')]
        for x in cursor.fetchall():
            result.append(x)
        f_result = AsciiTable(result)
        print(f_result.table)
        return sql
    else:
        q_condition = [
            {
                'type': 'input',
                'qmark': '[?]',
                'name': 'condition',
                'message': 'Enter WHERE condition (MySQL query)'
            }
        ]
        condition = prompt(q_condition, style=custom_style_3)['condition']
        sql = f'SELECT {colunms} FROM {table} WHERE {condition}'
        cursor.execute(sql)
        result = [colunms.split(', ')]
        for x in cursor.fetchall():
            result.append(x)
        f_result = AsciiTable(result)
        print(f_result.table)
        return sql
