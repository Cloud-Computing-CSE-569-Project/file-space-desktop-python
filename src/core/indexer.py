from models.event import SyncEvent



class Indexer:
    def __init__(self) -> None:
       pass

    def event_update(self):
        print("Something updated")

    def event_delete(self):
        print("Something deleted")

    def event_create(self):
        print("New File added")
