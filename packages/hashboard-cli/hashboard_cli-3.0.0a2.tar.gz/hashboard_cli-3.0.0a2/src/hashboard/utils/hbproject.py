from pathlib import Path
from typing import Union
import os

from hashboard.utils.json_file import read_json_file, write_json_file, write_json_key

HASHBOARD_PROJECT_FILE_NAME = ".hbproject"
DBT_ROOT_KEY = "dbt_root"
DEFAULT_BUILD_ID_KEY = "most_recent_build_id"
MAX_DEFAULT_BUILD_SECS = 3600  # One hour

def create_hashbord_root():
    with open(HASHBOARD_PROJECT_FILE_NAME, "a"):
        pass

def read_hashboard_project_value(key: str):
    root = get_hashboard_root_dir()
    if root is None:
        return None
    filepath = root / HASHBOARD_PROJECT_FILE_NAME
    values = read_json_file(filepath)
    return values.get(key, None)

def write_hashboard_project_value(key: str, value):
    root = get_hashboard_root_dir()
    if root is None:
        return
    filepath = root / HASHBOARD_PROJECT_FILE_NAME
    write_json_key(filepath, key, value)

def get_hashboard_root_dir() -> Union[Path, None]:
    current_path = os.getcwd()

    # Arbitrary limit to prevent searching for too long
    for _ in range(100):
        try:
            # List all files in the current directory
            for filename in os.listdir(current_path):
                if filename == HASHBOARD_PROJECT_FILE_NAME:
                    return Path(current_path)

            # Move to the parent directory
            parent_path = os.path.dirname(current_path)

            # If we've reached the root directory, stop
            if parent_path == current_path:
                break
            current_path = parent_path
        except PermissionError:
            return None
    return None
