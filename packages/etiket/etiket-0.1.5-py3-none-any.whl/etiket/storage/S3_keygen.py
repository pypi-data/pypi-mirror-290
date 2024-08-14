import uuid
import datetime

def generate_key(uuid : uuid.UUID, version_id : int):
    return f"{uuid}/{version_id}"

def generate_key_4_logging(username : str, file_name : str):
    return f"logs/{username}/{datetime.datetime.now().isoformat()}/{file_name}"