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

    def add_clip(self, clip):
        clips.append(clip)

    # Minor functions
    def get_clipcount():
        return len(clips)

    def add_clip(self, clip):
        self.clips.append(clip)

    def add_clips(self, cliplist):
        for clip in cliplist:
            if clip not in clips:
                self.newclips.append(clip)
        return

    def write_files():
        for clip in cliplist:
            with open('{libdir}/{filename}.txt' \
                  .format(libdir=LIBRARYDIR, \
                          filename='{} - {}'.format(clip.author, clip.title)) \
                  , 'a') as file:
                clipstring = '"' + clip.text + '"\n\n'
                clipstring += '(#{no}, '.format(no=count)
                if clip.page['x'] >= 0:
                    clipstring += 'Page {pagex}'.format(pagex=clip.page['x'])
                    if clip.page['y'] >= 0:
                        clipstring += '{sep}{pagey}, '.format(sep='-', pagey=clip.page['y'])
                    else:
                        clipstring += ', '
                if clip.loc['x'] >= 0:
                    clipstring += 'Loc {locx}'.format(locx=clip.loc['x'])
                    if clip.loc['y'] >= 0:
                        clipstring += '{sep}{locy}, '.format(sep='-', locy=clip.loc['y'])
                    else:
                        clipstring += ', '
                clipstring += 'Added at {timestamp})'.format(timestamp=clip.ctime)
                clipstring += '\n-----------\n\n'
                file.write(clipstring)

def get_library(libpath):
    books = os.listdir(libpath)
    libobj = Library()
    libobj.libpath = os.path.abspath(libpath)
    # Creating clip objects from the files
    for book in books:
       # Deriving author and title
       p = re.compile(r'([\S ]+) - ([\S ]+).txt')
       res = p.match(book)
       if res is not None:
           author = res.group(1)
           title = res.group(2)
       file = open(libpath + '/' + book, 'r')
       lines = file.readlines()
       startline = 0
       stopline = 0
       for index, line in enumerate(lines):
           if line.rstrip('\n') == CLIP_END_STRING:
               stopline = index
               clip = create_clip(lines[startline:stopline], author, title)
               libobj.add_clip(clip)
               startline = stopline + 2
    return libobj

# parses a file and returns a clipping object
def create_clip(cliplines, author, title):
    text = cliplines[0]
    p = re.compile(r'\(#(\d+),( Page (\d+)-?(\d+)?,)?' \
                   '( Loc (\d+)-?(\d+)?,)?' \
                   ' Added at ([a-zA-Z0-9 :]+)\)')
    res = p.match(cliplines[2])
    no = res.group(0)
    locx = res.group(6)
    locy = res.group(7)
    ctype = ''
    pagex = res.group(3)
    pagey = res.group(4)
    timestring = res.group(8)
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
