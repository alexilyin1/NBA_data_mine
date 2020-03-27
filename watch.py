import os
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler


def on_created(event):
    length = len(os.listdir('static/'))
    perc = int(length/59) * 100
    return perc, f'{perc}%'

def create_handler():
    patterns = '*.csv'
    ignore_patterns = ""
    ignore_directories = False
    case_sensitive = True
    event_handler = PatternMatchingEventHandler(patterns, ignore_patterns,
                                                ignore_directories, case_sensitive)
    event_handler.on_created = on_created
    return event_handler


def create_observer(path:str, handler):
    path = path
    go_recursively = True
    observer = Observer()
    observer.schedule(handler, path, recursive=go_recursively)
    return observer
