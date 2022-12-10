import os
from time import sleep
from threading import Thread
from .indexer import Indexer
from models.event import SyncEvent


class Watcher:
    def __init__(self, sync_folder_path: str, indexer: Indexer):
        self.sync_folder_path = sync_folder_path
        self.indexer = indexer

    def _start_sync(self):
        os.chdir(self.sync_folder_path)
        change_kind = Indexer()
      
        while True:
            files = []
            for file in os.listdir():
                if file not in files and os.path.isfile(file):
                    print("Something happened")
                    files.append(open(file, "r"))
                else:
                    change_kind = SyncEvent(4)

            self.indexer.event_handler(change_kind)
            count = len(files)
            print("Monitoring " + self.sync_folder_path + "Count: " + str(count))

            sleep(1)  # wait a sec!

    def start_sync(
        self,
    ):
        thread = Thread(target=self._start_sync)
        thread.run()
        thread.join()
