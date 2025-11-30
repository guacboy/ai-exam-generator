from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import uuid
import time
import os

REQUEST_PATH = os.path.abspath("request.txt")
REQUEST_DIR = os.path.dirname(REQUEST_PATH)


def generate_id():
    """Generates a unique identifier and stores it in the text file."""
    unique_id = str(uuid.uuid4().hex[:8])
    print("Generated ID:", unique_id)

    with open(REQUEST_PATH, "w") as request_file:
        request_file.write(unique_id)


class Handler(FileSystemEventHandler):
    """Monitores changes does to the directory where the text file is
    located."""

    def on_modified(self, event):
        with open(REQUEST_PATH, "r") as request_file:
            request = request_file.read()
        if request == "generate ID":
            if os.path.abspath(event.src_path) == os.path.abspath(REQUEST_PATH):
                print(f"{REQUEST_PATH} has been modified")
                generate_id()


request_manager = Observer()
request_manager.schedule(Handler(), path=REQUEST_DIR, recursive=False)
request_manager.start()


try:
    while True:
        time.sleep(0.25)
except KeyboardInterrupt:
    request_manager.stop()

request_manager.join()