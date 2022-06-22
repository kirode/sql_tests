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
