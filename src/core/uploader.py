from threading import Thread
from time import sleep
from datetime import datetime
from queue import Queue
from config.aws import Services
import requests, json

backend_url = ""


class Uploader(Thread):
    def __init__(self, sync_folder: str, queue=Queue):
        Thread.__init__(self=self)
        self.sync_folder = sync_folder
        self.queue = queue

    def run(self) -> None:
        while True:
            file = self.queue.get()
            try:
                self._upload(file=file)
            finally:
                self.queue.task_done()
                print("Operation finished with success")

            sleep(1)

    def _upload(self, file: dict):
        print("I am uploading this ", file["file_name"])
        # upload file to amazon s3
        # send response to the queue
        """ bucket = Services.s3.Bucket(Bucket= Services.bucket_name)
        response = bucket.upload_file() """
