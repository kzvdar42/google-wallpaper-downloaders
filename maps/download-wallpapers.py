#!/usr/bin/env python3

'''
Copyright 2020 Artur Dryomov & Vladislav Kuleykin

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

  http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
'''


import base64
import json
import os
import requests

try:
    import tqdm
    use_tqdm = True
    write = tqdm.write
except ImportError:
    use_tqdm = False
    write = print

REMOTE_URLS = [
    "https://www.gstatic.com/prettyearth/assets/data/v3/{}.json",
    "https://earthview.withgoogle.com/download/{}.jpg",
]
REMOTE_IDS_PATH = "ids.json"
LOCAL_PATH = "wallpapers"

PROMPT_1 = "Download fullsize images? Fullsize images contain watermarks (y/n) "
PROMPT_2 = "Skip already downloaded wallpapers? (y/n) "


def download_wallpapers():
    wallpapers_path = get_wallpapers_path()
    create_directory(wallpapers_path)

    # Choose the url to download from.
    prompt1_res = input(PROMPT_1).lower() == "y"
    REMOTE_URL = REMOTE_URLS[prompt1_res]

    # Check the list of already downloaded wallpapers.
    downloaded_wallpapers = os.listdir(wallpapers_path)
    downloaded_wallpapers_ids = map(lambda x: x.rsplit('.', 1)[0],
                                    downloaded_wallpapers)

    # Prompt the user to skip already downloaded wallpapers.
    wallpapers_ids = set(get_wallpaper_ids())
    if not wallpapers_ids.isdisjoint(downloaded_wallpapers_ids):
        if input(PROMPT_2).lower() == 'y':
            print('Skipping downloaded wallpapers')
            wallpapers_ids.difference_update(downloaded_wallpapers_ids)

    # Start the download.
    print(":: Downloading Google Maps wallpapers.")
    if use_tqdm:
        pbar = tqdm.tqdm(total=len(wallpapers_ids))
    for wallpaper_id in sorted(wallpapers_ids):
        wallpaper_url = REMOTE_URL.format(wallpaper_id)

        # Download the wallpaper using the chosen URL
        try:
            wallpaper_bytes = REQ_FUNCS[prompt1_res](wallpaper_url)
        except ValueError:
            write(f"[ERROR] Could not download the wallpaper with id {wallpaper_id}, retrying with other method.")
            try:
                wallpaper_bytes = REQ_FUNCS[not prompt1_res](wallpaper_url)
            except ValueError:
                write(f"[ERROR] Still can't download the wallpaper. Skipping it.")
                continue

        wallpaper_path = get_wallpaper_path(wallpapers_path, wallpaper_id)
        save_wallpaper(wallpaper_path, wallpaper_bytes)
        if use_tqdm:
            pbar.desc = "Wallpaper id: {}".format(wallpaper_id)
            pbar.update(1)
        else:
            print('Downloaded wallpaper with id: {}'.format(wallpaper_id))


def create_directory(dir_path):
    """Create the directory in the specified path."""
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)


def get_wallpapers_path():
    """Return the absolute path to the wallpapers directory."""
    wallpapers_path = os.path.dirname(os.path.realpath(__file__))
    return os.path.abspath(os.path.join(wallpapers_path, LOCAL_PATH))


def get_wallpaper_ids():
    """Load all the wallpaper IDs from the file."""
    with open(get_wallpaper_ids_path()) as wallpaper_ids_file:
        return json.load(wallpaper_ids_file)


def get_wallpaper_ids_path():
    """Return the absolute path to the wallpapers directory."""
    return os.path.join(os.path.dirname(__file__), REMOTE_IDS_PATH)


def download_wallpaper_official(wallpaper_url):
    """Download the wallpaper using the official URL."""
    response = requests.get(wallpaper_url)
    if response.headers.get('Content-Type') != 'image/jpeg':
        raise ValueError("Response should contain image, maybe it's 404 page.")
    return url_data.content


def get_wallpaper_bytes(wallpaper_info):
    """Get the wallpapers from the json response."""
    bytes_start_position = wallpaper_info.index(",") + 1
    return base64.b64decode(wallpaper_info[bytes_start_position:])


def download_wallpaper_from_plugin(wallpaper_info_url):
    """Download the wallpaper as the plugin do."""
    try:
        json_data = requests.get(wallpaper_info_url).json()['dataUri']
    except json.decoder.JSONDecodeError:
        raise ValueError("Response should contain json data, maybe it's 404 page.")
    return get_wallpaper_bytes(json_data)


def get_wallpaper_path(wallpapers_path, wallpaper_id):
    """Return the path for the wallpaper with specified id."""
    wallpaper_filename = "{id}.jpg".format(id=wallpaper_id)
    return os.path.join(wallpapers_path, wallpaper_filename)


def save_wallpaper(wallpaper_path, wallpaper_bytes):
    """Save the wallpaper to disk."""
    with open(wallpaper_path, "wb") as wallpaper_file:
        wallpaper_file.write(wallpaper_bytes)


REQ_FUNCS = {
    0: download_wallpaper_from_plugin,
    1: download_wallpaper_official,
}

if __name__ == "__main__":
    download_wallpapers()
