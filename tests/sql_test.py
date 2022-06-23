from src.query_page import QueryPage
from pytest_check import is_true
from helpers import update_query, insert_query


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
    columns, values = insert_query(customer)
    query = f'INSERT INTO Customers {columns} values {values};'
    page = QueryPage(driver).open()
    page.set_sql_statement(query)
    page.run_sql()
    is_true(page.get_operation_result_text(result))

    page.set_sql_statement(f'SELECT * FROM Customers WHERE CustomerName=\'{customer["CustomerName"]}\'')
    page.run_sql()
    created_customer = page.find_row_by_value(customer['CustomerName'])
    result_customer = page.row_to_dict(created_customer)
    del result_customer['CustomerID']
    is_true(result_customer == customer)


def test_update_customer(driver):
    customer = {'CustomerName': 'Alexander Petrov',
                'ContactName': 'Maria Pokrovskaya',
                'Address': '23 Tverskaya-Yamskaya',
                'City': 'Moscow',
                'PostalCode': '117418',
                'Country': 'RF'}
    result = 'You have made changes to the database. Rows affected: 1'
    page = QueryPage(driver).open()
    page.set_sql_statement(f'UPDATE Customers SET {update_query(customer)}WHERE CustomerID=\'1\'')
    page.run_sql()
    is_true(page.get_operation_result_text(result))

    page.set_sql_statement('SELECT * FROM Customers WHERE CustomerID=\'1\'')
    page.run_sql()
    updated_customer = page.row_to_dict(page.find_row_by_value('1'))
    del updated_customer['CustomerID']
    is_true(updated_customer == customer)


def test_delete_customer(driver):
    delete_result = 'You have made changes to the database. Rows affected: 1'
    select_result = 'No result.'
    page = QueryPage(driver).open()
    page.set_sql_statement('DELETE FROM Customers WHERE CustomerID=\'1\'')
    page.run_sql()
    is_true(page.get_operation_result_text(delete_result))

    page.set_sql_statement('SELECT * FROM Customers WHERE CustomerID=\'1\'')
    page.run_sql()
    is_true(page.get_operation_result_text(select_result))

