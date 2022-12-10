import os
from threading import Thread

class Watcher:

    def __init__(self, sync_folder_path:str):
        self.sync_folder_path = sync_folder_path

    def _start_sync(self):
        os.chdir(self.sync_folder_path)
      
      
        while True:
            files = os.listdir()
            count = len(files)
            print("Monitoring " + self.sync_folder_path + "Count: "+ str(count))
            print(*files)
        
    def start_sync(self, ):
        thread = Thread(target=self._start_sync)
        thread.run()
        thread.join()