# File message.py
# Description: Message response logic

import json
import os
import random

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
    
    def __init__(self, file_dir=None):
        """Load files if passed"""
        random.seed() # Seed the RNG used in self.get_random()
        if file_dir: self.load(file_dir)
        return
    
    def load(self, file_dir):
        """Load all message JSON files in file_dir and unpack them in self.msg_dict"""
        if not (file_dir in self.dirs): self.dirs.append(file_dir)
        for root, dirs, files in os.walk(file_dir):
            for f in files:
                if not f.endswith(".json"): continue
                with open(root + f, "r") as read_file:
                    self[f[:-5]] = json.load(read_file) # remove ".json" from key value
        return
    
    def reload(self):
        """Call self.load() on each file_dir in self.dirs"""
        for file_dir in self.dirs:
            self.load(file_dir)
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
    
    