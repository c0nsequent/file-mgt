from PIL import Image
from pathlib import Path
from os import rename, scandir
from datetime import datetime
import shutil 
from threading import Thread
from threading import Semaphore
#functions to clean up pictures
thread_lock = Semaphore(6)

def find_duplicates():
    #find all duplicates in the directory
    #return a list of the duplicates
    pass
def delete_duplicates():
    #delete all duplicates in the directory
    pass
def find_pictures(folder, root=False) -> list:
    picture_list = []
    with scandir(folder) as entries:
        for entry in entries:
            if entry.is_dir() and root == True:
                for pic in find_pictures(entry.path,root=root):
                    picture_list.append(pic)
            elif entry.is_file() and entry.name.endswith(('.jpg', '.jpeg', '.png', '.gif','JPEG','JPG','PNG','RAF')):
                picture_list.append(entry.path)
    return picture_list

def move_pictures(pictures, new_folder, sort=False):
    #move all pictures in the list to the new folder
    thread_list = list()
    thread_lock.acquire()
    while len(pictures) > 200:
        t1 = Thread(target=move_pictures, args=(pictures[:199],new_folder,sort))
        thread_list.append(t1)
        t1.start()
        pictures = pictures[199:]
    for picture in pictures:
        move_picture(picture,new_folder,sort)
    thread_lock.release()
    while thread_list:
        for t in thread_list:
            print('Thread wird gejoint: ' + str(t))
            t = Thread()
            if t.is_alive(): pass
            else: 
                t.join()
                thread_list.pop(t)
        
def move_picture(picture,new_folder, sort):
    try:
        if sort:
            new_path = sort_pictures(picture,new_folder)
        else:
                new_path = Path.joinpath(Path(new_folder),Path(picture).name)
        shutil.move(picture, new_path)
    except Exception as e:
        print(e)

def copy_pictures(pictures, new_folder, sort=False):
    #move all pictures in the list to the new folder
    thread_list = list()
    thread_lock.acquire()
    while len(pictures) > 200:
        t1 = Thread(target=copy_pictures, args=(pictures[:199],new_folder,sort))
        thread_list.append(t1)
        t1.start()
        pictures = pictures[199:]
    for picture in pictures:
        copy_picture(picture,new_folder,sort)
    thread_lock.release()
    while thread_list:
        for t in thread_list:
            print('Copy Thread wird gejoint: ' + str(t))
            t = Thread()
            if t.is_alive(): pass
            else: 
                t.join()
                thread_list.pop(t)

def copy_picture(picture,new_folder, sort):
    try:
        if sort:
            new_path = sort_pictures(picture,new_folder)
        else:
                new_path = Path.joinpath(Path(new_folder),Path(picture).name)
        shutil.copy2(picture, new_path)
    except Exception as e:
        print(e)

def get_picture_date(picture):
    try:
        picture_data = Image.open(picture)
        exif_data = picture_data.getexif()
        date = exif_data.get(306)
        if date is not None: 
            date = datetime.strptime(date, '%Y:%m:%d %H:%M:%S')
            return date
        else:
            return False
    except Exception as e:
        print(f'Fehler in function get_picture_date: {picture}: {e}')
        return False


def sort_pictures(picture,new_folder):
    new_path = Path(new_folder)
    date = get_picture_date(picture)
    if date:
        sort_list = [Path(str(date.year)),Path(str(date.month))]
    elif 'screenshot' in Path(picture).name.lower():
          sort_list = [Path('Screenshots')] 
    else:
        sort_list = [Path('unsortiert')]
    for dir in sort_list:
        try:        
            new_path = Path.joinpath(new_path,dir)
            if not new_path.exists():
                new_path.mkdir()
        except Exception as e:
            print(e)
    return Path.joinpath(new_path,Path(picture).name)