import json
import os
from multiprocessing.pool import ThreadPool

import requests
from clint.textui import progress

levelpath = os.path.join('C:\\', 'Users', os.getlogin(), 'Documents', 'Rhythm Doctor', 'Levels')
file_mode: int = 0


# Create function to handle renaming.
def rename(name, index):
    if os.path.exists(f'{levelpath}/{name.split(".rdzip")[0]} ({index}).rdzip'):
        return rename(name, index + 1)
    else:
        newname = name.split('.rdzip')[0]
        return f"{newname} ({index})" + ".rdzip"


# Download list of files from thing.
def get_initial():
    thing = requests.get(
        'https://script.google.com/macros/s/AKfycbzm3I9ENulE7uOmze53cyDuj7Igi7fmGiQ6w045fCRxs_sK3D4/exec').content
    stuff = json.loads(thing.decode('utf-8'))
    print("Total number of levels: " + str(len(stuff)) + "\n")
    return stuff


def download(url):
    # Set name of level to id if Drive, else set to discord link name.
    if url.startswith('https://drive.google.com/'):
        name = url.split('id=')[-1] + ".rdzip"
    else:
        name = url.split('/')[-1]

    # Append (1) to file name if already exists.
    if os.path.exists(f'{levelpath}/{name}'):
        if file_mode == 0:
            name = rename(name, 1)
        elif file_mode == 2:
            print(f"Skipping {name}")
            return name

    # Download and save zipped level in preZip.
    dwn = requests.get(url, stream=True)
    with open(f'{levelpath}/{name}', 'wb') as f:
        f.write(dwn.content)
    return name


def download_all(url_list, start, end, threads, file):
    urls = []
    global file_mode
    file_mode = file
    for level in url_list[start - 1:end]:
        urls.append(level['download_url'])

    results = ThreadPool(threads).imap_unordered(download, urls)
    for chunk in progress.bar(results, expected_size=len(urls)):
        print(f"Done downloading {chunk}" + ' ' * 30)


def positional_download(url_list, file, threads, file_thing):
    urls = []
    global file_mode
    file_mode = file_thing
    for level in url_list:
        urls.append(level['download_url'])

    with open(file, 'r') as data:
        urls_dl = data.read().splitlines()
        urls = set(urls).difference(urls_dl)

    results = ThreadPool(threads).imap_unordered(download, urls)
    for chunk in progress.bar(results, expected_size=len(urls)):
        print(f"Done downloading {chunk}" + ' ' * 30)
