from os import scandir, rename
from os.path import splitext, exists, join
import sys
import time
import logging
from shutil import move
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

source_dir = "/Users/ThinkPad P53s/Downloads"
dest_dir_docs = "/Users/ThinkPad P53s/Desktop/Folder_Docs"
dest_dir_soundsnmusic = "/Users/ThinkPad P53s/Desktop/Folder_Sounds"
dest_dir_zip = "/Users/ThinkPad P53s/Desktop/Folder_Zip"
dest_dir_images = "/Users/ThinkPad P53s/Desktop/Folder_Images"

def makeUnique(dest, name):
    filename, extension = splitext(name)
    counter = 1
    # * IF FILE EXISTS, ADDS NUMBER TO THE END OF THE FILENAME
    while exists(f"{dest}/{name}"):
        name = f"{filename}({str(counter)}){extension}"
        counter += 1

    return name

# def move(dest, entry, name):
#     file_exists = os.path.exists(dest + "/" + name)
#     if file_exists:
#         unique_name = makeUnique(name)
#         os.rename(entry, unique_name)
#     shutil.move(entry, dest)
    
def move_file(dest, entry, name):
    if exists(f"{dest}/{name}"):
        unique_name = makeUnique(dest, name)
        oldName = join(dest, name)
        newName = join(dest, unique_name)
        rename(oldName, newName)
    move(entry, dest)


class MoveHandler(FileSystemEventHandler):
    def on_modified(self, event):
        with scandir(source_dir) as entries:
            for entry in entries:
                name = entry.name
                dest = source_dir
                if name.endswith('.wav') or name.endswith('.mp3'):
                    dest = dest_dir_soundsnmusic
                    move_file(dest, entry, name)
                
                elif name.endswith('.pdf') or name.endswith('.docx'):
                    dest = dest_dir_docs
                    move_file(dest, entry, name)
                
                elif name.endswith('.zip'):
                    dest = dest_dir_zip
                    move_file(dest, entry, name)
                    
                elif name.endswith('.heic') or name.endswith('.png') or name.endswith('.jpeg') or name.endswith('.jpg'):
                    dest = dest_dir_images
                    move_file(dest, entry, name)

        

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    path = source_dir
    event_handler = MoveHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()