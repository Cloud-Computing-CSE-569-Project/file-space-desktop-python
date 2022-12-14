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
                    "id": "us-east-2:85fc0e9a-558b-431a-acc4-7b80aeafa60b",
                }
            ],
            "user": {
                "email": user["email"],
                "id": "us-east-2:85fc0e9a-558b-431a-acc4-7b80aeafa60b",
            },
        }
        return data
