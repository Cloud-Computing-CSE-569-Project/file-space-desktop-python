import sqlite3


class DBConnector:
    def __init__(self):
        self.connection = sqlite3.connect("/tmp/sql.db")
        self._init_connection()
    def _init_connection(self):

        try:

            cursor = self.connection.cursor()
            query = "select sqlite_version();"
            cursor.execute(query)
            result = cursor.fetchall()
            print("SQLite Version is {}".format(result))

            #cursor.close()

        except Exception as e:
            print(e)
       
    def create_table(self):

        # cursor object
        cursor_obj = self.connection.cursor()

        cursor_obj.execute("DROP TABLE IF EXISTS Files")

        table = """ CREATE TABLE Files (
                id int primary_key auto_increment,
			    name VARCHAR(255) NOT NULL unique,
			    version CHAR(25)); """

        cursor_obj.execute(table)

        print("Database created with success")

        self._close()

    def _close(self):
        self.connection.close()
    
    def update(self, name:str, version:str):
        cursor = self.connection.cursor()
        cursor.execute("""Insert into Files(name, version) values('{0}', '{1}')""".format(name, version))
        self.connection.commit()

    def fetch_all(self):
        cursor = self.connection.cursor()
        cursor.execute("""SELECT * FROM Files;""")
        return cursor.fetchall()
