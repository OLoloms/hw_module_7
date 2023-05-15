import sys
import re
from pathlib import Path
import os
import shutil

"""
1. Функція, яка повертає шлях до папки переданий під час запуску скрипта
2. Функція, яка обробляє папки 
3. Функція, яка перейменовує файли та папки
"""
###Блок реалізації функції get_path
def get_path() -> str:
    try:
        return sys.argv[1]
    except:
        print('Аргументи при запуску Python-скрипта не передані')
###

###Блок реалізації функції normalize
CYRILLIC = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ'
LATIN = ("a", "b", "v", "g", "d", "e", "e", "j", "z", "i", "j", "k", "l", "m", "n", "o", "p", "r", \
    "s", "t", "u", "f", "h", "ts", "ch", "sh", "sch", "", "y", "", "e", "yu", "ya", "je", "i", "ji", "g")
TRANS = {}
for c,l in zip(CYRILLIC, LATIN):
    TRANS[ord(c)] = l
    TRANS[ord(c.upper())] = l.upper()

pattern = re.compile(r'[^A-Za-z0-9]') # шаблон, для пошуку не латинських літер та цифр

def normalize(name: str) -> str:
    """A function that transliterates file names and replaces all non-Latin letters and numbers 
    with the symbol '_'"""
    file_attributes = name.split('.')
    file_attributes[0] = file_attributes[0].translate(TRANS)
    file_attributes[0] = pattern.sub('_', file_attributes[0])
    new_file_name = '.'.join(file_attributes)
    return new_file_name
###    


###Блок реалізації функції, яка обробляє папки
extensions = {
    'images': ['.jpeg','.png','.jpg','.svg'],
    'videos': ['.avi', '.mp4', '.mov', 'mkv'],
    'documents': ['.doc', '.docx', '.txt', '.pdf', '.xlsx', '.pptx'],
    'musics': ['.mp3', '.ogg', '.wav', '.amr'],
    'archives': ['.zip', '.gz', '.tar', '.7z'],
    'unknown_extensions': []
}

names_folders = ['images', 'videos', 'documents', 'musics', 'archives']

def create_directories(path: str):
    """A function that creates folders from the specified names"""
    try:
        for name in extensions:
            if not os.path.exists(name):
                os.mkdir(os.path.join(path, name))
        return 'Папки успішно створені'
    except:
        return 'При створені папок виникла помилка'
        
def get_directories_path(path: str):
    """A function that creates a list from folder paths"""
    directories_path = []
    for file in os.scandir(path):
        if os.path.isdir(file):
            directories_path.append(file.path)
    return directories_path

main_path = ''

def sorting_files(path: str):
    """A function that takes a folder path as an argument and sorts the files inside the folder by category"""
    global main_path
    if not main_path:
        main_path = path
    ext_lists = list(extensions.items())
    files = os.listdir(path)
    for file in files:
        low_path = os.path.join(path, file)
        if os.path.isdir(low_path) and file not in names_folders:
            sorting_files(low_path)
        else:
            file_suffix = Path(low_path).suffix
            for dict_items in range(len(ext_lists)):
                if file_suffix in ext_lists[4][1]:
                    if not os.path.exists(os.path.join(path, 'archives', (Path(file).name).split('.')[0])):
                        os.mkdir(os.path.join(path, 'archives', (Path(file).name).split('.')[0]))
                    shutil.unpack_archive(os.path.join(main_path, file), os.path.join(path, 'archives', (Path(file).name).split('.')[0]))
                    
                elif file_suffix in ext_lists[dict_items][1]:
                    new_file_name = normalize(file)
                    os.rename(low_path, f'{main_path}\\{ext_lists[dict_items][0]}\\{new_file_name}')
                    
                else:
                    if file not in names_folders: 
                        print(f'Невідоме розширення файлу - {file_suffix}')
                        
                    else:
                        print(f'Файл є директорією з назвою - {file}')
                        


def remove_empty_folders(path: str):
    """A function that takes a folder path as argument and deletes empty folders within a folder"""
    subfolder_path = get_directories_path(path)
    for p in subfolder_path:
        if not os.listdir(p) and Path(p).name not in names_folders:
            print(f'Видаляємо порожню папку {Path(p).name}')
            os.rmdir(p)
        
    return 'Empty folders is deleted'
                


    

def clean():
    try:
        path = sys.argv[1]
        get_path()
        create_directories(path)
        get_directories_path(path)
        sorting_files(path)
        remove_empty_folders(path)
    except:
        print('Неправильный шлях до папки')
    

if __name__ == '__main__':
    clean()

