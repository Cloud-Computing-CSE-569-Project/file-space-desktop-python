import os
from time import sleep
from threading import Thread
from .indexer import Indexer
from models.event import SyncEvent
from config.aws import Services
from config.db import DBConnector
import uuid
import multiprocessing


class Watcher:
    def __init__(self, sync_folder_path: str, indexer: Indexer, user_sync_folder: str):
        self.sync_folder_path = sync_folder_path
        self.indexer = indexer
        self.bucket = Services.s3.Bucket(Services.bucket_name)
        self.user_sync_folder = user_sync_folder

    def _start_sync(self):
        os.chdir(self.sync_folder_path)
        change_kind = Indexer()
        db = DBConnector()
        while True:
            files_local = [file_db[1] for file_db in db.fetch_all()]
            

            cloud_files = [
                file.key.split("/")[-1]
                for file in self.bucket.objects.filter(
                    Prefix="sync_folders/" + self.user_sync_folder + "/"
                )
            ]
            print(cloud_files)
            for file in os.listdir():

                if file not in files_local:
                    
                    if file not in cloud_files and os.path.isfile(file):
                        
                        db.update(name=file, version=str("first"))
                        change_kind = SyncEvent(2)
                    else:
                        change_kind = SyncEvent(3)
                else:
                    print("No")
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

    def _sync(self, key):
        for file in os.listdir():
            if file != key:
                print("Print not found I will upload")
            else:
                print("Found, I will try to update")

    def sync(self):
        """Syncs the local and remote S3 copies"""
        pool = multiprocessing.Pool()

        files_on_cloud = [
            file.key.split("/")[-1]
            for file in self.bucket.objects.filter(
                Prefix="sync_folders/" + self.user_sync_folder + "/"
            )
        ]
        print(files_on_cloud)
        pool.starmap(self._sync, files_on_cloud)
