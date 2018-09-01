# File: misc.py
# Description: Miscellaneous items for project

import datetime

def delta_timestamp(origin=None, **kwargs):
    """Return timestamp of (origin + timedelta(**kwargs)). If origin=None use current UTC time"""
    # Make time delta object
    delta = datetime.timedelta(**kwargs)
    if not origin:
        # Use current time
        origin = datetime.datetime.now(datetime.timezone.utc)
    elif isinstance(origin, float):
        # Timestamp - convert
        origin = datetime.datetime.fromtimestamp(origin, datetime.timezone.utc)
    new_time = origin + delta
    return new_time.timestamp()
