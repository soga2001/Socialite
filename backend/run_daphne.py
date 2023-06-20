import os
import subprocess
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Set the paths to your SSL certificate and private key files
private_key_path = '/Users/Suyogya/Projects/BasedBook/localhost-key.pem'
cert_key_path = '/Users/Suyogya/Projects/BasedBook/localhost.pem'

# Set the Daphne command
daphne_command = [
    'daphne',
    f'-e',
    f'ssl:8000:privateKey={private_key_path}:certKey={cert_key_path}',
    'backend.asgi:application'
]

class FileChangeHandler(FileSystemEventHandler):
    def on_any_event(self, event):
        if event.is_directory:
            return

        if event.event_type in ['created', 'modified', 'deleted']:
            print(f'Restarting Daphne server due to file change: {event.src_path}')
            subprocess.run(daphne_command)

if __name__ == '__main__':
    event_handler = FileChangeHandler()
    observer = Observer()
    observer.schedule(event_handler, path='.', recursive=True)
    observer.start()

    try:
        print('Daphne server started. Watching for file changes...')
        subprocess.run(daphne_command, check=True)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()
