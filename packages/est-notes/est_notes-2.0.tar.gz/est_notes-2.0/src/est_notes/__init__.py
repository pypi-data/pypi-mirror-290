from enum import STRICT
import os
import shutil
from datetime import date
import json
import uuid

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


def sort_name(val):
    return val['content']
def sort_date(val):
    return val['created']
def sort_target(val):
    return val['target_time']
def sort_prio(val):
    return val['priority']

def create_profile_data(profile: str, git_address: str, void: str = '') -> None:
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

    empty: list = []
    emptyjson: str = json.dumps(empty)
    emptyenc: bytes = enc.encrypt(emptyjson.encode())

    if os.path.isfile('todos') == False:
        with open('todos', 'wb') as file:
            file.write(emptyenc)

    if os.path.isfile('adds') == False:
        with open('adds', 'wb') as file:
            file.write(emptyenc)

    if os.path.isfile('removals') == False:
        with open('removals', 'w') as file:
            file.write('')

def create_profile(git_address: str, void: str = '') -> str:
    other_utils.init()
    newuuid: str = uuid_utils.gen_uuid()
    create_profile_data(newuuid, git_address)
    return newuuid

def get_todos(profile, sorting: str = 'priority') -> list:
    create_profile_data(profile, '', '')

    with open('key', 'rb') as file:
        key: bytes = file.read()
    enc = Fernet(key)

    with open('todos', 'rb') as file:
        todosbytes: bytes = file.read()

    todosjson = enc.decrypt(todosbytes).decode()
    todos: list = json.loads(todosjson)

    with open('adds', 'rb') as file:
        addsbytes: bytes = file.read()

    addsjson: str = enc.decrypt(addsbytes).decode()
    adds: list = json.loads(addsjson)

    with open('removals', 'r') as file:
        removalsstr: str = file.read()
    removals: list = removalsstr.split('\n')

    for i in range(len(adds)):
        todos.append(adds[i])

    for i in range(len(removals)):
        for j in range(len(todos)):
            if todos[j]['uuid'] == removals[i]:
                del todos[j]
                break

    if sorting == 'name':
        todos.sort(key=sort_name)
    if sorting == 'creation':
        todos.sort(key=sort_date)
    if sorting == 'target':
        todos.sort(key=sort_target)
    if sorting == 'priority':
        todos.sort(key=sort_prio)

    return todos

def add_todo(profile: str, content: str, priority: int=2, completed: bool=False, target_time: str=date.ctime(date.today()), creation_time: str=date.ctime(date.today())) -> None:
    todo = {
        'content': content,
        'priority': priority,
        'completed': completed,
        'created': creation_time,
        'target_time': target_time,
        'uuid': str(uuid.uuid4())
    }

    create_profile_data(profile, '', '')

    with open('key', 'rb') as file:
        key: bytes = file.read()
    enc = Fernet(key)

    with open('adds', 'rb') as file:
        addsbytes: bytes = file.read()

    addsjson: str = enc.decrypt(addsbytes).decode()
    adds: list = json.loads(addsjson)

    adds.append(todo)

    addsjson: str = json.dumps(adds)
    addsbytes: bytes = enc.encrypt(addsjson.encode())

    with open('adds', 'wb') as file:
        file.write(addsbytes)

def remove_todo(profile: str, todo_uuid: str) -> None:
    create_profile_data(profile, '', '')

    with open('removals', 'r') as file:
        removalsstr: str = file.read()
    removals: list = removalsstr.split('\n')

    removals.append(todo_uuid)

    removalsstr: str = '\n'.join(removals)
    with open('removals', 'w') as file:
        file.write(removalsstr)

def sync(profile: str) -> None:
    create_profile_data(profile, '', '')

    with open('repo', 'r') as file:
        git_address = file.read()

    with open('key', 'rb') as file:
        key: bytes = file.read()
    enc = Fernet(key)

    with open('adds', 'rb') as file:
        addsbytes: bytes = file.read()

    addsjson: str = enc.decrypt(addsbytes).decode()
    adds: list = json.loads(addsjson)

    with open('removals', 'r') as file:
        removalsstr: str = file.read()
    removals: list = removalsstr.split('\n')

    if os.path.exists('temp-repo') == True:
        shutil.rmtree('temp-repo')

    repo = git.Repo.clone_from(git_address, 'temp-repo')

    repo = git.Repo('temp-repo')
    os.chdir('temp-repo')

    empty: list = []
    emptyjson: str = json.dumps(empty)
    emptyenc: bytes = enc.encrypt(emptyjson.encode())

    if os.path.isfile(profile) == False:
        with open(profile, 'wb') as file:
            file.write(emptyenc)

    with open(profile, 'rb') as file:
        todosbytes: bytes = file.read()

    todosjson = enc.decrypt(todosbytes).decode()
    todos: list = json.loads(todosjson)

    for i in range(len(adds)):
        todos.append(adds[i])

    for i in range(len(removals)):
        for j in range(len(todos)):
            if todos[j]['uuid'] == removals[i]:
                del todos[j]
                break

    todosjson: str = json.dumps(todos)
    todosbytes: bytes = enc.encrypt(todosjson.encode())

    with open(profile, 'wb') as file:
        file.write(todosbytes)

    repo.index.add([profile])
    repo.index.commit('[EST] Synced data with client.')

    origin = repo.remote(name='origin')
    origin.push()

    other_utils.goto_profile_dir(profile)#

    if os.path.exists('temp-repo') == True:
        shutil.rmtree('temp-repo')

    with open('adds', 'wb') as file:
        file.write(emptyenc)

    with open('removals', 'wb') as file:
        file.write(emptyenc)

    with open('todos', 'wb') as file:
        file.write(todosbytes)
