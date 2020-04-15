#!/usr/bin/env python

# Imports
import re
import json

## CONFIGURATION
## Change these variables to configure the program
FILENAME = "My Clippings.txt"
CLIPPING_END_STRING = "=========="

# Global Variables
fileDir = "./" # End with a /
lines = []

# Open the file, read the data line by line into a list
file = open(fileDir + FILENAME, "r")
lines = file.readlines()
file.close()

# Parsing text
curLine = 0
startLine = 0
stopLine = 0

count = 0

class Clip:
    """The clipping class definitio n"""
    def __init__(self, _title, _author, _text, _time):
        self.title = _title
        self.author = _author
        self.text = _text
        self.time = _time

    def printClip(self):
        print("Title:", self.title)
        print("Author:", self.author)
        print("Text:", self.text)


# Parses a block of clipping to get information
def parseBlock(startLine, stopLine):
   # line 1: Book info
   curLine = lines[startLine].strip()
   p = re.compile(r"([\s\S]+)\(([\s\S]+)\)")
   res = p.match(curLine)
   clipObj = Clip("","","","")
   if res != None:
       clipObj.title = res.group(1).strip()
       clipObj.author = res.group(2).strip()
   # line 2: Metadata
   curLine = lines[startLine+1].strip()
   p = re.compile(r"- Your (Highlight|Note|Bookmark) (on|at) (location|page) " \
                   "(\d+)(-?)(\d*)( \| location (\d+)(-?)(\d*))? \| " \
                   "Added on ([a-zA-Z]{3})[a-zA-Z]{,3}day, (\d{1,2}) " \
                   "([a-zA-Z]{3})[a-zA-Z]+ (\d{4}) (\d\d):(\d\d):(\d\d)")
   res = p.match(curLine)
   # extracting timestamp
   # strptime('Fri Mar 01 23:38:40 2019')
   timestring = '{weekday} {month} {day} {hour}:{minute}:{second} {year}'
   timestring = timestring.format(weekday=res.group(11), month=res.group(13), \
                                  day=res.group(12), \
                                  hour=res.group(15), minute=res.group(16), \
                                  second=res.group(17), \
                                  year=res.group(14))
   print(timestring)
   #if res != None:
    #   print(res.groups())
   # line 3: Highlight
   curLine = lines[startLine + 3].strip()
   clipObj.text = curLine
#  print(clipObj)
#  clipObj.printClip()
# The main program begins here:
for index, line in enumerate(lines):
#   print("{}: {}".format(index, line))
    if line.rstrip() == CLIPPING_END_STRING:
        count = count + 1
#       print(count)
        stopLine = index
        parseBlock(startLine, stopLine)
        startLine = stopLine + 1

