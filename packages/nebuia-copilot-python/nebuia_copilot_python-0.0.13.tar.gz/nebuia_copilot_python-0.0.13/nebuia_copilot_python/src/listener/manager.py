import time
import threading
from typing import Dict
from queue import Queue
from threading import Event
from nebuia_copilot_python.src.api_client import APIClient
from nebuia_copilot_python.src.models import BatchType, StatusDocument


class ThreadedEventBasedListener:
    def __init__(self, api_client: APIClient, status: StatusDocument, batchType: BatchType, interval: int, limit_documents: int):
        self.api_client = api_client
        self.status = status
        self.batch_type = batchType
        self.interval = interval
        self.limit_documents = limit_documents
        self.stop_event = Event()
        self.results_queue = Queue()
        self.thread = None

    def fetch_documents(self):
        documents = self.api_client.get_documents_by_status_and_batch(
            status=self.status,
            batch_type=self.batch_type,
            limit=self.limit_documents
        )
        return documents

    def run(self):
        while not self.stop_event.is_set():
            documents = self.fetch_documents()
            for doc in documents.documents:
                self.results_queue.put((self.status, doc))
            time.sleep(self.interval)

    def start(self):
        if self.thread is None or not self.thread.is_alive():
            self.thread = threading.Thread(target=self.run)
            self.thread.start()

    def stop(self):
        self.stop_event.set()
        if self.thread and self.thread.is_alive():
            self.thread.join()

    def get_results(self):
        while not self.results_queue.empty():
            yield self.results_queue.get()

class ThreadedListenerManager:
    def __init__(self, api_client: APIClient):
        self.api_client = api_client
        self.listeners: Dict[StatusDocument, ThreadedEventBasedListener] = {}

    def add_listener(self, status: StatusDocument, batchType: BatchType, interval: int, limit_documents: int) -> ThreadedEventBasedListener:
        listener = ThreadedEventBasedListener(
            self.api_client, status=status, batchType=batchType, interval=interval, 
            limit_documents=limit_documents
        )
        self.listeners[status] = listener
        return listener

    def start_all_listeners(self):
        for listener in self.listeners.values():
            listener.start()

    def stop_all_listeners(self):
        for listener in self.listeners.values():
            listener.stop()

    def get_all_results(self):
        for status, listener in self.listeners.items():
            yield from listener.get_results()