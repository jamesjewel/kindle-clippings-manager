#!/usr/bin/env python3
import os
import re
# Custom file imports
import clip

CLIP_END_STRING = '-' * 11

class Library:
    books = []
    libpath = ''
    clips = []
    newclips = []

    # Minor functions
    def get_clip_count(self):
        return len(self.clips)

    def get_new_clip_count(self):
        return len(self.newclips)

    def add_clip(self, clip):
        flag = False
        # TODO See if this can be implemented in a better way
        for lclip in self.clips:
            if lclip == clip:
                flag = True
                break
        if flag == False:
            self.newclips.append(clip)

    def write(self):
        for clip in self.newclips:
            with open('{libdir}/{filename}.txt' \
                  .format(libdir=self.libpath, \
                          filename='{} - {}'.format(clip.author, clip.title)) \
                  , 'a') as file:
                clipstring = clip.text + '\n\n'
                # TODO Add clipping number
                clipstring += '(#{no}, '.format(no=1)
                clipstring += '{ctype}, '.format(ctype=clip.ctype.capitalize())
                if clip.page['x'] is not None:
                    clipstring += 'Page {pagex}'.format(pagex=clip.page['x'])
                    if clip.page['y'] is not None:
                        clipstring += '{sep}{pagey}, '.format(sep='-', pagey=clip.page['y'])
                    else:
                        clipstring += ', '
                if clip.loc['x'] is not None:
                    clipstring += 'Loc {locx}'.format(locx=clip.loc['x'])
                    if clip.loc['y'] is not None:
                        clipstring += '{sep}{locy}, '.format(sep='-', locy=clip.loc['y'])
                    else:
                        clipstring += ', '
                clipstring += 'Added at {timestamp})'.format(timestamp=clip.ctime)
                clipstring += '\n-----------\n\n' # TODO Use multiplication notation
                file.write(clipstring)

def get_library(libpath):
    books = os.listdir(libpath)
    libobj = Library()
    libobj.libpath = os.path.abspath(libpath)
    # Creating clip objects from the files
    for book in books:
       # Deriving author and title
       p = re.compile(r'(?P<title>[\S ]+) - (?P<author>[\S ]+).txt')
       res = p.match(book)
       if res is not None:
           author = res.group('title')
           title = res.group('author')
       file = open(libpath + '/' + book, 'r')
       lines = file.readlines()
       startline = 0
       stopline = 0
       for index, line in enumerate(lines):
           if line.rstrip('\n') == CLIP_END_STRING:
               stopline = index
               clip = create_clip(lines[startline:stopline], author, title)
               libobj.clips.append(clip)
               startline = stopline + 2
    return libobj

# parses a file and returns a clipping object
def create_clip(cliplines, author, title):
    text = cliplines[0].rstrip('\n')
    p = re.compile(r'\(#(?P<no>\d+), (?P<type>[a-zA-Z]+),' \
                   '( Page (?P<pagex>\d+)-?(?P<pagey>\d+)?,)?' \
                   '( Loc (?P<locx>\d+)-?(?P<locy>\d+)?,)?' \
                   ' Added at (?P<tstamp>[a-zA-Z0-9 :]+)\)')
    res = p.match(cliplines[2])
    no = res.group('no')
    ctype = res.group('type').lower()
    locx = res.group('locx')
    locy = res.group('locy')
    pagex = res.group('pagex')
    pagey = res.group('pagey')
    timestring = res.group('tstamp')
    clipobj = clip.Clip(title, author, text, ctype, timestring, [locx, locy], [pagex, pagey])
    return clipobj


# Output clipping format
#
# "This is text of the clipping. The highlight text goes here."
#
# (#26, Page 223, Location 1034-1234, Added at Fri Jan 20, 11:25)
# --------------
#
# "This is text of the clipping. The highlight text goes here. The text just keeps getting
# bigger and bigger and bigger with no change in other aspects."
#
# (#27, Page 223, Location 1034-1234, Added at Fri Jan 20, 11:25)
# --------------
