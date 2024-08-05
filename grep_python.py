#!/bin/python
# Author(s) politelychaotic
# Date created 8/5/24

import argparse
import sys

line_buffer = []
counted = 0


def matcher(pattern, line):
    global counted
    if ignore_case:
        pattern = pattern.lower()
        line = line.lower()
    if pattern in line:
        if count:
            counted += 1
        line_buffer.append(line)

def inverser(pattern, line):
    global counted
    if ignore_case:
        pattern = pattern.lower()
        line = line.lower()
    if pattern not in line:
        if count:
            counted += 1
        line_buffer.append(line)

def inverse_matches(pattern, text):
    for line in text:
        inverser(pattern, line)
    if count:
        sys.stdout.write(f'{str(counted)}\n')
    else:
        sys.stdout.writelines(line_buffer)

def find_matches(pattern, text):
    for line in text:
        matcher(pattern, line)
    if count:
        sys.stdout.write(f'{str(counted)}\n')
    else:
        sys.stdout.writelines(line_buffer)
        
def find_inverse_file(pattern, filename):
    with open(filename, 'r') as f:
        for line in f.readlines():
            matcher(pattern,line)
    if count:
        sys.stdout.write(f'{str(counted)}\n')
    else:
        sys.stdout.writelines(line_buffer)

def find_matches_file(pattern, filename):
    with open(filename, 'r') as f:
        for line in f.readlines():
            matcher(pattern, line)
    if count:
        sys.stdout.write(f'{str(counted)}\n')
    else:
        sys.stdout.writelines(line_buffer)

def main():
    global ignore_case, count
    parser = argparse.ArgumentParser()
    arguments = parser.add_argument_group('Arguments')
    options = parser.add_argument_group('Options')
    options.add_argument('-v', '--inverse', action='store_true', help='prints out all the lines that do not matches the pattern')
    options.add_argument('-c', '--count', action='store_true', help='This prints only a count of the lines that match a pattern')
    options.add_argument('-i', '--ignore-case', action='store_true', help='Ignores case for matching')
    arguments.add_argument('pattern', nargs='?', help='Pattern to match')
    arguments.add_argument('filename', nargs='?', help='File/filepath to find matches in')
    options.add_argument('-n', '--line-number', action='store_true', help='Display the matched lines and their line numbers')
    options.add_argument('-w', '--word', action='store_true', help='Match whole word -- in progress DO NOT USE')
    
    args = parser.parse_args()
    ignore_case = args.ignore_case
    count = args.count

    print(args)


    if not args.pattern:
        parser.print_help()
        exit()
    
    else:
        if not args.inverse and not args.filename:
            find_matches(args.pattern, sys.stdin)
           
        if not args.inverse and args.filename:
            find_matches_file(args.pattern, args.filename)

        if args.inverse and not args.filename:
            inverse_matches(args.pattern, sys.stdin)
        
        if args.inverse and args.filename:
            find_inverse_file(args.pattern, args.filename)

if __name__ == '__main__':
    main()
