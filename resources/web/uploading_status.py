from multiprocessing import Queue

class UploadStatus:
    def __init__(self):
        self.queue = Queue()
        self.is_uploading = False

    def enqueue(self, item):
        self.queue.put(item)

    def dequeue(self):
        return self.queue.get()

    def set_uploading(self, uploading):
        self.is_uploading = uploading

    def get_status(self):
        return {
            'queue': self.queue.qsize(),
            'uploading': self.is_uploading
        }