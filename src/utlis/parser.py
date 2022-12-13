import os


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
