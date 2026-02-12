import os
from pathlib import Path

# Common directories to skip for speed and relevance
EXCLUDE_DIRS = {'.cache', '.local', '.venv', '.git'}

def get_dir_size(path):
    """
    Calculates size of a directory while skipping excluded folders 
    to prevent deep recursion and speed up the process.
    """
    total = 0
    try:
        with os.scandir(path) as it:
            for entry in it:
                # 1. Skip hidden files/folders and excluded names
                if entry.name.startswith('.') or entry.name in EXCLUDE_DIRS:
                    continue
                
                # 2. Skip Symlinks to avoid infinite loops
                if entry.is_symlink():
                    continue

                if entry.is_file():
                    total += entry.stat().st_size
                elif entry.is_dir():
                    total += get_dir_size(entry.path)
    except (PermissionError, OSError):
        # Ignore folders we can't read (system restricted)
        pass 
    return total

def get_home_path():
    return str(Path.home())