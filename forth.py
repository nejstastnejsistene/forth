#!/usr/bin/env python3

import sys
import operator


class Forth(object):

    def __init__(self):
        self.stack = []
        self.env = builtins
        self._showstack = False
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
        elif word in self.env:
            func = builtins[word]
            if isinstance(func, list):
                self.exec(func)
            else:
                builtins[word](self)

        # Anything else is assumed to be a base 10 integer.
        else:
            self.stack.append(int(word))


    def exec(self, words):
        for word in words:
            self.push(word)

    def parse_until(self, word, action=lambda f: None):
        '''Set a delimiter, and a function to apply to parsed wordsi.'''
        self.delimiter = word
        self.args = []
        self.action= action

    def clear(self):
        '''Clear end of line comments, and optionally print the stack.'''
        if self.delimiter == '\n':
            self.delimiter = None
        if self._showstack:
            print(self.stack)

    def showstack(self, show):
        self._showstack = show

    def foo(self, func, nargs):
        '''Apply a python function to the top nargs items on the stack,
           and place the result back on the stack.
        '''
        args = [self.stack.pop() for i in range(nargs)]
        self.stack.append(func(*reversed(args)))


def defun(f):
    '''Define a function.'''
    name = f.args[0]
    body = f.args[1:]
    f.env[name] = body

def if_statement(f):
    def handle_then(f):
        f.exec(f.args)
        f.parse_until('else')
    def handle_else(f):
        f.parse_until('else', lambda f: f.exec(f.args))
    f.parse_until('then', handle_then if f.stack.pop() else handle_else)

def dup(f):
    '''( a -- a a )'''
    a = f.stack.pop()
    f.stack.append(a)
    f.stack.append(a)

def swap(f):
    '''( a b -- b a)'''
    b = f.stack.pop()
    a = f.stack.pop()
    f.stack.append(b)
    f.stack.append(a)

def over(f):
    '''( a b -- a b a)'''
    b = f.stack.pop()
    a = f.stack.pop()
    f.stack.append(a)
    f.stack.append(b)
    f.stack.append(a)

builtins = {
    '(': lambda f: f.parse_until(')'),
    '\\': lambda f: f.parse_until('\n'),
    '.': lambda f: print(f.stack.pop()),
    'showstack': lambda f: f.showstack(True),
    'noshowstack': lambda f:f.showstack(False),
    '.s': lambda f: print(f.stack),
    ':': lambda f: f.parse_until(';', defun),
    'if': lambda f: if_statement(f),

    # Arithmetic and logical operators.
    '+': lambda f: f.foo(operator.add, 2),
    '-': lambda f: f.foo(operator.sub, 2),
    '*': lambda f: f.foo(operator.mul, 2),
    '/': lambda f: f.foo(operator.floordiv, 2),
    'mod': lambda f: f.foo(operator.mod, 2),
    #'/mod': lambda f: f.foo(operator.divmod, 2),
    'and': lambda f: f.foo(operator.and_, 2),
    'or': lambda f: f.foo(operator.or_, 2),
    'xor': lambda f: f.foo(operator.xor, 2),
    'lshift': lambda f: f.foo(operator.lshift, 2),
    '<<': lambda f: f.foo(operator.lshift, 2),
    'rshift': lambda f: f.foo(operator.rshift, 2),
    '>>': lambda f: f.foo(operator.rshift, 2),
    'abs': lambda f: f.foo(abs, 1),
    'max': lambda f: f.foo(max, 2),
    'min': lambda f: f.foo(min, 2),
    'invert': lambda f: f.foo(operator.inv, 1),
    'negate': lambda f: f.foo(operator.neg, 1),
    '1-': list('1-'),
    '1+': list('2+'),
    '2/': list('2/'),
    '2*': list('2*'),

    # Stack operators.
    'dup': lambda f: dup(f),
    '?dup': 'dup if dup then'.split(),
    'drop': lambda f: f.stack.pop(),
    'swap': lambda f: swap(f),
    'over': lambda f: over(f),
    'rot': lambda f: rot(f),
    '-rot': 'rot rot'.split(),
    'nip': 'swap drop'.split(),
    'tuck': 'swap over'.split(),
}



def prompt(ps1=' ok '):
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
