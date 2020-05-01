#!/usr/bin/env python3

class Clip:
    def __init__(self, _title, _author, _text, _type, _time, _loc=[None, None], _page=[None, None]):
        self.title = _title
        self.author = _author
        self.text = _text
        self.ctype = _type
        self.ctime = _time
        self.loc = {}
        self.page = {}
        self.loc['x'] = _loc[0]
        self.loc['y'] = _loc[1]
        self.page['x'] = _page[0]
        self.page['y'] = _page[1]

    def __eq__(self, other):
        self_tuple = (self.title, self.author, self.text, \
                      self.ctype, self.ctime, \
                      self.loc['x'], self.loc['y'], \
                      self.page['x'], self.page['y'])
        other_tuple = (other.title, other.author, other.text, \
                       other.ctype, other.ctime, \
                       other.loc['x'], other.loc['y'], \
                       other.page['x'], other.page['y'])
        if self_tuple == other_tuple:
            return True
        return False
