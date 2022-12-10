import os


class FileParser:
    def get_local_path(self, path, key):
        """Returns the local file storage path for a given file key"""
        return os.path.join(path, self.prefix, key)

    def get_s3_path(self, key):
        return key.split("/")[-1]
