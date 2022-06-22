import time

from src.query_page import QueryPage
from selenium.webdriver.common.by import By


def test_single_record(driver):
    page = QueryPage(driver).open()
    page.set_sql_statement('SELECT * FROM Customers;')
    page.run_sql()
    header = page.get_header_text()
    time.sleep(1)
    table = page.get_table_rows()

    assert header == 'Number of Records: 91'

    assert len(table) == 91

    row = page.find_row_by_value('Hanna Moos')
    record = page.row_to_dict(row)
    assert record["PostalCode"] == '68306'

