#!/usr/bin/python
import sys

import reader

if __name__ == '__main__':
    """Run the program for stdin or file input. Output to stdout."""
    import fileinput
    sumitup = reader.Summer()
    for line in fileinput.input(): print sumitup.readline(line)
