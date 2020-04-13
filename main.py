#!/usr/bin/env python

# Imports
# import os

## CONFIGURATION
## Change these variables to configure the program
FILENAME = "My Clippings.txt"
CLIPPING_END_STRING = "=========="
# Global Variables
fileDir = "./" # End with a /

# Open the file, read the data as a string
file = open(fileDir + FILENAME, "r")
dataStr = file.read()
# print(dataStr)

# Parsing text
curLine = 0
startLine = 0
stopLine = 0

count = 0
file.seek(0)
lines = file.readlines()

for index, line in enumerate(lines):
#   print("{}: {}".format(index, line))
    if line.rstrip() == CLIPPING_END_STRING:
        stopLine = index
        for i in range(startLine, stopLine):
            print(lines[i], end='')
        print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
        startLine = stopLine + 1
