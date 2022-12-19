import os

from datetime import datetime, timezone


class FileParser:
    def get_local_path(self, path, key):
        """Returns the local file storage path for a given file key"""
        return os.path.join(path, self.prefix, key)

    def get_name(self, path):
        return path.split("/")[-1]

    def get_extension(self, path: str):
        res = ""
        for rev in reversed(path):
            if rev != ".":
                res = res + rev
            else:
                break
        return res

    def file_to_object(self, file: str, user):
        is_folder = os.path.isdir(file)

        data = {
            "is_folder": is_folder,
            "file_extension": "folder"
            if is_folder == True
            else os.path.splitext(p=file)[-1],
            "modified": datetime.fromtimestamp(
                os.stat(file).st_mtime, tz=timezone.utc
            ).strftime("%Y-%m-%d-%H:%M"),
            "file_size": os.stat(file).st_size,
            "file_path": "".join(os.path.realpath(file))
            .replace(os.path.basename(p=file), "")
            .replace("/home/", "")
            .replace(os.getlogin(), ""),
            "file_name": os.path.basename(p=file),
            "is_starred": False,
            "access_list": [
                {
                    "email": user["email"],
                    "id": user["cog_id"],
                }
            ],
            "user": {
                "email": user["email"],
                "id": user["cog_id"],
            },
        }
        return data

    def dict_to_json_file(self, d:dict):
        data = {
            "is_folder": d["is_folder"],
            "file_extension": d["file_extension"],
            "modified": d["modified"],
            "file_size": d["file_size"],
            "file_path": d["file_path"],
            "file_name": d["file_name"],
            "is_starred": d["is_starred"],
            "access_list": d["access_list"],
            "user": d["user"]
        }
        return data
