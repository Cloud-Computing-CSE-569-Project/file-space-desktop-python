from db.db import engine, files
from sqlalchemy import text

from models.local_file import LocalFile
class DatabaseCrud:

    def select(self, query):
        my_query = text(query)

        response = engine.execute(my_query).fetchall()

        return response

    def ensure_file_exists(self, file_path: str) -> bool:

        response = engine.execute(
           text(""" SELECT * FROM files where file_path = '{0}';""".format(file_path))
        ).fetchall()

        if len(response) == 1:
            return True
        else:
            return False

    def update(self, file: LocalFile):
        query = text("""Insert into files(object_id, file_name, is_folder, last_modified, file_path, version) values('{0}', '{1}', '{2}', '{3}', '{4}', '{5}')""".format(
                file.object_id,
                file.file_name,
                file.is_folder,
                file.last_modified,
                file.file_path,
                file.version,
            ))
        result = engine.execute( query )

    def delete(self, file:str):
        query = text(""" delete from files where file_name = '{0}'""".format(file))
        result = engine.execute(query)
