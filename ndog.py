#!/usr/bin/env python

import os
import sys
import time
import subprocess

from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler

class NginxPattern(PatternMatchingEventHandler):
    """Pattern class to match only nginx conf files"""

    def reload(self):
        subprocess.run(['nginx','-s', 'reload'])

    def on_created(self, event):
        filename = os.path.basename(event.src_path)
        dst = sys.argv[2]
        path = f'{dst}{filename}'
        if not os.path.exists(path):
            os.symlink(event.src_path, path)
            self.reload()
        
        
    def on_deleted(self, event):
        filename = os.path.basename(event.src_path)
        dst = sys.argv[2]
        path = f'{dst}{filename}'
        if not os.path.exists(os.readlink(path)):
            os.remove(path)
            self.reload()

    def on_modified(self, event):
        self.reload()

    # def on_moved(self, event):
    #     print(f"ok ok ok, someone moved {event.src_path} to {event.dest_path}")

if __name__ == "__main__":
    patterns = ["*.conf"]
    
    event_handler = NginxPattern(
        patterns, 
        ignore_directories = False,
        case_sensitive=True
    )

    path = sys.argv[1]
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)

    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        observer.join()