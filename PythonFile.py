import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class MyHandler(FileSystemEventHandler):
    def __init__(self):
        self.last_modified_time = 0

    def on_modified(self, event):
        self.last_modified_time = time.time()

    def get_mins_since_last_modified(self):
        current_time = time.time()
        mins_since_last_modified = (current_time - self.last_modified_time) / 60
        return mins_since_last_modified

destination = '/n'

observer = Observer()
observer.schedule(MyHandler(), destination, recursive=True)
observer.start()

try:
    while True:
        handler = observer.handlers[0]
        mins_since_last_modified = handler.get_mins_since_last_modified()
        print(f"Minutes since last modified: {mins_since_last_modified:.2f}")
        time.sleep(1)
except KeyboardInterrupt:
    observer.stop()
observer.join()