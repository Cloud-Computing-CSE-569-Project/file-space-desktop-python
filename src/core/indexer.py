from models.event import SyncEvent
from config.db import DBConnector

class Indexer:
   
    def __init__(self) -> None:
        self.db = DBConnector()

    def event_update(self):
        print("Something updated")

    def event_delete(self):
        print("Something deleted")

    def event_create(self):
        print("New File added")
