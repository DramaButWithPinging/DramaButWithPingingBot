# File: logger.py
# Description: configures logging system for run time

import logging
import logging.config
import sys

from pathlib import Path

# Turn program wide debugging on (True) or off (False)
debug_mode = False

# Setup logging directory
log_dir = Path(__file__).parents[1] / "logs"
if not log_dir.exists(): log_dir.mkdir()

def get_logger(name, handlers=["file","console","combined"]):
    """Build dictionary config and return logger made with name"""
    ### Begin Dictionary Configuration ###
    loggingConfiguration = {
        "version": 1,
        "incremental": False,
        "disable_existing_loggers": False }

    loggingConfiguration['formatters'] = {
        "default": {
            "format": "{asctime} [{msecs:03.0f}] - {name:^14} - {levelname:^8} - {message}",
            "datefmt": "%b %d %H:%M:%S",
            "style": "{" } }
    
    loggingConfiguration['handlers'] = {
        'file': {
            "class": "logging.FileHandler",
            "level": "INFO",
            "formatter": "default",
            "filename": str(log_dir / f"{name}.log") },
        'console': {
            "class": "logging.StreamHandler",
            "level": "WARNING",
            "formatter": "default",
            "stream": sys.stdout },
        'combined': {
            "class": "logging.FileHandler",
            "level": "INFO",
            "formatter": "default",
            "filename": str(log_dir / "bot.log") } }
    
    if debug_mode:
        loggingConfiguration['handlers']['debug'] = {
            "class": "logging.FileHandler",
            "level": "DEBUG",
            "formatter": "default",
            "filename": str(log_dir / f"{name}-debug.log") }
        loggingConfiguration['handlers']['combined']['level'] = "DEBUG"
        handlers.append("debug")
          
    loggingConfiguration['loggers'] = {
        str(name): {
            "level": "DEBUG",
            "propogate": False,
            "handlers" : handlers } }
    
    loggingConfiguration['root'] = { "level": "CRITICAL" }
    ### End Dictionary Configuration ###
    logging.config.dictConfig(loggingConfiguration)
    return logging.getLogger(str(name))
                        
       
    

    
    

                        