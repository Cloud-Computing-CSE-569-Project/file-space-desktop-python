import sqlite3
from models.login import Login
from models.local_file import LocalFile


class DBConnector:
    def __init__(self):
        self.connection = sqlite3.connect("/tmp/sql.db", timeout=25)
        self._init_connection()

    def _init_connection(self):

        try:
            cursor = self.connection.cursor()
            result = cursor.fetchall()
        except Exception as e:
            print(e)

    def create_table(self):
        # cursor object
        cursor_obj = self.connection.cursor()

        cursor_obj.execute("DROP TABLE IF EXISTS Files")

        table = """ CREATE TABLE Files (
                id integer primary key autoincrement,
                object_id varchar(512) not null unique,
			    file_name VARCHAR(255) NOT NULL unique,
                is_folder BOOL not null,
                last_modified datetime not null,
                file_path varchar(255) not null,
			    version varchar(255)); """

        cursor_obj.execute(table)

        print("Database created with success")

        self._close()

    def create_login_table(self):
        # cursor object
        cursor_obj = self.connection.cursor()

        table = """ CREATE TABLE if not exists logins (
                id integer primary key autoincrement,
                username varchar(255) NOT NULL,
                isLogged bool not null default 0,
                refreshToken varchar(255),
			    accessToken varchar(255)); """

        cursor_obj.execute(table)

    def _close(self):
        self.connection.close()

    def update(self, file: LocalFile):
        cursor = self.connection.cursor()
        cursor.execute(
            """Insert into Files(object_id, file_name, is_folder, last_modified, file_path, version) values('{0}', {1}', '{2}', '{3}', '{4}', '{5}')""".format(
                file.object_id,
                file.file_name,
                file.is_folder,
                file.last_modified,
                file.file_path,
                file.version,
            )
        )
        self.connection.commit()

    def create_login(self, data: Login):
        cursor = self.connection.cursor()

        query = """ Insert into logins(username, isLogged, accessToken) values ('{0}','{1}', '{2}')""".format(
            data.username, data.is_logged, data.access_token
        )

        cursor.execute(query)
        self.connection.commit()

        return cursor.lastrowid

    def fetch_logins(self):
        cursor = self.connection.cursor()
        cursor.execute("""SELECT * FROM logins;""")
        return cursor.fetchall()

    def fetch_files(self):
        cursor = self.connection.cursor()
        cursor.execute("""SELECT * FROM Files;""")
        return cursor.fetchall()

    def ensure_file_exists(self, file_path: str) -> bool:
        cursor = self.connection.cursor()

        response = cursor.execute(
            """ SELECT * FROM Files where file_path = '{0}';""".format(file_path)
        ).fetchall()

        if len(response) == 1:
            return True
        else:
            return False
