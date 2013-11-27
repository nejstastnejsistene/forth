#!/usr/bin/env python3

import sys


class Forth(object):

    def push(self, word):
        print('word:', word)


forth = Forth()

word = ''
while True:
    ch = sys.stdin.read(1)
    if not ch or ch.isspace():
        if word:
            forth.push(word)
            word = ''
        if not ch:
            break
    else:
        word += ch
