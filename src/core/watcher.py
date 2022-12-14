from .downloader import Downloader
from .uploader import Uploader
import time
from datetime import timezone, datetime
import logging
import os
from utlis.parser import FileParser
from config.db import DBConnector
from threading import Thread
from queue import Queue
import uuid
from watchdog.observers import (
    Observer,
)
from watchdog.events import *
from watchdog.events import (
    LoggingEventHandler,
)
from watchdog.utils.dirsnapshot import DirectorySnapshot

user_name = os.getlogin()
sync_folder_name = "My Space"
sync_folder_path = "/home/" + user_name + "/" + sync_folder_name


class Watcher(object):
    def __init__(self, sync_folder: str, sync_folder_remote: str, user):
        self.sync_folder = sync_folder
        self.sync_folder_remote = sync_folder_remote
        self.observer = Observer()
        self.queue = Queue()
        self.user = user
        

    def sync(self):
        """
        Calls the _schedule  and _start to start synchronizing the file
        """
        os.chdir(self.sync_folder)
        self._schedule()
        self._start()

    def _on_created(self, event: FileCreatedEvent):
        """
        File has been created. As it can be a newly downloaded the file, we need to make sure to add to local DB if it is not there and then call upload to storage.
        """

        print(event)

    def _on_deleted(self, event: FileDeletedEvent):
        """
        If the file has been deleted, the delete from the metadata and consequently from the Cloud storage
        """
        print(event)

    def on_file_moved(self, event: FileMovedEvent):
        pass

    def _on_modified(self, event: FileModifiedEvent):
        """
        File is already in DB and has been changed, compute the file diff and upload only what have changed.
        """
        db = DBConnector()
        # if this file is not yet on d
        if (
            db.ensure_file_exists(file_path=event.src_path)
            and event.src_path != "/My Space" or event.src_path != "My S"
        ):
            # update file to cloud
            pass
        else:
            worker = Uploader(
                sync_folder=self.sync_folder_remote, queue=self.queue, user=self.user
            )
            worker.daemon = True
            worker.start()
            data = FileParser().file_to_object(file=event.src_path, user=self.user)
            self.queue.put(item=data)
        self.queue.join()

    def _on_thread_start(self):
        """
        Push and Pull all the changes that happened while I was sleeping!
        """
        downloader = None
        uploader = None

        # self._pull(worker=downloader)
        self._push(worker=uploader)

    def _pull(self, worker: Thread):
        print("I am just Started - Checking if I missed something!")
        for i in range(8):
            worker = Downloader()
            worker.daemon = True  # make it a daemon
            worker.start()

    def _push(self, worker: Thread):

        print("I just started - Checking if there are things to update!")
        db = DBConnector()
        for file in DirectorySnapshot(path=self.sync_folder, recursive=True).paths:

            if  db.ensure_file_exists(file_path=file) or os.path.samefile(
                self.sync_folder, file
            ):
                continue
            else:
                worker = Uploader(
                    sync_folder=self.sync_folder_remote,
                    queue=self.queue,
                    user=self.user,
                )
                worker.daemon = True
                worker.start()

                data = FileParser().file_to_object(file=file, user=self.user)
                """   is_folder = os.path.isdir(file)

                data = {
                    "is_folder": is_folder,
                    "file_extension": "folder"
                    if is_folder == True
                    else os.path.splitext(p=file)[-1],
                    "modified": datetime.fromtimestamp(
                        os.stat(file).st_mtime, tz=timezone.utc
                    ).strftime("%Y-%m-%d-%H:%M"),
                    "file_size": os.stat(file).st_size,
                    "file_path": "".join(os.path.realpath(file)).replace(
                        os.path.basename(p=file), "").replace("/home/", "").replace(os.getlogin(), ""),
                    "file_name": os.path.basename(p=file),
                    "is_starred": False,
                    "access_list": [
                        {
                            "email": self.user["email"],
                            "id": "us-east-2:85fc0e9a-558b-431a-acc4-7b80aeafa60b",
                        }
                    ],
                    "user": {
                        "email": self.user["email"],
                        "id": "us-east-2:85fc0e9a-558b-431a-acc4-7b80aeafa60b",
                    },
                } """

                self.queue.put(item=data)

        self.queue.join()

    def _schedule(self):
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        path = self.sync_folder
        event_handler = LoggingEventHandler()  # event handler

        event_handler.on_created = self._on_created
        event_handler.on_deleted = self._on_deleted
        event_handler.on_modified = self._on_modified
        event_handler.on_moved = self.on_file_moved

        self.observer.on_thread_start = self._on_thread_start
        self.observer.schedule(event_handler=event_handler, path=path, recursive=True)

    def _start(self):
        self.observer.start()  # star the observer thread
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            self.observer.stop()

        self.observer.join()
