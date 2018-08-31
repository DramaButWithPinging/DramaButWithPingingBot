# File setup.py
# Description: Generates and saves JSON files to be read later and used to build responses to posts

# Start import setup - think of better way
import sys
from pathlib import Path
sys.path.insert(1, str(Path(__file__).parents[1]))
# End import setup

import app.log as log

import json

def save_files(msgs):
    file_root = sys.path[0] # store files where setup.py is located
    for file, text in msgs.items():
        with open(f"{file_root}/{file}.json", "w") as f:
            json.dump(text, f)
    
    
    return

##### MESSAGES #####
import message_dict

# message_dict.py kept seperate and added to .gitignore to remove customization
# message_dict.py has structure:
# messages = {}
# messages['main'] = {
#    "example": "text1",
#    "example2": "text2" }
#
# messages['quotes'] = { "example3": "text3" }
# messages['quotes']['/r/subreddit'] = {
#    "source": "another quote",
#    "another": "quote2" }
#
# ...etc...


if __name__ == '__main__':
    save_files(message_dict.messages)