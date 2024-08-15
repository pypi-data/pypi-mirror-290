import os

import platformdirs

def get_appdata_path() -> str:
    appdatapath: str = platformdirs.user_data_dir("est-notes")
    return appdatapath

def init() -> None:
    if os.path.isdir(get_appdata_path()) == False:
        os.makedirs(get_appdata_path())
    os.chdir(get_appdata_path())

def goto_profile_dir(profile):
    init()

    if os.path.isdir(profile) == False:
        os.mkdir(profile)
    os.chdir(profile)
