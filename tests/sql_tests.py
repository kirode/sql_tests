import time

from src.query_page import QueryPage
from selenium.webdriver.common.by import By


def test_customer_address(driver):
    page = QueryPage(driver).open()
    page.set_sql_statement('SELECT * FROM Customers;')
    page.run_sql()
    row = page.find_row_by_value('Giovanni Rovelli')
    record = page.row_to_dict(row)
    assert record["Address"] == 'Via Ludovico il Moro 22'


def test_customer_count(driver):
    page = QueryPage(driver).open()
    page.set_sql_statement('SELECT * FROM Customers WHERE city=\'London\'')
    page.run_sql()
    rows = page.get_table_data()
    assert len(rows) == 6


def test_create_customer(driver):
    customer = {'CustomerName': 'Alexander Petrov',
                'ContactName': 'Maria Pokrovskaya',
                'Address': '23 Tverskaya-Yamskaya',
                'City': 'Moscow',
                'PostalCode': '117418',
                'Country': 'RF'}
    result = 'You have made changes to the database. Rows affected: 1'
    columns = []
    values = []
    for key, value in customer.items():
        columns.append(key)
        values.append(value)
    query = f'INSERT INTO Customers {tuple(columns)} values {tuple(values)};'
    page = QueryPage(driver).open()
    page.set_sql_statement(query)
    page.run_sql()
    assert page.get_operation_result_text(result)

    page.set_sql_statement(f'SELECT * FROM Customers WHERE CustomerName=\'{customer["CustomerName"]}\'')
    page.run_sql()
    created_customer = page.find_row_by_value(customer['CustomerName'])
    result_customer = page.row_to_dict(created_customer)
    del result_customer['CustomerID']
    assert result_customer == customer


def test_update_customer(driver):
    customer = {'CustomerName': 'Alexander Petrov',
                'ContactName': 'Maria Pokrovskaya',
                'Address': '23 Tverskaya-Yamskaya',
                'City': 'Moscow',
                'PostalCode': '117418',
                'Country': 'RF'}
    result = 'You have made changes to the database. Rows affected: 1'
    page = QueryPage(driver).open()
    values = ''
    for key, value in customer.items():
        values += f'{key}=\'{value}\', '
    index = values.rfind(',')
    values = values[:index] + ' '
    page.set_sql_statement(f'UPDATE Customers SET {values}WHERE CustomerID=\'1\'')
    page.run_sql()
    assert page.get_operation_result_text(result)

    page.set_sql_statement('SELECT * FROM Customers WHERE CustomerID=\'1\'')
    page.run_sql()
    updated_customer = page.row_to_dict(page.find_row_by_value('1'))
    del updated_customer['CustomerID']
    assert updated_customer == customer



