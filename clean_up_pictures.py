from PIL import Image
from pathlib import Path
from os import rename, scandir
from datetime import datetime
#functions to clean up pictures
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
            elif entry.is_file() and entry.name.endswith(('.jpg', '.jpeg', '.png', '.gif','JPEG','JPG','PNG')):
                picture_list.append(entry.path)
    return picture_list

def move_pictures(pictures, new_folder, sort=False):
    #move all pictures in the list to the new folder
    for picture in pictures:
        try:
            if sort:
                new_path = sort_pictures(picture,new_folder)
            else:
                new_path = Path.joinpath(Path(new_folder),Path(picture).name)
            rename(picture, new_path)
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