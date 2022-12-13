from threading import Thread
from time import sleep
from datetime import datetime
from queue import Queue
from config.aws import Services
import requests, json
from botocore.exceptions import ClientError
import logging
from utlis.process_percentage import ProgressPercentage
import os
from config.db import DBConnector
from models.local_file import LocalFile

update_url = "http://127.0.0.1:8000/user/update_item"


class Uploader(Thread):
    def __init__(self, user, sync_folder: str, queue=Queue):
        Thread.__init__(self=self)
        self.sync_folder = sync_folder
        self.queue = queue
        self.user = user
        self.local_sync_folder = "/home/" + os.getlogin() + "/"

    def run(self) -> None:
        while True:
            my_file = self.queue.get()
            try:
                if self._upload(file=my_file):
                    # send response to the queue
                    response = requests.post(update_url, json = my_file)
                    if response.status_code == 200:
                        print("Operation finished with success")
                else:
                    logging.warning("Could not send the file")
            except Exception as e:
                logging.exception(e.args)
            finally:
                db = DBConnector()
                ##upate local DB
                ver = os.stat(path= self.local_sync_folder + my_file["file_path"]+my_file["file_name"]).st_dev
                db.update(file =  LocalFile(is_folder=my_file["is_folder"], last_modified = my_file["modified"], file_path = my_file["file_path"]+"/"+my_file["file_name"], version = ver, file_name=my_file["file_name"]))
                self.queue.task_done()

            sleep(2)

    def _upload(self, file: dict) -> bool:
        # upload file to amazon s3
        s3 = Services.s3_bucket
        try:
            file_upload = os.path.join(file["file_path"], file["file_name"])
            
            response = s3.put_object(
                #Bucket= Services.bucket_name,
                Key =  os.path.join(self.sync_folder, self.user["username"], "".join(file_upload.split("/{0}/{1}/".format("home", os.getlogin())))),
            )
            ProgressPercentage(filename=self.local_sync_folder + file_upload)
       
        except ClientError as e:
            logging.error(e)
            return False
        return True
