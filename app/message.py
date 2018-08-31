# File message.py
# Description: Message response logic

import logger

import json
import os
import random
from pathlib import Path

class MessageCenter(dict):
    """
    Loads and contains the lists of possible message responses for posting
    """
    
    instances = {}
    def __new__(cls, *args, **kwargs):
        """Singleton"""
        if not cls.instances:
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
        # Make sure it's a valid directory
        if not path_dir.is_dir():
            #Logging code goes here
            raise ValueError
        if not (path_dir in self.dirs): self.dirs.append(path_dir)
        # Iterate recursively through path_dir and return all .json files
        for file in path_dir.rglob("*.json"):
            with file.open("r") as f:
                self[file.stem] = json.load(f)
        return
    
    def reload(self):
        """Call self.load() on each path_dir in self.dirs"""
        for path_dir in self.dirs:
            self.load(path_dir)
        return
    
    def get_random(self, *args):
        """Get a random message from dict at args keys. get_random("x", "y") pulls random quote from dict at self['x']['y']"""
        # Go to our initial starting point based on args
        loc = self
        for i in args:
            loc = loc[i]
        # Now randomly progress until we find a string - not a dict
        while True:
            if isinstance(loc, str): break # we've found our message
            try:
                loc = loc[random.choice(list(loc.keys()))]
            except IndexError:
                return "Error accessing message - something went wrong"
        return loc
    
    