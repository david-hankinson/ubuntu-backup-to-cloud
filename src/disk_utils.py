import os
from pathlib import Path

def get_home_path():
    return str(Path.home())

EXCLUDE_DIRS = {'.cache', '.local', '.venv', '.git', 'node_modules', 'Downloads', 'anaconda3', 'anaconda_projects'}

def get_dir_size(path):
    total = 0
    try:
        with os.scandir(path) as entries:
            for entry in entries:
                if entry.is_symlink() or entry.name.startswith('.') or entry.name in EXCLUDE_DIRS:
                    continue
                if entry.is_file():
                    total += entry.stat().st_size
                elif entry.is_dir():
                    total += get_dir_size(entry.path)
    except (PermissionError, OSError):
        pass 
    return total

def format_size(size_bytes):
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size_bytes < 1024:
            return f"{size_bytes:7.2f} {unit}"
        size_bytes /= 1024

def analyze_home():
    home = Path.home()
    report = {}

    print(f"--- Analyzing: {home} ---")
    
    # Scan only the top-level directories in Home
    with os.scandir(home) as entries:
        for entry in entries:
            if entry.is_dir() and not entry.name.startswith('.'):
                print(f"Scanning {entry.name}...")
                size = get_dir_size(entry.path)
                report[entry.name] = size

    # Sort by size (value) descending
    sorted_report = sorted(report.items(), key=lambda item: item[1], reverse=True)

    print("\n--- Top 10 Largest Folders ---")
    for name, size in sorted_report[:10]:
        print(f"{format_size(size)} | {name}")

if __name__ == "__main__":
    analyze_home()