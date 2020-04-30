#!/usr/bin/env python3

import clip
import library

# Global variables
LIBPATH = './clippings-library/'
FILEDIR = './'
FILENAME = 'My Clippings.txt'

CLIPPING_END_STRING = '=' * 10

# See if library exists in path
try:
    lib = library.get_library(LIBPATH)
except FileNotFoundError:
    print('Library doesn\'t exist at', os.path.abspath(LIBPATH))
    choice = input('Create new library here? [y/N] ')
    if choice.lower() == 'y':
        os.mkdir(LIBPATH)   # Create library
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

curLine = 0
count = 0
startline = 0
stopline = 0

cliplist = []
for index, line in enumerate(lines):
    if line.rstrip() == CLIPPING_END_STRING:
        count = count + 1
        stopline = index
        cliplist.append(parseBlock(startline, stopline).getClip())
        startline = stopline + 1

if len(cliplist) == 0:
    print('No clips found in the file. Nothing to do.')


#for aclip in lib.clips:
#    print(aclip.__dict__)
