import os

from . import uuid_utils
from . import other_utils


def get_profiles() -> list:
    other_utils.init()
    path = other_utils.get_appdata_path()
    profiles = [ name for name in os.listdir(path) if os.path.isdir(os.path.join(path, name)) ]
    return profiles

def save_profile(profile: str) -> None:
    other_utils.init()

    with open('saved_profile', 'w') as file:
        file.write(profile)

def get_saved_profile() -> str:
    other_utils.init()

    if os.path.isfile('saved_profile') == False:
        with open('saved_profile', 'w') as file:
            file.write('')

    with open('saved_profile', 'r') as file:
        profile = file.read()

    return profile

def set_git_address(profile: str, git_address: str) -> None:
    other_utils.init()

    if os.path.isdir(profile) == False:
        os.mkdir(profile)
    os.chdir(profile)

    with open('repo', 'w') as file:
        file.write(git_address)
