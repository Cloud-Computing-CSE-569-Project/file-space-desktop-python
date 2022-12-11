import os
from time import sleep
from threading import Thread
from .indexer import Indexer
from models.event import SyncEvent
from config.aws import Services
from config.db import DBConnector
import uuid
import multiprocessing
from auth.auth import Auth

user_name = os.getlogin()
sync_folder_name = "My Space"
sync_folder_path = "/home/" + user_name + "/" + sync_folder_name

bucket = Services.s3.Bucket(Services.bucket_name)

indexer = Indexer()
class Watcher:

    def __init__(self, sync_folder_path: str, indexer: Indexer, user_sync_folder: str):
        self.sync_folder_path = sync_folder_path
        self.indexer = indexer
        self.bucket = Services.s3.Bucket(Services.bucket_name)
        self.user_sync_folder = user_sync_folder
        self.remote_thread = SyncRemote()
        self.local_thread = SyncLocal()

    def _start_sync_local(self):
        os.chdir(self.sync_folder_path)
    
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

    def _start_sync_remote(self):
       
        db = DBConnector()
        while True:
            files_local = [file_db[1] for file_db in db.fetch_all()]
            
            cloud_files = [
                file.key.split("/")[-1]
                for file in self.bucket.objects.filter(
                    Prefix="sync_folders/" + self.user_sync_folder + "/"
                )
            ]
            
            for remote_file in cloud_files:

                if remote_file in files_local:
                   pass
                else:
                    print("I am going to download this " + remote_file)
               
                sleep(1)  # wait a sec!

    def start_sync(
        self,
    ):
        """ thread_local = Thread(target=self._start_sync_local)
        thread_remote = Thread(target=self._start_sync_remote)
        thread_local.run()
        thread_remote.run()

        thread_remote.join()
        thread_local.join() """
        self.local_thread.start()
        self.remote_thread.start()

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

class SyncLocal(Thread):
    
    def run(self):
        
        db = DBConnector()
        user = Auth().get_user_info(token=db.fetch_logins()[0][-1])
        os.chdir(sync_folder_path)
        while True:
            files_local = [file_db[1] for file_db in db.fetch_files()]
            
            cloud_files = [
                file.key.split("/")[-1]
                for file in bucket.objects.filter(
                    Prefix="sync_folders/" + user["sync_folder_name"] + "/"
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

                
                indexer.event_handler(change_kind)
                print("Monitoring " + sync_folder_path)
               
                sleep(1)  # wait a sec!


            sleep(1)

class SyncRemote(Thread):

    def _sync_file_remote(self):

        db = DBConnector()
        user = Auth().get_user_info(token=db.fetch_logins()[0][-1])
        while True:
            files_local = [file_db[1] for file_db in db.fetch_files()]
            
            cloud_files = [
                file.key.split("/")[-1]
                for file in bucket.objects.filter(
                    Prefix="sync_folders/" + user["sync_folder_name"] + "/"
                )
            ]
            
            for remote_file in cloud_files:

                if remote_file in files_local:
                   pass
                else:
                    print("I am going to download this " + remote_file)
               
                sleep(1)  # wait a sec!
    def run(self):
       self._sync_file_remote()
