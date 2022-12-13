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
import requests

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

    def start_sync(
        self,
    ):
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
        request_response = requests.get(
            "http://127.0.0.1:8000/user/us-east-2%3A09f3597a-ad39-4e40-8a7f-502ca9b93458&ipmrt5%40glockapps.com/files/all"
        )

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
                    if remote_file != "":
                        pass
                        print("I am going to download this " + remote_file)
                        self._download_thread(key=remote_file)

                sleep(1)  # wait a sec!

    def run(self):
        self._sync_file_remote()

    def _download(self, key):
        for i in range(100):
            print("Downloading {0}".format(key), i, end=" ")

    def _download_thread(self, key):
        thread = Thread(target=self._download, args=[key])
        thread.run()
