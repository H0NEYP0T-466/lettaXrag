import os
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from utils.logger import log_info
from pathlib import Path


class DataFolderHandler(FileSystemEventHandler):
    """Monitor /data folder for changes"""
    
    def __init__(self, callback, ignore_file=None):
        self.callback = callback
        self.last_modified = time.time()
        self.debounce_seconds = 2
        self.ignore_file = Path(ignore_file).resolve() if ignore_file else None
    
    def _should_ignore(self, event_path):
        """Check if file should be ignored"""
        if self.ignore_file:
            return Path(event_path).resolve() == self.ignore_file
        return False
    
    def on_created(self, event):
        if event.is_directory or self._should_ignore(event.src_path):
            return
        if self._should_process():
            log_info(f"New file detected: {event.src_path}")
            self.callback()
    
    def on_modified(self, event):
        if event.is_directory or self._should_ignore(event.src_path):
            return
        if self._should_process():
            log_info(f"File modified: {event.src_path}")
            self.callback()
    
    def on_deleted(self, event):
        if event.is_directory or self._should_ignore(event.src_path):
            return
        if self._should_process():
            log_info(f"File deleted: {event.src_path}")
            self.callback()
    
    def _should_process(self):
        """Debounce to avoid multiple triggers"""
        current_time = time.time()
        if current_time - self.last_modified > self.debounce_seconds:
            self.last_modified = current_time
            return True
        return False


class FileWatcher:
    """Watch data folder for changes and trigger re-indexing"""
    
    def __init__(self, path: str, callback, ignore_file=None):
        self.path = path
        self.callback = callback
        self.observer = None
        self.ignore_file = ignore_file
    
    def start(self):
        """Start watching the folder"""
        if not os.path.exists(self.path):
            os.makedirs(self.path)
            log_info(f"Created data folder: {self.path}")
        
        event_handler = DataFolderHandler(self.callback, self.ignore_file)
        self.observer = Observer()
        self.observer.schedule(event_handler, self.path, recursive=True)
        self.observer.start()
        log_info(f"Started watching folder: {self.path}")
    
    def stop(self):
        """Stop watching the folder"""
        if self.observer:
            self.observer.stop()
            self.observer.join()
            log_info("Stopped file watcher")
