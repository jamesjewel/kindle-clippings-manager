#!/usr/bin/env python3

class Clip:
    def __init__(self, _title, _author, _text, _type, _time, _loc=[-1, -1], _page=[-1, -1]):
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
