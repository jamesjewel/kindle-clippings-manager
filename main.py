#!/usr/bin/env python3

# TODO Import selectively?
import re
import time
import os
import clip
import library

# Global variables
LIBPATH = './clippings-library/'
FILEDIR = './'
FILENAME = 'My Clippings.txt'

CLIPPING_END_STRING = '=' * 10

# See if library exists in path
lib = ''
try:
    lib = library.get_library(LIBPATH)
    print('Library found:', lib.get_clip_count(), 'clips')
except FileNotFoundError:
    print('Library doesn\'t exist at', os.path.abspath(LIBPATH))
    choice = input('Create new library here? [y/N] ')
    if choice.lower() == 'y':
        os.mkdir(LIBPATH)   # Create library
        lib = library.get_library(LIBPATH)
        print('Library initialized.')
    else:
        exit(1)

# Read the source file
# Open the file, read the data line by line into a list
try:
    file = open(FILEDIR + FILENAME, 'r', encoding = 'utf-8')
except FileNotFoundError:
    print('Error: The file', FILEDIR + FILENAME, 'does not exist.')
    exit(1)
lines = file.readlines()
if len(lines) == 0:
    print('Error: The file', FILEDIR + FILENAME, 'is empty.')
    exit(1)
file.close()

# Functions for the main program
# Parses a block of clipping to get information
def parse_block(cliplines):
    # line 1: Book info
    curline = cliplines[0].lstrip('\ufeff').rstrip('\n')
    p = re.compile(r'(?P<title>[\S ]+) \(?P<author>([\S ]+)\)')
    res = p.match(curline)
    title = res.group('title')
    author = res.group('author')

    # line 2: Metadata
    curline = cliplines[1].strip()
    # TEST Name the regular expression
    p = re.compile(r"- Your (?P<type>Highlight|Note|Bookmark) " \
                    "(on|at) (?P<postype>location|page) " \
                    "(?P<posx>\d+)(-?(?P<posy>\d+))?" \
                    "( \| location (?P<locx>\d+)(-?(?P<locy>\d+))?)? \| " \
                    # Getting the timestamp
                    "Added on (?P<wday>[a-zA-Z]{3})[a-zA-Z]{,3}day, " \
                    "(?P<day>\d{1,2}) (?P<month>[a-zA-Z]{3})[a-zA-Z]+ " \
                    "(?P<year>\d{4}) (?P<hr>\d\d):(?P<min>\d\d):(?P<sec>\d\d)")
    res = p.match(curline)
    # getting clipping type
    ctype = res.group('type').lower()
    # getting position data
    # TODO: A possible alternative to 'None'
    if res.group('postype') == 'location':
        loc = [res.group('posx'), res.group('posy')]
        page = [None, None]
    elif res.group('postype') == 'page':
        page = [res.group('posx'), res.group('posy')]
        loc = [res.group('locx'), res.group('locy')]
    # extracting timestamp
    # strptime('Fri Mar 01 23:38:40 2019')
    timestring = '{weekday} {month} {day} {hour}:{minute}:{second} {year}'
    timestring = timestring.format(weekday=res.group('wday'), \
                                   month=res.group('month'), \
                                   day=res.group('day'), \
                                   hour=res.group('hr'), \
                                   minute=res.group('min'), \
                                   second=res.group('sec'), \
                                   year=res.group('year'))
    # creating the time object
#   timeobj = time.strptime(timestring)
#   if res != None:
#       print(res.groups())
    # line 3: Highlight
    curline = cliplines[3].strip()
    text = curline
    clipobj = clip.Clip(title, author, text, ctype, timestring, loc, page)
    return clipobj

count = 0
startline = 0
stopline = 0

cliplist = []
for index, line in enumerate(lines):
    if line.rstrip() == CLIPPING_END_STRING:
        count = count + 1
        stopline = index
        cliplist.append(parse_block(lines[startline:stopline]))
        startline = stopline + 1

if len(cliplist) == 0:
    print('No clips found in the file. Nothing to do.')

# Add clips to library
for clip in cliplist:
    lib.add_clip(clip)

# Print update status
count = lib.get_new_clip_count()
if count == 0:
    print('No new clips to add.')
    exit(1)
else:
    print('File has', count, 'new clips.')
# Ask for confirmation
choice = input('Update library? [Y/n] ')
# Update library
if choice.lower() == 'y':
    lib.write()
    print('Done.')
