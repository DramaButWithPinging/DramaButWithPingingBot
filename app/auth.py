# File: auth.py
# Description: Handles loading and passing credentials to PRAW from a file

class AuthDict(dict):
    """
    Used to pass Reddit login credentials as keyword arguments to PRAW.
    
    Usage: **AuthDict
    """
    
    def __init__(self, username, password, client_id, client_secret, user_agent):
        """Init with the five needed credentials as strings"""
        # First call super() to init dict
        super()
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
    
    def __init__(self, file):
        """Read credentials from file passed as string. Store in AuthDict object"""
        with open(file, "r") as f:
            lines = [] # Store the lines in a list
            for line in f:
                stripped = line.rstrip() # Strip whitespace
                # Don't add blank lines
                if stripped: lines.append(stripped)
        # Make sure we got the right amount of keys
        if len(lines) != 5:
            raise Exception(f"Error: read {len(lines)} lines from input file '{file}'. {self.__class__.__name__} expects 5. Please check '{file}'")
        # Pass the lines to AuthDict
        self.keys = AuthDict(*lines)
        return
    
    
        