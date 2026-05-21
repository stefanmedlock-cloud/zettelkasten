import sys
from .unix import UnixFileLock
from .windows import WindowsFileLock

def get_file_lock(filepath: str):
    if sys.platform.startswith("win"):
        return WindowsFileLock(filepath)
    return UnixFileLock(filepath)
