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
        print(f'self.last_modified_time: {self.last_modified_time}')
        mins_since_last_modified = ((current_time - self.last_modified_time) /60)
        return mins_since_last_modified

destination = '/notebooks/notebooks/'

handler = MyHandler()  # Create the handler instance
observer = Observer()
observer.schedule(handler, destination, recursive=False)  # Pass the handler instance to the observer
observer.start()

try:
    while True:
        mins_since_last_modified = handler.get_mins_since_last_modified()  # Use the handler instance to get the minutes since last modified
        print(f"Minutes since last modified: {mins_since_last_modified}")
        time.sleep(1)
except KeyboardInterrupt:
    observer.stop()
observer.join()