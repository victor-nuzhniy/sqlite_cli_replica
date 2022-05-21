import re
import os.path
import my_sqlite_request as rqt


class Interpreter:

    def __init__(self):
        self.command_dict = {'FROM': self.from_args,
                             'SELECT': self.select_args,
                             'WHERE': self.where_args,
                             'JOIN': self.join_args,
                             'ORDER': self.order_args,
                             'INSERT': self.insert_args,
                             'VALUES': self.values_args,
                             'UPDATE': self.update_args,
                             'SET': self.set_args,
                             'DELETE': self.delete_args,
                             ';': self.run_args}
        self.args = []
        self.request = rqt.MySqliteRequest()
        self.result = None

    def from_args(self):
        if os.path.exists(self.args[0]):
            self.request.from_(self.args[0])
        else:
            self.request.error = 'File does not exist'

    def select_args(self):
            self.request.select(self.args)

    def where_args(self):
        if self.args[1] == '=' and len(self.args) % 3 == 0:
            self.request.where(self.args[0], self.args[2])
        else:
            self.request.error = 'Invalid WHERE input'

    def join_args(self):
        if os.path.exists(self.args[0]) and self.args[1] == 'ON' and self.args[3] == '=':
            self.request.join_(self.args[2], self.args[0], self.args[4])
        else:
            self.request.error = 'Invalid JOIN input'

    def order_args(self):
        if self.args[0] == 'BY' and self.args[2] in {'DESC', 'ASC'}:
            self.request.order(self.args[2], self.args[1])
        else:
            self.request.error = 'Invalid ORDER input'

    def insert_args(self):
        if os.path.exists(self.args[1]):
            self.request.insert(self.args[1])
        else:
            self.request.error = 'Invalid INSERT table name'

    def values_args(self):
        args_list = re.findall(r'[^ ,\'\"]+|[\'\"][^\'\"]+[\'\"]', self.args[0][1:-1])
        self.args = []
        for elems in args_list:
            x = re.search(r'[^\'\"]+', elems)
            self.args.append(x[0])
        self.request.values(self.args)

    def update_args(self):
        if os.path.exists(self.args[0]):
            self.request.update(self.args[0])
        else:
            self.request.error = 'Invalid UPDATE table name'

    def set_args(self):
        self.dict_parsing()
        if self.args:
            self.request.set_(self.args)
        else:
            self.request.error = 'Invalid SET input'

    def delete_args(self):
        self.request.delete()

    def run_args(self):
        self.result = self.request.run()
        if self.result:
            self.output()

    def dict_parsing(self):
        args_dict = {}
        i = 0
        while i < len(self.args):
            if self.args[i] == '=':
                args_dict[elem] = self.args[i + 1]
                i += 2
            else:
                elem = self.args[i]
                i += 1
        self.args = args_dict

    def output(self):
        for lines in self.result:
            s = ''
            for item in iter(lines.values()):
                s = s + '|' + item
            print(s[1:])


if __name__ == "__main__":
    print('MySQLite version 0.1 2022-03-29')
    while True:
        words = input("my_sqlite_cli>")
        if words == 'quit':
            break
        else:
            inter = Interpreter()
            commands = re.findall(r'[^\s()\',;]+|[(][^()]*[)]|;|\'[^\']+\'', words)
            i, memory = 0, None
            try:
                commands[-1] != ';'
            except:
                print("';' is missing in the end of the request")
                i = len(commands)
            if len(commands) < 4 and commands[0] not in {'SELECT', 'INSERT', 'DELETE', 'UPDATE'}:
                i = len(commands)
                print('Invalid command')
            while i < len(commands):
                if inter.command_dict.get(commands[i]):
                    if inter.args and memory:
                        inter.command_dict[memory]()
                        if inter.request.error:
                            print(inter.request.error)
                            break
                        inter.args, memory = [], None
                    elif not inter.args and memory:
                        print('Invalid ', memory, ' params input')
                        break
                    if commands[i] in {'DELETE', ';'}:
                        inter.command_dict[commands[i]]()
                    else:
                        memory = commands[i]
                    i += 1
                else:
                    x = re.search(r'[\(].+[\)]|[^\'\"]+', commands[i])
                    inter.args.append(x[0])
                    i += 1