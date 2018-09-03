# File: crosspost.py
# Description: Handles our crossposting logic

import history
import logger

import praw

import datetime
import random
import re

# Setup logging
log = logger.get_logger("Crosspost")


#this file needs better logging

# better way in future
def not_re_search(*args, **kwargs):
    return not re.search(*args, **kwargs)
    
class FilterRule(dict):
    """ """
    def __init__(self, key, val, atr, cmp):
        """ """
        super().__init__()
        self[key] = {
            "val": val,
            "atr": atr,
            "cmp": cmp }
        return

class CrosspostFilter:
    """Defines a filter for crossposting"""
    
    def __init__(self, **kwargs):
        """
        this needs updating
        -------
        max_uv = inclusive max upvotes allowed (None as expected)
        min_uv = inclusive min upvotes allowed (None as expected)
        max_age = inclusive max age allowed (None as expected)
        min_age = inclusive minimum age allowed (None as expected)
        yes_src = must match a src in list (None means not required)
        no_src = must not match a src in list (None means not required)
        sticky = bool if true must be stickied if false doesn't matter
        no_sticky = bool if true can't be a sticky if false doesn't matter
        """
        # Comparison should be such that cmp(val, post["atr"]) true means filtered
        self.filter_rules = {}
        self.default_filter_rules = {
            **FilterRule("max_uv", None, "score", lambda x,y: x < y),
            **FilterRule("min_uv", None, "score", lambda x,y: x > y),
            **FilterRule("max_age", None, "created_utc", lambda x,y: x > y),
            **FilterRule("min_age", None, "created_utc", lambda x,y: x < y),
            **FilterRule("yes_url", None, "url", lambda x,y: not re.search(x, y)),
            **FilterRule("not_url", None, "url", lambda x,y: re.search(x, y)),
            **FilterRule("yes_domain", None, "domain", lambda x,y: not re.search(x, y)),
            **FilterRule("not_domain", None, "domain", lambda x,y: re.search(x, y)),
            **FilterRule("sticky", False, "stickied", lambda x,y: x != y),
            **FilterRule("not_sticky", False, "stickied", lambda x,y: x == y),
            **FilterRule("max_comment", None, "num_comments", lambda x,y: x < y),
            **FilterRule("min_comment", None, "num_comments", lambda x,y: x > y),
            **FilterRule("yes_title", None, "title", lambda x,y: not re.search(x, y)),
            **FilterRule("not_title", None, "title", lambda x,y: re.search(x, y)),
            **FilterRule("over_18", False, "over_18", lambda x,y: x == y),
            **FilterRule("archived", False, "archived", lambda x,y: x == y),
            **FilterRule("yes_author", None, "author", lambda x,y: not re.search(x, y.name)),
            **FilterRule("not_author", None, "author", lambda x,y: re.search(x, y.name)),
            **FilterRule("yes_self", False, "is_self", lambda x,y: x != y),
            **FilterRule("not_self", False, "is_self", lambda x,y: x == y),
            **FilterRule("ids", None, "id", lambda x,y: y in x) }
        for key, value in kwargs.items():
            if key not in self.default_filter_rules.keys():
                log.exception(f"Unknown {self.__class__.__name__} keyword {key}")
                raise KeyError
            self.filter_rules[key] = self.default_filter_rules[key]
            self.filter_rules[key]['val'] = value
        return
    
    def __str__(self):
        return str(self.filter_rules)
    
    def update_rules(self, **kwargs):
        """ """
        for key, value in kwargs.items():
            if key not in self.default_filter_rules.keys():
                log.exception(f"Unknown {self.__class__.__name__} keyword {key}")
                raise KeyError
            self.filter_rules[key] = self.default_filter_rules[key]
            self.filter_rules[key]['val'] = value
        return
    
    def reject(self, post):
        """ """
        reject = []
        for key, rule in self.filter_rules.items():
            #current = self.filter_rules[key]
            if not rule['val']:
                continue # None or False means no filter test
            comp = rule['cmp']
            post_atr = post.__getattribute__(rule['atr'])
            if comp(rule['val'], post_atr):
                log.debug(f"Filtering {post} because {key}: {comp}({rule['val']}, post.{atr})")
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
        self.filters.extend(list(fltr_list))
        self.retrieved_posts = [] # posts retrieved pre-filtering
        self.filter_reasons = {} # form -  post: [ (filter1, [reason1, reason2]) , (filter2, [reason1, reason2, reason3, ...]), ... ]
        self.posts = []
        return
    
    def get_posts(self, count=100, sort_style="new"):
        """ """
        # get count # of posts from self.src and put in self.retrieved_posts'
        
        #fresh copy for now
        self.retrieved_posts = []
        self.filter_reasons = {}
        self.posts = []
        
        self.retrieved_posts = list(getattr(self.src, sort_style)(limit=count))
        for post in self.retrieved_posts:
            log.debug(f'Looking at post "{post.title}...')
            self.filter_reasons[post] = []
            for filter in self.filters:
                log.debug(f'Applying filter {filter}')
                filter_reasons = filter.reject(post)
                if filter_reasons:
                    log.debug(f"Filtering post titled {post.title} because of {filter_reasons}\n")
                    self.filter_reasons[post].append((filter, filter_reasons))
            if not self.filter_reasons[post]:
                # Not filtered pass it on
                log.debug(f'Post: "{post.title}" passed through filters')
                self.posts.append(post)
        return
    
    def add_filters(self, fltr_list):
        """ """
        self.filters.extend(list(fltr_list))
        return
    
    # remove filters?
    
    def sort_posts(self, attr="score", rvrs=True):
        """ """
        self.posts.sort(key=lambda x: x.__getattribute__(attr), reverse=rvrs)
        return
    
    def random_sort(self):
        random.seed()
        random.shuffle(self.posts)
        return
    
    def post(self):
        # check if already exists
        the_post = None
        dup_ids = []
        for p in self.posts:
            dups = list(p.duplicates())
            if self.dest.display_name not in [dups[x].subreddit.display_name for x in range(len(dups))]:
                the_post = p
                break # We're good
            dup_ids.append(p.id)
            log.debug(f"Post: {p.title} already posted in r/{self.dest}")
        if not the_post:
            log.exception("Couldn't find a valid crosspost")
            raise "Something went wrong"
        new_title = f'(x-post r/{self.src}) "{the_post.title}"'
        if len(new_title) > 300:
            new_title = f'{new_title[:295]}..."'
        log.info(f"Crossposting from r/{self.src} -> r/{self.dest}:\nTitle: {new_title}")
        #new_post = self.dest.submit(new_title, url=the_post.url, resubmit=False, send_replies=False)
        new_post = the_post.crosspost(self.dest, new_title, send_replies=False)
        return (the_post, new_post, dup_ids)
    

    
    
    
        