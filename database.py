import sqlite3


class DataBase:
    def __init__(self, name_database="project.db"):
        self.name_database = name_database

    def get_data(self, name_tables, name_data="*", criterion="", data_criterion=None):
        self.con = sqlite3.connect(self.name_database)
        self.cur = self.con.cursor()

        if data_criterion is not None and criterion != "":
            request = self.cur.execute(f"SELECT {name_data} FROM"
                                       f" {name_tables} WHERE {criterion}",
                                       data_criterion).fetchall()
            self.con.close()
            return request

        elif criterion != "":
            request = self.cur.execute(f"SELECT {name_data} FROM "
                                       f"{name_tables}"
                                       f" WHERE {criterion}").fetchall()
            self.con.close()
            return request

        request = self.cur.execute(f"SELECT {name_data} FROM "
                                   f"{name_tables}").fetchall()
        self.con.close()
        return request

    def add_data(self, name_tables, data_criterion=None):
        if data_criterion is not None:
            self.con = sqlite3.connect(self.name_database)
            self.cur = self.con.cursor()

            question_mark = ", ".join(["?" for _ in
                                       range(len(data_criterion))])
            self.cur.execute(f"INSERT INTO {name_tables} VALUES"
                             f"({question_mark})", data_criterion)

            self.con.commit()
            self.con.close()
