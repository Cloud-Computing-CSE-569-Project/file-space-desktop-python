from threading import Thread
from time import sleep
from datetime import datetime


class Downloader(Thread):
    def __ini__(self, sync_folder_name: str, sync_folder: str):
        self.sync_folder_name = sync_folder_name
        self.sync_folder = sync_folder
        Thread.__init__(self=self)

    def run(self) -> None:
        for i in range(4):
            print("Hello I am the downloader : ", datetime.now())
            sleep(1)
           

    def _download(self, file_name: str):
        "Download a file given a file path"

    def join(self, timeout=None):
        Thread.join(self=self, timeout=timeout)
