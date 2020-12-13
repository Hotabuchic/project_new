import sqlite3


class DataBase:
    def __init__(self, name_database="project.db"):
        self.name_database = name_database

    def get_data(self, name_tables, name_data="*", criterion="", data_criterion=None):
        self.refresh()
        if data_criterion is not None and criterion != "":
            return self.cur.execute(f"SELECT {name_data} FROM {name_tables} WHERE {criterion}",
                                    data_criterion).fetchall()
        elif criterion != "":
            return self.cur.execute(f"SELECT {name_data} FROM {name_tables} WHERE {criterion}").fetchall()
        return self.cur.execute(f"SELECT {name_data} FROM {name_tables}").fetchall()

    def add_data(self, name_tables, data_criterion=None):
        self.refresh()
        if data_criterion is not None:
            question_mark = ", ".join(["?" for _ in range(len(data_criterion))])
            self.cur.execute(f"INSERT INTO {name_tables} VALUES({question_mark})", data_criterion)
            self.con.commit()
            self.con.close()

    def refresh(self):
        self.con = sqlite3.connect(self.name_database)
        self.cur = self.con.cursor()
