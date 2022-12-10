import os
from time import sleep
from threading import Thread
from .indexer import Indexer
from models.event import SyncEvent
from config.aws import Services

class Watcher:
    def __init__(self, sync_folder_path: str, indexer: Indexer, bucket_name=str):
        self.sync_folder_path = sync_folder_path
        self.indexer = indexer
        self.bucket_name = bucket_name

    def _start_sync(self):
        os.chdir(self.sync_folder_path)
        change_kind = Indexer()
        
        bucket = Services.s3.Bucket(self.bucket_name)
        cloud_files = bucket.objects.all()
        while True:
            
            for file in os.listdir():
                if file not in cloud_files and os.path.isfile(file):   
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
