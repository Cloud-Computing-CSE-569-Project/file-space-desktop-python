from threading import Thread
from time import sleep
from datetime import datetime
from queue import Queue


class Downloader(Thread):
    def __init__(self, sync_folder: str, queue=Queue):
        Thread.__init__(self=self)
        self.sync_folder = sync_folder
        self.queue = queue

    def run(self) -> None:
        while True:
            file = self.queue.get()
            try:
                self._download(file=file)
            finally:
                self.queue.task_done()
                print("Operation finished with success")

            sleep(1)

    def _download(self, file: dict):
        print("I am downloading this ", file["file_name"])
