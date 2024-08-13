
import os
import shutil

from cryptography.fernet import Fernet
import git

from . import uuid_utils
from . import other_utils
from . import profile_utils

def get_appdata_path() -> str:
    return other_utils.get_appdata_path()
def get_profiles() -> list:
    return profile_utils.get_profiles()
def save_profile(profile: str) -> None:
    profile_utils.save_profile(profile)
def get_saved_profile() -> str:
    return profile_utils.get_saved_profile()
def set_git_address(profile: str, git_address: str) -> None:
    set_git_address(profile, git_address)
def is_valid_uuid(uuid: str) -> bool:
    return is_valid_uuid(uuid)


def create_profile_data(profile: str, git_address: str, first_todo_content: str) -> None:
    other_utils.goto_profile_dir(profile)

    if os.path.isfile('key') == False:
        key: bytes = Fernet.generate_key()
        with open('key', 'wb') as file:
            file.write(key)

    with open('key', 'rb') as file:
        key: bytes = file.read()
    enc = Fernet(key)

    if os.path.isfile('repo') == False:
        with open('repo', 'w') as file:
            file.write(git_address)

    if os.path.isfile('todos') == False:
        first_todo: bytes = enc.encrypt(first_todo_content.encode())
        with open('todos', 'wb') as file:
            file.write(first_todo)

    encrypted_empty: bytes = enc.encrypt(''.encode())

    if os.path.isfile('adds') == False:
        with open('adds', 'wb') as file:
            file.write(encrypted_empty)

    if os.path.isfile('removals') == False:
        with open('removals', 'wb') as file:
            file.write(encrypted_empty)

def create_profile(git_address: str, first_todo_content: str) -> str:
    other_utils.init()
    newuuid: str = uuid_utils.gen_uuid()
    create_profile_data(newuuid, git_address, first_todo_content)
    return newuuid

def get_todos(profile: str) -> list:
    create_profile_data(profile, '', '')

    with open('key', 'rb') as file:
        key: bytes = file.read()
    enc = Fernet(key)

    with open('todos', 'rb') as file:
        todosbytes: bytes = file.read()

    todosstr: str = enc.decrypt(todosbytes).decode()
    todos: list = todosstr.split('\n')

    with open('adds', 'rb') as file:
        addsbytes: bytes = file.read()

    addsstr: str = enc.decrypt(addsbytes).decode()
    adds: list = addsstr.split('\n')

    with open('removals', 'rb') as file:
        removealsbytes: bytes = file.read()

    removalsstr: str = enc.decrypt(removealsbytes).decode()
    removals: list = removalsstr.split('\n')

    for i in adds:
        todos.append(i)

    for i in removals:
        if i in todos:
            todos.remove(i)

    return todos

def add_todo(profile: str, todo: str) -> None:
    create_profile_data(profile, '', '')

    with open('key', 'rb') as file:
        key: bytes = file.read()
    enc = Fernet(key)

    with open('adds', 'rb') as file:
        addsbytes: bytes = file.read()

    addsstr: str = enc.decrypt(addsbytes).decode()
    adds: list = addsstr.split('\n')

    adds.append(todo)

    addsstr: str = '\n'.join(adds)
    addsbytes: bytes = enc.encrypt(addsstr.encode())

    with open('adds', 'wb') as file:
        file.write(addsbytes)

def remove_todo(profile: str, todo: str) -> None:
    create_profile_data(profile, '', '')

    with open('key', 'rb') as file:
        key: bytes = file.read()
    enc = Fernet(key)

    with open('removals', 'rb') as file:
        removalsbytes: bytes = file.read()

    removalsstr: str = enc.decrypt(removalsbytes).decode()
    removals: list = removalsstr.split('\n')

    removals.append(todo)

    removalsstr: str = '\n'.join(removals)
    removalsbytes: bytes = enc.encrypt(removalsstr.encode())

    with open('removals', 'wb') as file:
        file.write(removalsbytes)

def sync(profile: str) -> None:
    create_profile_data(profile, '', '')

    with open('repo', 'r') as file:
        git_address = file.read()

    with open('key', 'rb') as file:
        key: bytes = file.read()
    enc = Fernet(key)

    with open('adds', 'rb') as file:
        addsbytes: bytes = file.read()

    addsstr: str = enc.decrypt(addsbytes).decode()
    adds: list = addsstr.split('\n')

    with open('removals', 'rb') as file:
        removealsbytes: bytes = file.read()

    removalsstr: str = enc.decrypt(removealsbytes).decode()
    removals: list = removalsstr.split('\n')

    other_utils.init()

    if os.path.exists('temp-repo') == True:
        shutil.rmtree('temp-repo')

    repo = git.Repo.clone_from(git_address, 'temp-repo')

    repo = git.Repo('temp-repo')
    os.chdir('temp-repo')

    if os.path.isfile(profile) == False:
        first_todo: bytes = enc.encrypt(''.encode())
        with open(profile, 'wb') as file:
            file.write(first_todo)

    with open(profile, 'rb') as file:
        todosbytes: bytes = file.read()

    todosstr: str = enc.decrypt(todosbytes).decode()
    todos: list = todosstr.split('\n')

    for i in adds:
        todos.append(i)

    for i in removals:
        if i in todos:
            todos.remove(i)

    todosstr: str = '\n'.join(todos)
    todosbytes: bytes = enc.encrypt(todosstr.encode())

    with open(profile, 'wb') as file:
        file.write(todosbytes)

    repo.index.add([profile])
    repo.index.commit('[EST] Synced data with client.')

    origin = repo.remote(name='origin')
    origin.push()

    other_utils.init()
    if os.path.exists('temp-repo') == True:
        shutil.rmtree('temp-repo')

    other_utils.goto_profile_dir(profile)

    encrypted_empty: bytes = enc.encrypt(''.encode())

    with open('adds', 'wb') as file:
        file.write(encrypted_empty)

    with open('removals', 'wb') as file:
        file.write(encrypted_empty)

    with open('todos', 'wb') as file:
        file.write(todosbytes)
