#!/usr/bin/env python
# coding:utf-8

"""lex definition for C--"""
#pylint: disable=C0103

import yare
import yaly.lex as lex

tokens = (
    # Types
    'CHAR', 'INT', 'VOID',

    # Keywords
    'ELSE', 'EXTERN', 'FOR', 'IF', 'RETURN', 'WHILE',

    # Literals
    'INTCON', 'STRINGCON', 'CHARCON',

    # Comments
    'COMMENT',

    # Operators
    'ASSIGN', 'PLUS', 'MINUS', 'TIMES', 'DIVIDE',
    'OR', 'AND', 'NOT', 'LT', 'LE', 'GT', 'GE', 'EQ', 'NE',
    'COMMA', 'SEMI',

    # Parenthenses
    'LPAREN', 'RPAREN',
    'LBRACKET', 'RBRACKET',
    'LBRACE', 'RBRACE',

    # Newlines
    'NEWLINE',

    # Whitespaces
    'WHITESPACE',

    # Identifiers
    'ID',
)

# Types
t_CHAR = yare.concat(list('char'))
t_INT = yare.concat(list('int'))
t_VOID = yare.concat(list('void'))

# Keywords
t_ELSE = yare.concat(list('else'))
t_EXTERN = yare.concat(list('extern'))
t_FOR = yare.concat(list('for'))
t_IF = yare.concat(list('if'))
t_RETURN = yare.concat(list('return'))
t_WHILE = yare.concat(list('while'))

# Literals
def t_INTCON(t):
    t.value = int(t.value)
    return t
t_INTCON.__doc__ = yare.concat([
    yare.loop_(yare.DIGIT),
])

__STRINGCON__ = ' !#$%&\'()*+,-./0123456789:;<=>?@' + \
    'ABCDEFGHIJKLMNOPQRSTUVWXYZ[]^_`abcdefghijklmnopqrstuvwxyz{|}~'
t_STRINGCON = yare.concat([
    '"',
    yare.loop(
        yare.select([
            yare.select(list(__STRINGCON__)),
            yare.concat(['\\', yare.select(['n', '\\', '"'])]),
        ])
    ),
    '"',
])

__CHARCON__ = ' !#$%&()*+,-./0123456789:;<=>?@' + \
    'ABCDEFGHIJKLMNOPQRSTUVWXYZ[]^_`abcdefghijklmnopqrstuvwxyz{|}~'
t_CHARCON = yare.concat([
    '\'',
    yare.select([
        yare.select(list(__CHARCON__)),
        yare.concat(['\\', yare.select(['n', '\\', '\'', '0'])]),
    ]),
    '\'',
])

def t_COMMENT(t):
    t.lexer.lineno += 1
    t.skip = True
    return t
t_COMMENT.__doc__ = yare.concat([
    '/',
    '/',
    yare.loop(yare.diff(['\n'])),
    '\n',
])

# Operators
t_ASSIGN = yare.escape('=')
t_PLUS = yare.escape('+')
t_MINUS = yare.escape('-')
t_TIMES = yare.escape('*')
t_DIVIDE = yare.escape('/')
t_OR = yare.concat(list('||'))
t_AND = yare.concat(list('&&'))
t_NOT = yare.escape('!')
t_LT = yare.escape('<')
t_GT = yare.escape('>')
t_LE = yare.concat(list('<='))
t_GE = yare.concat(list('>='))
t_EQ = yare.concat(list('=='))
t_NE = yare.concat(list('!='))
t_COMMA = yare.escape(',')
t_SEMI = yare.escape(';')

# Parenthenses
t_LPAREN = yare.escape('(')
t_RPAREN = yare.escape(')')
t_LBRACKET = yare.escape('[')
t_RBRACKET = yare.escape(']')
t_LBRACE = yare.escape('{')
t_RBRACE = yare.escape('}')

# Newlines
def t_NEWLINE(t):
    t.lexer.lineno += t.value.count('\n')
    t.skip = True
    return t
t_NEWLINE.__doc__ = yare.loop_('\n')

# Whitespaces
def t_WHITESPACE(t):
    t.skip = True
    return t
t_WHITESPACE.__doc__ = yare.loop_(yare.select([' ', '\t']))

# Identifiers
t_ID = yare.concat([
    yare.select([yare.LOWERCASE, yare.UPPERCASE]),
    yare.loop(
        yare.select([
            yare.LOWERCASE, yare.UPPERCASE,
            yare.escape('_'), yare.DIGIT
        ])
    )
])

lexer = lex.lex()

if __name__ == '__main__':
    import os.path as p
    with open(p.join(p.dirname(__file__), 'temp.c'), 'r') as f:
        s = f.read()
    lexer.set_string(s)
    for token in lexer.get_next_token():
        print token
