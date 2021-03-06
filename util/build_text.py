# File build_text.py
# Description: Generates and saves JSON files to be read later and used to build responses to posts

# Start import setup - think of better way
import sys
from pathlib import Path
sys.path.insert(1, str(Path(sys.path[0]).parent))
# End import setup

import app.logger as logger

import json

# Setup logging
log = logger.get_logger("MessageSetup")


def save_files(msgs):
    file_root = Path(sys.path[1]) / "text" # need to update this
    log.info(f"Attempting to build and save message files in directory {file_root}")
    for file, text in msgs.items():
        log.info(f"Attempting to write to {file_root}/{file}.json")
        with Path(file_root / f"{file}.json").open("w") as f:
            log.info(f"File open - attempting to dump JSON")
            json.dump(text, f)
    
    
    return

##### MESSAGES #####
import text.message_dict

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
    log.info(f"build_text.py running as __main__")
    save_files(text.message_dict.messages)