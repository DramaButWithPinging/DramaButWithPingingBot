# File: backup.py
# Description: Utility to backup file - for now mainly message_dict.py (all our messages)

import logging
import os
import shutil
import sys
import time
from pathlib import Path

# Should implement logging
# Could implement cleanup(file) which removes all backups but most recent

def backup(file):
    """Backups up libpath.Path file to appropriate filename in local directory ./.backups"""
    backup_stem_suffix = "-{}.{}.{}" # How our backups will look file.stem+backup_stem_suffix+[(number)].file.suffix.backup
    backup_dir_name = ".backups" # Name of local backups directory
    backup_path = file.parent / backup_dir_name
    if not backup_path.is_dir(): backup_path.mkdir() # make backup directory if needed
    t = time.localtime()
    bss = backup_stem_suffix.format(t.tm_year, t.tm_mon, t.tm_mday)
    # File might exist if backing up more than once an hour (why?!)
    matches = backup_path.glob(f"*{file.stem}{bss}*")
    match_count = len(list(matches))
    # Append appropriate number in parens if needed
    mat_str = ''
    if match_count: mat_str = f"-{match_count}"
    # Should have an appropriate backup file now
    backup_file = backup_path / f"{file.stem}{bss}{mat_str}{file.suffix}.backup"
    print(f"Backing up {file} to {backup_file}...")
    shutil.copy(str(file), str(backup_file)) # Copy file to backup location
    return
    
    
if __name__ == '__main__':
    cwd = Path(os.getcwd())
    print(f"Backing up files: {', '.join(sys.argv[1:])}")
    for i in range(1, len(sys.argv)):
        backup((cwd / Path(sys.argv[i])).resolve())
    
    