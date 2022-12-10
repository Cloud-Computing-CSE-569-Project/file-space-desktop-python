import os
from time import sleep
from threading import Thread
from .indexer import Indexer
from models.event import SyncEvent
from config.aws import Services


class Watcher:
    def __init__(self, sync_folder_path: str, indexer: Indexer, user_sync_folder: str):
        self.sync_folder_path = sync_folder_path
        self.indexer = indexer
        self.bucket_name = Services.bucket_name
        self.user_sync_folder = user_sync_folder

    def _start_sync(self):
        os.chdir(self.sync_folder_path)
        change_kind = Indexer()
       
        
        response = Services.s3.list_objects(
            Bucket=self.bucket_name,
            Prefix="sync_folders/" + self.user_sync_folder + "/",
        )
        cloud_files = [file["Key"] for file in response["Contents"]]
        while True:

            for file in os.listdir():
                if file not in cloud_files and os.path.isfile(file):
                    print(cloud_files)
                    print("File not on the cloud")
                else:
                    change_kind = SyncEvent(4)

            self.indexer.event_handler(change_kind)

            print("Monitoring " + self.sync_folder_path)

            sleep(1)  # wait a sec!

    def start_sync(
        self,
    ):
        thread = Thread(target=self._start_sync)
        thread.run()
        thread.join()
