import sqlite3


class Database:
    def __init__(self, path_to_db=r"data/main.db"):
        self.path_to_db = path_to_db

    @property
    def connection(self):
        return sqlite3.connect(self.path_to_db)

    def execute(self, sql: str, parameters: tuple = None, fetchone=False, fetchall=False, commit=False):
        if not parameters:
            parameters = ()
        connection = self.connection
        connection.set_trace_callback(logger)
        cursor = connection.cursor()
        data = None
        cursor.execute(sql, parameters)

        if commit:
            connection.commit()
        if fetchall:
            data = cursor.fetchall()
        if fetchone:
            data = cursor.fetchone()
        connection.close()
        return data

    def create_table_users(self) -> object:
        sql = """
        CREATE TABLE if not exists users(
            id int NOT NULL,
            Name varchar(255) NOT NULL,
            username varchar(255),
            date varchar(255) NOT NULL
            );
"""
        self.execute(sql, commit=True)

    @staticmethod
    def format_args(sql, parameters: dict):
        sql += " AND ".join([
            f"{item} = ?" for item in parameters
        ])
        return sql, tuple(parameters.values())

    def add_user(self, id: int, name: str, date: str, username: str = None):
        # SQL_EXAMPLE = "INSERT INTO Users(id, Name, email) VALUES(1, 'John', 'John@gmail.com')"

        sql = """
        INSERT INTO users(id, Name, username, date) VALUES(?, ?, ?, ?)
        """
        self.execute(sql, parameters=(id, name, username, date), commit=True)

    def select_all_users(self):
        sql = """
        SELECT * FROM users
        """
        return self.execute(sql, fetchall=True)

    def select_all_users_id(self):
        sql = """
        SELECT id FROM users
        """
        return self.execute(sql, fetchall=True)

    def select_all_users_name(self):
        sql = """
        SELECT Name FROM users
        """
        return self.execute(sql, fetchall=True)

    def select_all_users_username(self):
        sql = """
        SELECT username FROM users
        """
        return self.execute(sql, fetchall=True)

    def select_all_users_date(self):
        sql = """
        SELECT date FROM users
        """
        return self.execute(sql, fetchall=True)

    def select_user(self, **kwargs):
        # SQL_EXAMPLE = "SELECT * FROM Users where id=1 AND Name='John'"
        sql = "SELECT * FROM users WHERE "
        sql, parameters = self.format_args(sql, kwargs)

        return self.execute(sql, parameters=parameters, fetchone=True)

    def count_users(self):
        return self.execute("SELECT COUNT(*) FROM users;", fetchone=True)

    def delete_users(self):
        self.execute("DELETE FROM users WHERE TRUE", commit=True)

def logger(statement):
    print(f"""
_____________________________________________________        
Executing: 
{statement}
_____________________________________________________
""")
