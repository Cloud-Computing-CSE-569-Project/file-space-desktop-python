from models.event import SyncEvent


class Indexer:
    def event_handler(self, event: SyncEvent):
        if event is SyncEvent.deleted:
            self._event_delete()
        elif event is SyncEvent.created:
            self._event_create()
        elif event is SyncEvent.updated:
            self._event_update()
        else:
            print("Nothing happened")

    def _event_update(self):
        print("Something updated")

    def _event_delete(self):
        print("Something deleted")

    def _event_create(self):
        print("New File added")
