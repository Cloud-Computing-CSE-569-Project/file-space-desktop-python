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

from models.local_file import LocalFile
from db.db import database, engine
from utlis.crud import DatabaseCrud
from utlis.parser import FileParser

update_url = "http://18.188.244.88/user/update_item"


class Uploader(Thread):
    def __init__(self, user, sync_folder: str, queue=Queue):
        Thread.__init__(self=self)
        self.sync_folder = sync_folder
        self.queue = queue
        self.user = user
        self.local_sync_folder = "/home/" + os.getlogin() + "/"

    def run(self) -> None:
        while True:
            file_request = {}
            my_file = self.queue.get()

            try:
                db = DatabaseCrud()
                if self._upload(file=my_file):
                    # send response to the queue
                    file_request = FileParser().dict_to_json_file(my_file)
                    file_request["file_path"] = os.path.join("/sync_folders", os.getlogin() + "/")

                    response = requests.post(update_url, json=file_request)
                    if response.status_code == 200:
                        ##upate local DB
                        object_id = json.loads(response.text)["object_id"]
                        ver = os.stat(
                            path=self.local_sync_folder
                            + my_file["file_path"]
                            + my_file["file_name"]
                        ).st_dev
                        db.update(
                            file=LocalFile(
                                is_folder=my_file["is_folder"],
                                last_modified=my_file["modified"],
                                file_path=my_file["file_path"]
                                + my_file["file_name"],
                                version=ver,
                                file_name=my_file["file_name"],
                                object_id=object_id,
                            )
                        )
                else:
                    logging.warning("Could not send the file")
            except Exception as e:
                logging.exception(e.args)
            finally:
                print("Waiting New changes")
                self.queue.task_done()

            sleep(2)

    def _upload(self, file: dict) -> bool:
        # upload file to amazon s3
        s3 = Services.s3_bucket
     
        try:
            file_upload = os.path.join(file["file_path"], file["file_name"])

            response = s3.upload_file(
                    Filename=self.local_sync_folder + file_upload,
                    Key=self.sync_folder + "/" + file["file_name"],
                   
                )
            
        except ClientError as e:
            logging.error(e)
            return False
        return True
