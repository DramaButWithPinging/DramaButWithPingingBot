# File: crosspost.py
# Description: Handles our crossposting logic

import history
import logger

import praw

import datetime
import operator as op
import re

# Setup logging
log = logger.get_logger("Crosspost")

# better way in future
def not_re_search(*args, **kwargs):
    return not re.search(*args, **kwargs)
    
class FilterRule(dict):
    """ """
    def __init__(self, key, val, atr, cmp):
        """ """
        super()
        self[key] = {
            "val": val,
            "atr": atr,
            "cmp": cmp }
        return

class CrosspostFilter:
    """Defines a filter for crossposting"""
    
    def __init__(self, **kwargs):
        """
        max_uv = inclusive max upvotes allowed (None as expected)
        min_uv = inclusive min upvotes allowed (None as expected)
        max_age = inclusive max age allowed (None as expected)
        min_age = inclusive minimum age allowed (None as expected)
        yes_src = must match a src in list (None means not required)
        no_src = must not match a src in list (None means not required)
        sticky = bool if true must be stickied if false doesn't matter
        no_sticky = bool if true can't be a sticky if false doesn't matter
        """
        # Possible additions:
        # author
        # gilded
        # over_18
        # title
        # archived
        # comment count
        #
        # Comparison should be such that cmp(val, post["atr"]) true means filtered
        self.filter_rules = {
            **FilterRule("max_uv", None, "score", op.lt),
            **FilterRule("min_uv", None, "score", op.gt),
            **FilterRule("max_age", None, "created_utc", op.gt),
            **FilterRule("min_age", None, "created_utc", op.lt),
            **FilterRule("yes_url", None, "url", not_re_search),
            **FilterRule("no_url", None, "url", re.search),
            **FilterRule("yes_domain", None, "domain", not_re_search),
            **FilterRule("no_domain", None, "domain", re.search),
            **FilterRule("sticky", False, "stickied", op.ne),
            **FilterRule("no_sticky", False, "stickied", op.eq) }
        for key, value in kwargs.items():
            if key not in self.filter_rules.keys():
                log.exception(f"Unknown {self.__class__.__name__} keyword {key}")
                raise KeyError
            self.filter_rules[key]['val'] = value     
        return
    
    def update_rule(self, rule):
        """ """
        # checking?
        self.filter_rules.update(**rule)
        return
    
    def reject(self, post):
        """ """
        reject = []
        for key, value in self.filter_rules.items():
            current = self.filter_rules[key]
            if not current['val']:
                continue # None or False means no filter test
            comp = current['cmp']
            post_atr = post.__getattribute__(current['atr'])
            if comp(current['val'], post_atr):
                log.debug(f"Filtering {post} because {key}: {comp}({current['val']}, {post_atr})")
                reject.append(key)
        return reject
            

class Crossposter:
    """ """
    
    def __init__(self, reddit, from_sub, to_sub, fltr_list=[]):
        """ """
        log.info(f"Initializing new {self.__class__.__name__} for '/r/{str(from_sub)}' -> '/r/{str(to_sub)}'")
        self.reddit = reddit
        # Convert to subreddit objects if passed as strings
        if isinstance(from_sub, str): from_sub = reddit.subreddit(from_sub)
        if isinstance(to_sub, str): to_sub = reddit.subreddit(to_sub)
        self.src = from_sub
        self.dest = to_sub
        self.filters = []
        self.filters.extend(fltr_list)
        self.retrieved_posts = [] # posts retrieved pre-filtering
        self.filter_reasons = {} # form -  post: [ (filter1, [reason1, reason2]) , (filter2, [reason1, reason2, reason3, ...]), ... ]
        self.posts = []
        return
    
    def get_posts(self, count=100, sort_style="new"):
        """ """
        # get count # of posts from self.src and put in self.retrieved_posts'
        self.retrieved_posts = list(getattr(self.src, sort_style)(limit=count))
        for post in self.retrieved_posts:
            self.filter_reasons[post] = []
            for filter in self.filters:
                filter_reasons = filter.reject(post)
                if filter_reasons:
                    log.debug(f"Filtering post titled {post.name} because of {filter_reasons}")
                    self.filter_reasons[post].append((filter, filter_reasons))
            if not self.filter_reasons[post]:
                # Not filtered pass it on
                self.posts.append(post)
        return
    
    def add_filters(self, fltr_list):
        """ """
        self.filters.extend(fltr_list)
        return
    
    def post(self):
        # name manipulation?
        # pick from self.posts and post it
        # check if already exists
        pass
    
    
        