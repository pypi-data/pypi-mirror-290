from typing import Callable
from loguru import logger
from nebuia_copilot_python.src.api_client import APIClient
from nebuia_copilot_python.src.listener.manager import ThreadedListenerManager
from nebuia_copilot_python.src.models import BatchType, StatusDocument

class ListenerIntegrator:
    def __init__(self, api_client: APIClient):
        self.manager = ThreadedListenerManager(api_client)
        self.on_document_handler = None
        self.on_listener_start_handler = None
        self.on_listener_stop_handler = None
        self.on_all_complete_handler = None

    def add_listener(self, status: StatusDocument, batch_type: BatchType, interval: int, limit_documents: int):
        self.manager.add_listener(status, batch_type, interval, limit_documents)

    def set_on_document_handler(self, handler: Callable[[StatusDocument, dict], None]):
        self.on_document_handler = handler

    def set_on_listener_start_handler(self, handler: Callable[[StatusDocument], None]):
        self.on_listener_start_handler = handler

    def set_on_listener_stop_handler(self, handler: Callable[[StatusDocument], None]):
        self.on_listener_stop_handler = handler

    def set_on_all_complete_handler(self, handler: Callable[[], None]):
        self.on_all_complete_handler = handler

    def on_document(self, status, doc):
        if self.on_document_handler:
            self.on_document_handler(status, doc)
        else:
            logger.info(f"New document from {status}: {doc}")

    def on_listener_start(self, status):
        if self.on_listener_start_handler:
            self.on_listener_start_handler(status)
        else:
            logger.info(f"Listener started for status: {status}")

    def on_listener_stop(self, status):
        if self.on_listener_stop_handler:
            self.on_listener_stop_handler(status)
        else:
            logger.info(f"Listener stopped for status: {status}")

    def on_all_complete(self):
        if self.on_all_complete_handler:
            self.on_all_complete_handler()
        else:
            logger.info("All listeners have completed their work")

    def setup_event_handlers(self):
        self.manager.events.on_document += self.on_document
        self.manager.events.on_listener_start += self.on_listener_start
        self.manager.events.on_listener_stop += self.on_listener_stop
        self.manager.events.on_all_complete += self.on_all_complete

    def run(self):
        self.setup_event_handlers()
        self.manager.run()