import json
import time
import logging
import os
from utlis.parser import FileParser
from threading import Thread
from config.db import DBConnector

from watchdog.observers import (
    Observer,
)  # creating an instance of the watchdog.observers.Observer from watchdogs class.
from watchdog.events import (
    LoggingEventHandler,
)  # implementing a subclass of watchdog.events.FileSystemEventHandler which is LoggingEventHandler in our case
from watchdog.utils.dirsnapshot import (
    DirectorySnapshot,
    DirectorySnapshotDiff,
    EmptyDirectorySnapshot,
)

user_name = os.getlogin()
sync_folder_name = "My Space"
sync_folder_path = "/home/" + user_name + "/" + sync_folder_name


class Watcher(object):
    def __init__(self, sync_folder: str, sync_folder_remote: str):
        self.sync_folder = sync_folder
        self.sync_folder_remote = sync_folder_remote
        self.observer = Observer()
        

    def sync(self):
        """
        Calls the _schedule  and _start to start synchronizing the file
        """
        os.chdir(self.sync_folder)
        self._schedule()
        self._start()

    def _on_created(self, event):
        """
        File has been created. As it can be a newly downloaded the file, we need to make sure to add to local DB if it is not there and then call upload to storage.
        """
        print(event)

    def _on_deleted(self, event):
        """
        If the file has been deleted, the delete from the metadata and consequently from the Cloud storage
        """
        print()

    def _on_modified(self, event):
        """
        File is already in DB and has been changed, compute the file diff and upload only what have changed.
        """
        print(
            """{0} has been {1}""".format(
                FileParser().get_name(path = event.src_path), event.event_type
            )
        )

    def _download_from_cloud(self, file):
        """
        Download file from cloud that are not in the local DB
        """
        pass

    def _upload_to_cloud(self, file):
        """
        Upload a file to the cloud and communicate with the Queue to update metadata
        """
        pass

    def _on_thread_start(self):
        """
        Push and Pull all the changes that happened while I was sleeping!
        """
        self._pull()
        self._push()


    def _pull(self):
        print("I am just Started - Checking if I missed something!")
        
    """"   id integer primary key autoincrement,
			    file_name VARCHAR(255) NOT NULL unique,
                is_folder BOOL not null,
                last_modified datetime not null,
                file_path varchar(255) not null,
			    version varchar(255)); """

    def _push(self):
       
        db = DBConnector()
        print("I just started - Checking if there are things to update!")
        
       
        for file in os.listdir():
            if db.ensure_file_exists(file_path = file):
                pass
            else:
                print("{0} is not on the table".format(file))
    

    def _describe(self, stat_info):
        print(stat_info)

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