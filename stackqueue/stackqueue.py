from queue import LifoQueue


class StackQueue:
    def __init__(self):
        self.inbox = LifoQueue()
        self.outbox = LifoQueue()

    def pop(self, default=None):
        if self.outbox.empty():
            while not self.inbox.empty():
                self.outbox.put(self.inbox.get())
        if not self.outbox.empty():
            return self.outbox.get()
        return default

    def put(self, element):
        if not self.outbox.empty():
            while not self.outbox.empty():
                self.inbox.put(self.outbox.get())
        self.inbox.put(element)
