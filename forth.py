#!/usr/bin/env python3

import sys


class Forth(object):

    def __init__(self):
        self.stack = []
        self.delimiter = None

    def push(self, word):
        '''Process a single word.'''

        # If the delimiter is reached, process the accumulated arguments.
        if word == self.delimiter:
            self.delimiter = None
            self.action(self)

        # Accumulate arguments while searching for delimiter.
        elif self.delimiter:
            self.args.append(word)

        # Apply builtin functions.
        elif word in builtins:
            builtins[word](self)

        # Anything else is assumed to be a base 10 integer.
        else:
            self.stack.append(int(word))


    def parse_until(self, word, action=lambda f: None):
        '''Set a delimiter, and a function to apply to parsed wordsi.'''
        self.delimiter = word
        self.args = []
        self.action= action

    def clear(self):
        '''Clear end of line comments.'''
        if self.delimiter == '\n':
            self.delimiter = None

builtins = {
    '(': lambda f: f.parse_until(')'),
    '\\': lambda f: f.parse_until('\n'),
    '.': lambda f: print(f.stack.pop()),
}



def prompt(ps1='>>> '):
    sys.stdout.write(ps1)
    sys.stdout.flush()


forth = Forth()

prompt()
word = ''
while True:
    ch = sys.stdin.read(1)
    if not ch or ch.isspace():
        if word:
            forth.push(word)
            word = ''
        if not ch:
            break
        if ch == '\n':
            forth.clear()
            prompt()
    else:
        word += ch
