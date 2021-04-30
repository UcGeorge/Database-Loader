from __future__ import print_function, unicode_literals
from PyInquirer import prompt
from pprint import pprint
from examples import custom_style_3
from terminaltables import AsciiTable


def delete(mydb):
    cursor = mydb.cursor()

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
    q_field = [
        {
            'type': 'list',
            'qmark': '[?]',
            'name': 'field',
            'message': 'Select field to filter',
            'choices': fields
        }
    ]
    field = prompt(q_field, style=custom_style_3)['field']

    q_condition = [
        {
            'type': 'input',
            'qmark': '[?]',
            'name': 'condition',
            'message': f'Enter {field} value to filter'
        }
    ]
    filterr = prompt(q_condition, style=custom_style_3)['condition']

    sql = f"DELETE FROM {table} WHERE {field} = '{filterr}'"

    q_confirm = [
        {
            'type': 'confirm',
            'name': 'proceed',
            'message': f'QUERY: {sql}\nAre you sure you want to proceed?',
        },
    ]
    proceed = prompt(q_confirm, style=custom_style_3)['proceed']

    if proceed:
        cursor.execute(sql)
        mydb.commit()
        print(cursor.rowcount, "record(s) deleted")
        return sql
    else:
        return
