#!/usr/bin/env python3

import clip
import library

# Global variables
LIBPATH = './clippings-library/'

# See if library exists in path
try:
    lib = library.get_library(LIBPATH)
except FileNotFoundError:
    print('Library doesn\'t exist at ', LIBPATH)
    choice = input("Create new library here? [y/N] ")
    if lower(choice) == 'y':
        os.mkdir(LIBPATH)
    # Create it
    exit(1)
print(lib.libpath)

9
#for aclip in lib.clips:
#    print(aclip.__dict__)
