import os
import shutil
import json
import uuid

from cryptography.fernet import Fernet
import git
import platformdirs

def create_profile_data(profile: str, git_address: str, void: str = '') -> None:
    goto_profile_dir(profile)

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

    if os.path.isfile('data') == False:
        with open('data', 'wb') as file:
            file.write(emptyenc)

    if os.path.isfile('adds') == False:
        with open('adds', 'wb') as file:
            file.write(emptyenc)

    if os.path.isfile('removals') == False:
        with open('removals', 'w') as file:
            file.write('')

def create_profile(git_address: str, void: str = '') -> str:
    init()
    newuuid: str = gen_uuid()
    create_profile_data(newuuid, git_address)
    return newuuid

def get_data(profile) -> list:
    create_profile_data(profile, '', '')

    with open('key', 'rb') as file:
        key: bytes = file.read()
    enc = Fernet(key)

    with open('data', 'rb') as file:
        databytes: bytes = file.read()

    datajson = enc.decrypt(databytes).decode()
    data: list = json.loads(datajson)

    with open('adds', 'rb') as file:
        addsbytes: bytes = file.read()

    addsjson: str = enc.decrypt(addsbytes).decode()
    adds: list = json.loads(addsjson)

    with open('removals', 'r') as file:
        removalsstr: str = file.read()
    removals: list = removalsstr.split('\n')

    for i in range(len(adds)):
        data.append(adds[i])

    for i in range(len(removals)):
        for j in range(len(data)):
            if data[j]['uuid'] == removals[i]:
                del data[j]
                break

    return data

def add_dict(profile: str, data: dict) -> None:
    data['uuid'] = gen_uuid()

    create_profile_data(profile, '', '')

    with open('key', 'rb') as file:
        key: bytes = file.read()
    enc = Fernet(key)

    with open('adds', 'rb') as file:
        addsbytes: bytes = file.read()

    addsjson: str = enc.decrypt(addsbytes).decode()
    adds: list = json.loads(addsjson)

    adds.append(data)

    addsjson: str = json.dumps(adds)
    addsbytes: bytes = enc.encrypt(addsjson.encode())

    with open('adds', 'wb') as file:
        file.write(addsbytes)

def remove_dict(profile: str, dict_uuid: str) -> None:
    create_profile_data(profile, '', '')

    with open('removals', 'r') as file:
        removalsstr: str = file.read()
    removals: list = removalsstr.split('\n')

    removals.append(dict_uuid)

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
        databytes: bytes = file.read()

    datajson = enc.decrypt(databytes).decode()
    data: list = json.loads(datajson)

    for i in range(len(adds)):
        data.append(adds[i])

    for i in range(len(removals)):
        for j in range(len(data)):
            if data[j]['uuid'] == removals[i]:
                del data[j]
                break

    datajson: str = json.dumps(data)
    databytes: bytes = enc.encrypt(datajson.encode())

    with open(profile, 'wb') as file:
        file.write(databytes)

    repo.index.add([profile])
    repo.index.commit('[SSO] Synced data with client.')

    origin = repo.remote(name='origin')
    origin.push()

    goto_profile_dir(profile)

    if os.path.exists('temp-repo') == True:
        shutil.rmtree('temp-repo')

    with open('adds', 'wb') as file:
        file.write(emptyenc)

    with open('removals', 'wb') as file:
        file.write(emptyenc)

    with open('data', 'wb') as file:
        file.write(databytes)

def gen_uuid() -> str:
    while True:
        newuuid: str = str(uuid.uuid4())
        if os.path.isdir(newuuid) == False:
            break
    return newuuid

def get_profiles() -> list:
    init()
    path = get_appdata_path()
    profiles = [ name for name in os.listdir(path) if os.path.isdir(os.path.join(path, name)) ]
    return profiles

def set_git_address(profile: str, git_address: str) -> None:
    init()

    if os.path.isdir(profile) == False:
        os.mkdir(profile)
    os.chdir(profile)

    with open('repo', 'w') as file:
        file.write(git_address)

def get_appdata_path() -> str:
    appdatapath: str = platformdirs.user_data_dir("safelysaveonline")
    return appdatapath

def init() -> None:
    if os.path.isdir(get_appdata_path()) == False:
        os.makedirs(get_appdata_path())
    os.chdir(get_appdata_path())

def goto_profile_dir(profile) -> None:
    init()

    if os.path.isdir(profile) == False:
        os.mkdir(profile)
    os.chdir(profile)
