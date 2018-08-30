# File setup.py
# Description: Generates and saves JSON files to be read later and used to build responses to posts

import json

def save_files(msgs):
    for file, text in msgs.items():
        with open(f"./{file}.json", "w") as f:
            json.dump(text, f)
    
    
    return

##### MESSAGES #####
import message_dict

# message_dict.py kept seperate and added to .gitignore to remove customization
# message_dict.py has structure:
# messages = {}
# messages['main'] = { "example": "text1",
#                      "example2": "text2"
#                    }
# messages['quotes'] = { "example3": "text3" }
# messages['quotes']['/r/subreddit'] = { "source": "another quote",
#                                        "another": "quote2"
#                                      }
# ...etc...


if __name__ == '__main__':
    save_files(message_dict.messages)