import os
import uuid

def is_valid_uuid(newuuid: str) -> bool:
    try:
        uuid.UUID(newuuid)
        return True
    except ValueError:
        return False

def gen_uuid() -> str:
    while True:
        newuuid: str = str(uuid.uuid4())
        if os.path.isdir(newuuid) == False:
            break
    return newuuid
