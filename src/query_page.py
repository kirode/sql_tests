from selenium.webdriver.common.by import By
from src.widget import Widget


class QueryPage(Widget):
    _url = Widget._url + '/sql/trysql.asp?filename=trysql_select_all'
    _run_sql_button = (By.CLASS_NAME, 'ws-btn')
    _code_field = (By.CLASS_NAME, 'CodeMirror-lines')
    _table_header = (By.CSS_SELECTOR, '#divResultSQL div div')
    _operation_result_header = (By.CSS_SELECTOR, '#divResultSQL div')
    _table_content = (By.CSS_SELECTOR, '#divResultSQL div table tbody')

    def open(self):
        self.driver.get(self._url)
        return self

    def run_sql(self):
        self._get_element(self._run_sql_button).click()

    def set_sql_statement(self, query):
        self._get_element(QueryPage._code_field)
        self.driver.execute_script(f'window.editor.doc.setValue("{query}")')

    def get_header_text(self, text):
        return self._get_element_with_text(self._table_header, text)

    def get_operation_result_text(self, text):
        return self._get_element_with_text(self._operation_result_header, text)

    def get_table_content(self):
        table = self._get_element(self._table_content)
        return [row for row in table.find_elements(By.CSS_SELECTOR, 'tr')]

    def get_table_headers(self):
        return [elem.text for elem in self.get_table_content()[0].find_elements(By.CSS_SELECTOR, 'th')]

    def get_table_rows(self):
        return self.get_table_content()[1:]

    def get_table_data(self):
        table_data = []
        for row in self.get_table_rows():
            table_data.append([elem.text for elem in row.find_elements(By.CSS_SELECTOR, 'td')])
        return table_data

    def find_row_by_value(self, value):
        return self._get_element(self._table_content).find_element(By.XPATH, f'.//td[text()="{value}"]//parent::tr')

    def row_to_dict(self, row):
        headers = self.get_table_headers()
        row_values = [cell.text for cell in row.find_elements(By.CSS_SELECTOR, 'td')]
        return dict(zip(headers, row_values))

