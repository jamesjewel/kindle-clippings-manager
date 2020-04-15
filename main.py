#!/usr/bin/env python

# Imports
import re
import time
import json

## CONFIGURATION
## Change these variables to configure the program
FILENAME = "My Clippings.txt"
CLIPPING_END_STRING = "=========="

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
        self.time = _time
        self.loc = {}
        self.page = {}
        self.loc['x'] = _loc[0]
        self.loc['y'] = _loc[1]
        self.page['x'] = _page[0]
        self.page['y'] = _page[1]

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
    curLine = lines[startLine].strip()
    p = re.compile(r"([\s\S]+)\(([\s\S]+)\)")
    res = p.match(curLine)
    if res != None:
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
    ctype = res.group(1)
    # getting position data
    # integer conversion
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
    clipObj = Clip(title, author, text, ctype, timeObj, loc, page)
    return clipObj.__dict__

# The main program begins here:
# Open the file, read the data line by line into a list
file = open(fileDir + FILENAME, "r")
lines = file.readlines()
file.close()

curLine = 0
startLine = 0
stopLine = 0
count = 0

clipList = []
for index, line in enumerate(lines):
#   print("{}: {}".format(index, line))
    if line.rstrip() == CLIPPING_END_STRING:
        count = count + 1
#       print(count)
        stopLine = index
        clipList.append(parseBlock(startLine, stopLine))
        startLine = stopLine + 1

print(clipList)
jsonString = json.dumps(clipList, indent=4, sort_keys=False)

file = open(fileDir + "My Clippings.json", "w")
file.write(jsonString)
file.close()
