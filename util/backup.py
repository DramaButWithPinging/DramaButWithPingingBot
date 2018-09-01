# File: backup.py
# Description: Utility to backup file - for now mainly message_dict.py (all our messages)

# Start import setup - think of better way
import sys
from pathlib import Path
sys.path.insert(1, str(Path(sys.path[0]).parent))
# End import setup

import app.logger as logger

import os
import shutil
import sys
import time
from pathlib import Path

# Setup logging
log = logger.get_logger("Backup")

# Could implement cleanup(file) which removes all backups but most recent

def backup(file):
    """Backups up libpath.Path file to appropriate filename in local directory ./.backups"""
    file = Path(file) # in case of string
    backup_stem_suffix = "-{}.{}.{}" # How our backups will look file.stem+backup_stem_suffix+[-number].file.suffix.backup
    backup_dir_name = ".backups" # Name of local backups directory
    backup_path = file.parent / backup_dir_name
    log.info(f"Attempting to backup {file} to directory {backup_path}")
    if not backup_path.is_dir():
        log.info(f"Directory {backup_path} does not exist - attempting to create")
        backup_path.mkdir()
    t = time.localtime()
    bss = backup_stem_suffix.format(t.tm_year, t.tm_mon, t.tm_mday)
    # File might exist if backing up more than once an hour (why?!)
    matches = backup_path.glob(f"*{file.stem}{bss}*")
    match_count = len(list(matches))
    # Append appropriate number in parens if needed
    mat_str = ''
    if match_count:
        log.info(f"Backup already exists with name {file.stem}{bss}{file.suffix}.backup")
        mat_str = f"-{match_count}"
    # Should have an appropriate backup file now
    backup_file = backup_path / f"{file.stem}{bss}{mat_str}{file.suffix}.backup"
    log.info(f"Backing up {file} to {backup_file}")
    shutil.copy(str(file), str(backup_file)) # Copy file to backup location
    return
    
    
if __name__ == '__main__':
    cwd = Path(os.getcwd())
    log.info(f"backup.py running as __main__")
    log.info(f"Backing up files: {', '.join(sys.argv[1:])}")
    for i in range(1, len(sys.argv)):
        file = (cwd / Path(sys.argv[i])).resolve()
        log.info(f"Attempting to backup {file}")
        backup(file)
    
    