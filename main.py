#!/usr/bin/env python

# Imports
import re
import time
import os
import json

## CONFIGURATION
## Change these variables to configure the program
FILENAME = "My Clippings.txt"
CLIPPING_END_STRING = "=========="
LIBRARYDIR = "./clippings-library"

# Global Variables
fileDir = "./" # End with a /

# Class definitions
class Clip:
    """The clipping class definition"""
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

    def getClip(self):
        clipDict = {}
        clipDict['title'] = self.title
        clipDict['author'] = self.author
        clipDict['text'] = self.text
        clipDict['type'] = self.ctype
        clipDict['location'] = self.loc
        clipDict['page'] = self.page
        clipDict['time'] = self.ctime
        return clipDict
   
    def printClip(self):
        print("Title:", self.title)
        print("Author:", self.author)
        print("Text:", self.text)
        print("Type:", self.ctype)
        print("Location:", self.loc)
        print("Page:", self.page)
        print("Time:", time.asctime(self.time))

# Parses a block of clipping to get information
def parseBlock(startLine, stopLine):
   # line 1: Book info
    curLine = lines[startLine].lstrip('\ufeff').rstrip('\n')
    p = re.compile(r'([\S ]+) \(([\S ]+)\)')
    res = p.match(curLine)
    title = res.group(1)
    author = res.group(2)

    # line 2: Metadata
    curLine = lines[startLine+1].strip()
    p = re.compile(r"- Your (Highlight|Note|Bookmark) (on|at) (location|page) " \
                    "(\d+)(-?(\d+))?( \| location (\d+)(-?(\d+))?)? \| " \
                    "Added on ([a-zA-Z]{3})[a-zA-Z]{,3}day, (\d{1,2}) " \
                    "([a-zA-Z]{3})[a-zA-Z]+ (\d{4}) (\d\d):(\d\d):(\d\d)")
    res = p.match(curLine)
    # getting clipping type
    ctype = res.group(1).lower()
    # getting position data
    temp = []
    for i in [4, 6, 8, 10]:
        if res.group(i) is not None:
            temp.append(int(res.group(i)))
        else:
            temp.append(-1)
    if res.group(3) == 'location':
        loc = [temp[0], temp[1]]
        page = [-1, -1]
    elif res.group(3) == 'page':
        page = [temp[0], temp[1]]
        loc = [temp[2], temp[3]]
    # extracting timestamp
    # strptime('Fri Mar 01 23:38:40 2019')
    timeString = '{weekday} {month} {day} {hour}:{minute}:{second} {year}'
    timeString = timeString.format(weekday=res.group(11), month=res.group(13), \
                                   day=res.group(12), \
                                   hour=res.group(15), minute=res.group(16), \
                                   second=res.group(17), \
                                   year=res.group(14))
    # creating the time object
    timeObj = time.strptime(timeString)
#   if res != None:
#       print(res.groups())
    # line 3: Highlight
    curLine = lines[startLine + 3].strip()
    text = curLine
    clipObj = Clip(title, author, text, ctype, time.asctime(timeObj), loc, page)
    return clipObj

# The main program begins here:
# Open the file, read the data line by line into a list
try:
    file = open(fileDir + FILENAME, "r", encoding = 'utf-8')
except FileNotFoundError:
    print("Error: The file", fileDir + FILENAME, "does not exist.")
    exit(1)
lines = file.readlines()
if len(lines) == 0:
    print("Error: The file", fileDir + FILENAME, "is empty.")
    exit(1)
file.close()

curLine = 0
startLine = 0
stopLine = 0
count = 0

clipList = []
clipObjList = []
for index, line in enumerate(lines):
    if line.rstrip() == CLIPPING_END_STRING:
        count = count + 1
        stopLine = index
        clipObj = parseBlock(startLine, stopLine)
        clipList.append(clipObj.getClip())
        clipObjList.append(clipObj)
        startLine = stopLine + 1

if len(clipList) == 0:
    print("No clips found in the file. Nothing to do.")

# derive the exitsting booklist from folders.
firstRunFlag = False
# check if library exists
if not os.path.exists(LIBRARYDIR):
    print("The library location does not exist ({})".format(LIBRARYDIR));
    choice = input("Create new library here? [y/N] ")
    if choice.lower() == 'y':
        firstRunFlag = True
        os.mkdir(LIBRARYDIR)
# pre-process: get info about the current library
# req: the current library be written
bookList = []
count = 0
for clip in clipObjList:
    count += 1
    if clip.title not in bookList:
        bookList.append(clip.title)
        # if new book check path exists
        if not os.path.exists(LIBRARYDIR + clip.title):
            os.mkdir('{libdir}/{subdir}'.format(libdir=LIBRARYDIR, subdir=clip.title))
    # iterate through clips add them to clipping file
    with open('{libdir}/{subdir}/{filename}.txt'.format(libdir=LIBRARYDIR, subdir=clip.title, filename='{} - {}'.format(clip.author, clip.title)), 'a+') as file:
        metastring = '"' + clip.text + '"\n\n'
        metastring += '(#{no}, '.format(no=count)
        if clip.page['x'] >= 0:
            metastring += 'Page {pagex}'.format(pagex=clip.page['x'])
            if clip.page['y'] >= 0:
                metastring += '{sep}{pagey}, '.format(sep='-', pagey=clip.page['y'])
            else:
                metastring += ', '
        if clip.loc['x'] >= 0:
            metastring += 'Loc {locx}'.format(locx=clip.loc['x'])
            if clip.loc['y'] >= 0:
                metastring += '{sep}{locy}, '.format(sep='-', locy=clip.loc['y'])
            else:
                metastring += ', '
        metastring += 'Added at {timestamp})'.format(timestamp=clip.ctime)
        metastring += '\n-----------\n\n'
        file.write(metastring)

jsonString = json.dumps(clipList, indent=3, sort_keys=False)

file = open(fileDir + "My Clippings.json", "w")
file.write(jsonString)
file.close()
