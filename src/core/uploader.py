from threading import Thread
from time import sleep
from datetime import datetime


class Uploader(Thread):
    def __ini__(self, sync_folder_name: str, sync_folder: str):
        self.sync_folder_name = sync_folder_name
        self.sync_folder = sync_folder

    def run(self) -> None:
        while True:
            print("Hello I am the uploader : ", datetime.now())
            sleep(1)

    def _upload(self, file_name: str):
        "Upload a file given a file path"

    def join(self, timeout=None):
        Thread.join(self=self, timeout=timeout)
