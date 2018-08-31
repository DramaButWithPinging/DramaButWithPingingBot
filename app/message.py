# File message.py
# Description: Message response logic

import logger

import json
import os
import random
from pathlib import Path

# Setup logging
log = logger.get_logger("MessageCenter")

class MessageCenter(dict):
    """
    Loads and contains the lists of possible message responses for posting
    """
    
    instances = {}
    def __new__(cls, *args, **kwargs):
        """Singleton"""
        log.debug(f"In {cls.__name__}.__new__()")
        if not cls.instances:
            log.debug(f"First call to singleton {cls.__name__} - creating instance")
            cls.instances[cls] = super().__new__(cls)
            cls.instances[cls].dirs = []
        return cls.instances[cls]
    
    def __init__(self, path_dir=None):
        """Load files from path_dir if passed and seed RNG for self.get_random()"""
        random.seed()
        if path_dir: self.load(file_dir)
        return
    
    def load(self, path_dir):
        """Load all message JSON files in file_dir and unpack them into self (dict)"""
        log.info(f"Attempting to load message files from {path_dir}")
        # Make sure it's a valid directory
        if not path_dir.is_dir():
            log.exception(f"Unable to load message files - {path_dir} is not a directory")
            raise ValueError
        if not (path_dir in self.dirs):
            log.debug(f"{path_dir} is new - adding to directory list")
            self.dirs.append(path_dir)
        # Iterate recursively through path_dir and return all .json files
        for file in path_dir.rglob("*.json"):
            log.info(f"Found file {file} - attempting to import")
            with file.open("r") as f:
                self[file.stem] = json.load(f)
        log.info(f"Finished importing from {path_dir}")
        return
    
    def reload(self):
        """Call self.load() on each path_dir in self.dirs"""
        log.info(f"Attempting to reload message files from all stored directories")
        for path_dir in self.dirs:
            self.load(path_dir)
        return
    
    def get_random(self, *args):
        """Get a random message from dict at args keys. get_random("x", "y") pulls random quote from dict at self['x']['y']"""
        # Go to our initial starting point based on args
        log.debug(f"Attempting to get a random message - args: {args}")
        loc = self
        for i in args:
            loc = loc[i]
        # Now randomly progress until we find a string - not a dict
        while True:
            if isinstance(loc, str): break # we've found our message
            try:
                loc = loc[random.choice(list(loc.keys()))]
            except IndexError:
                log.exception("Error finding random message - likely an empty dict in message files")
                return self['main']['wentwrong'] # something went wrong
        return loc
    
    