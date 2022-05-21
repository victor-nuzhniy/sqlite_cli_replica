import csv
from collections import OrderedDict
import copy


class MySqliteRequest:

    def __init__(self, table_name=None):
        self.type_of_request = ''
        self.select_columns = []
        self.where_select = [['~~', None]]
        self.where_join = ['~~~', None]
        self.table_name = table_name
        self.set_params = None
        self.values_param = None
        self.order_params = []
        self.column_a_b = []
        self.result = []
        self.error = None

    def from_(self, table_name):
        self.table_name = table_name
        return self

    def select(self, columns):
        if type(columns) is list:
            for elements in columns:
                self.select_columns.append(str(elements))
        else:
            self.select_columns.append(str(columns))
        self.request_type('select')
        return self

    def where(self, column_name, criteria):
        if len(self.column_a_b):
            self.where_join = [column_name, criteria]
        else:
            self.where_select.append([column_name, criteria])
        return self

    def join_(self, column_on_db_a, filename_db_b, column_on_db_b):
        self.values_param = filename_db_b
        self.column_a_b.append(column_on_db_a)
        self.column_a_b.append(column_on_db_b)
        return self

    def order(self, order, column_name):
        self.order_params.append(order)
        self.order_params.append(column_name)
        return self

    def insert(self, table_name):
        self.request_type('insert')
        self.table_name = table_name
        return self

    def values(self, data):
        if type(data) is not list:
            self.values_param = [data]
        else:
            self.values_param = data
        return self

    def update(self, table_name):
        self.request_type('update')
        self.table_name = table_name
        return self

    def set_(self, data):
        self.set_params = data
        return self

    def delete(self):
        self.request_type('delete')
        return self

    def run_select(self):
        self.run_select_where()
        if len(self.column_a_b):
            self.run_select_join()
        result = []
        for rows in self.result:
            if len(self.select_columns):
                if self.select_columns[0] == '*':
                    result.append(dict(rows))
                else:
                    result.append({elem: rows.get(elem) for elem in self.select_columns if rows.get(elem)})
            else:
                if __name__ == "__main__":
                    raise Exception('Invalid input: select column pointer absent')
        self.result = copy.deepcopy(result)
        if len(self.order_params):
            self.run_select_order()
        if __name__ == "__main__":
            print(self.result)

    def run_select_where(self):
        f = open(self.table_name, 'r')
        table = csv.DictReader(f)
        for rows in table:
            flag = 0
            for where in self.where_select:
                if rows.get(where[0]) == where[1]:
                    flag = 1
                else:
                    flag = 0
                    break
            if flag == 1:
                self.result.append(rows)
        f.close()

    def run_select_join(self):
        f = open(self.values_param, 'r')
        table = csv.DictReader(f)
        result_b = []
        result = []
        for rows in table:
            result_b.append(rows)
        f.close()
        for rows_a in self.result:
            for rows_b in result_b:
                if rows_a[self.column_a_b[0]] == rows_b[self.column_a_b[1]]:
                    if rows_b.get(self.where_join[0]) == self.where_join[1]:
                        rows_a.update(rows_b)
                        result.append(rows_a)
        self.result = copy.deepcopy(result)

    def run_select_order(self):
        if self.order_params[0] == 'ASC':
            self.result.sort(key=lambda x: x[self.order_params[1]])
        elif self.order_params[0] == 'DESC':
            self.result.sort(key=lambda x: x[self.order_params[1]], reverse=True)
        else:
            if __name__ == "__main__":
                raise Exception('Invalid input order')

    def run_insert(self):
        if type(self.values_param[0]) is dict:
            f = open(self.table_name, 'r')
            table = csv.reader(f)
            headers = next(table)
            f.close()
        f = open(self.table_name, 'a')
        table = csv.writer(f)
        if type(self.values_param[0]) is dict:
            for elem in self.values_param:
                result_list = []
                for item in headers:
                    result_list.append(str(elem[item]))
                table.writerow(result_list)
        else:
            table.writerow(self.values_param)
        f.close()

    def run_update(self):
        f = open(self.table_name, 'r')
        table = csv.DictReader(f)
        result = []
        for rows in table:
            flag = 0
            for where in self.where_select:
                if rows.get(where[0]) == where[1]:
                    flag = 1
                else:
                    flag = 0
                    break
            if flag == 1:
                rows.update(self.set_params)
            result.append(rows)
        f.close()
        f = open(self.table_name, 'w')
        table = csv.DictWriter(f, fieldnames=list(result[0].keys()))
        table.writeheader()
        table.writerows(result)
        f.close()

    def run_delete(self):
        f = open(self.table_name, 'r')
        table = csv.DictReader(f)
        result = []
        for rows in table:
            flag = 0
            for where in self.where_select:
                if not where[1] or rows.get(where[0]) != where[1]:
                    flag = 1
                else:
                    flag = 0
                    break
            if flag == 1:
                result.append(rows)
        f.close()
        f = open(self.table_name, 'w')
        table = csv.DictWriter(f, fieldnames=list(result[0].keys()))
        table.writeheader()
        table.writerows(result)
        f.close()

    def run(self):
        if self.type_of_request == 'select':
            self.run_select()
            return self.result
        elif self.type_of_request == 'insert':
            self.run_insert()
        elif self.type_of_request == 'update':
            self.run_update()
        elif self.type_of_request == 'delete':
            self.run_delete()
        else:
            if __name__ == "__main__":
                raise Exception('Invalid request')

    def request_type(self, new_type):
        if self.type_of_request == '' or self.type_of_request == new_type:
            self.type_of_request = new_type
        else:
            self.error = ('Invalid: type of request already set to '
                + self.type_of_request + '(new type is ' + new_type + ')')
            if __name__ == "__main__":
                raise Exception(self.error)


request = MySqliteRequest()
request = request.delete()
request = request.from_('nba_player_data.csv')
request = request.where('name', 'Ivan')
request.run()