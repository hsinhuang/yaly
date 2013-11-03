#!/usr/bin/env python
# coding:utf-8

"""lex definition for C--"""
#pylint: disable=C0103

import pyre

# Reserved words

tokens = [
    # Literals (identifier, integer constant, float constant,
    # string constant, char const)
    'ID', 'TYPEID', 'ICONST', 'FCONST', 'SCONST', 'CCONST',

    # Operators (+,-,*,/,%,|,&,~,^,<<,>>, ||, &&, !, <, <=, >, >=, ==, !=)
    'PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'MOD',
    'OR', 'AND', 'NOT', 'XOR', 'LSHIFT', 'RSHIFT',
    'LOR', 'LAND', 'LNOT',
    'LT', 'LE', 'GT', 'GE', 'EQ', 'NE',

    # Assignment (=, *=, /=, %=, +=, -=, <<=, >>=, &=, ^=, |=)
    'EQUALS', 'TIMESEQUAL', 'DIVEQUAL', 'MODEQUAL', 'PLUSEQUAL', 'MINUSEQUAL',
    'LSHIFTEQUAL','RSHIFTEQUAL', 'ANDEQUAL', 'XOREQUAL', 'OREQUAL',

    # Increment/decrement (++,--)
    'PLUSPLUS', 'MINUSMINUS',

    # Structure dereference (->)
    'ARROW',

    # Ternary operator (?)
    'TERNARY',

    # Delimeters ( ) [ ] { } , . ; :
    'LPAREN', 'RPAREN',
    'LBRACKET', 'RBRACKET',
    'LBRACE', 'RBRACE',
    'COMMA', 'PERIOD', 'SEMI', 'COLON',

    # Ellipsis (...)
    'ELLIPSIS',
]

# Operators
t_PLUS             = pyre.escape('+')
t_MINUS            = pyre.escape('-')
t_TIMES            = pyre.escape('*')
t_DIVIDE           = pyre.escape('/')
t_MODULO           = pyre.escape('%')
t_OR               = pyre.escape('|')
t_AND              = pyre.escape('&')
t_NOT              = pyre.escape('~')
t_XOR              = pyre.escape('^')
t_LSHIFT           = pyre.concatenation('<<')
t_RSHIFT           = pyre.concatenation('>>')
t_LOR              = pyre.concatenation('||')
t_LAND             = pyre.concatenation('&&')
t_LNOT             = pyre.escape('!')
t_LT               = pyre.escape('<')
t_GT               = pyre.escape('>')
t_LE               = pyre.concatenation('<=')
t_GE               = pyre.concatenation('>=')
t_EQ               = pyre.concatenation('==')
t_NE               = pyre.concatenation('!=')

# Assignment operators

t_EQUALS           = pyre.escape('=')
t_TIMESEQUAL       = pyre.concatenation('*=')
t_DIVEQUAL         = pyre.concatenation('/=')
t_MODEQUAL         = pyre.concatenation('%=')
t_PLUSEQUAL        = pyre.concatenation('+=')
t_MINUSEQUAL       = pyre.concatenation('-=')
t_LSHIFTEQUAL      = pyre.concatenation('<<=')
t_RSHIFTEQUAL      = pyre.concatenation('>>=')
t_ANDEQUAL         = pyre.concatenation('&=')
t_OREQUAL          = pyre.concatenation('|=')
t_XOREQUAL         = pyre.concatenation('^=')

# Increment/decrement
t_INCREMENT        = pyre.concatenation('++')
t_DECREMENT        = pyre.concatenation('--')

# ->
t_ARROW            = pyre.concatenation('->')

# ?
t_TERNARY          = pyre.escape('?')

# Delimeters
t_LPAREN           = pyre.escape('(')
t_RPAREN           = pyre.escape(')')
t_LBRACKET         = pyre.escape('[')
t_RBRACKET         = pyre.escape(']')
t_LBRACE           = pyre.escape('{')
t_RBRACE           = pyre.escape('}')
t_COMMA            = pyre.escape(',')
t_PERIOD           = pyre.escape('.')
t_SEMI             = pyre.escape(';')
t_COLON            = pyre.escape(':')
t_ELLIPSIS         = pyre.concatenation('...')

# Identifiers: r'[A-Za-z_][A-Za-z0-9_]*'
t_ID = pyre.concatenation([
    pyre.selection([
        pyre.selection(pyre.LOWERCASE),
        pyre.selection(pyre.UPPERCASE),
        pyre.escape('_'),
    ]),
    pyre.loop(
        pyre.selection([
            pyre.selection(pyre.LOWERCASE),
            pyre.selection(pyre.UPPERCASE),
            pyre.escape('_'),
            pyre.selection(pyre.DIGITS),
        ])
    )
])

# Integer literal
t_INTEGER = r'\d+([uU]|[lL]|[uU][lL]|[lL][uU])?'

# Floating literal
t_FLOAT = r'((\d+)(\.\d+)(e(\+|-)?(\d+))? | (\d+)e(\+|-)?(\d+))([lL]|[fF])?'

# String literal
t_STRING = r'\"([^\\\n]|(\\.))*?\"'

# Character constant 'c' or L'c'
t_CHARACTER = r'(L)?\'([^\\\n]|(\\.))*?\''

# Comment (C-Style)
def t_COMMENT(t):
    r'/\*(.|\n)*?\*/'
    t.lexer.lineno += t.value.count('\n')
    return t

# Comment (C++-Style)
def t_CPPCOMMENT(t):
    r'//.*\n'
    t.lexer.lineno += 1
    return t
