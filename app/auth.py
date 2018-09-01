# File: auth.py
# Description: Handles loading and passing credentials to PRAW from a file

import logger

from pathlib import Path

log = logger.get_logger("Auth")

class AuthDict(dict):
    """
    Used to pass Reddit login credentials as keyword arguments to PRAW.
    
    Usage: **AuthDict
    """
    
    def __init__(self, username, password, client_id, client_secret, user_agent):
        """Init with the five needed credentials as strings"""
        # First call super() to init dict
        super()
        log.info(f"Initializing {self.__class__.__name__} for /u/{username}")
        # Now store params as key:value pairs in self (dict)
        self['username'] = username
        self['password'] = password
        self['client_id'] = client_id
        self['client_secret'] = client_secret
        self['user_agent'] = user_agent
        return
    
class AuthFile:
    """
    Read Reddit login credentials from file and store as self.keys = AuthDict.
    
    File format must be:
    username
    password
    client_id
    client_secret
    user_agent
    --EOF--
    
    Newlines seperate items
    """
    
    count = 5 # Expected number of values to import
    
    def __init__(self, file):
        """Read credentials from file. Store in AuthDict object"""
        file = Path(file) # for case of string
        if not file.is_file():
            log.exception(f"Could not load credentials - {file} is not a file")
            raise FileNotFoundError
        log.info(f"Attempting to read credential file {file}")
        with file.open("r") as f:
            log.debug(f"Reading lines from file")
            lines = [] # Store the lines in a list
            for line in f:
                stripped = line.rstrip() # Strip whitespace
                if stripped: lines.append(stripped)  # Don't add blank lines
        # Make sure we got the right amount of values
        if len(lines) != AuthFile.count:
            log.exception(f"Error: read {len(lines)} values from input file '{file}'. {self.__class__.__name__} expects {AuthFile.count}. Please check file.")
            raise Exception
        # Pass the lines to AuthDict
        self.keys = AuthDict(*lines)
        log.info("Done loading credentials")
        return
    
    
        