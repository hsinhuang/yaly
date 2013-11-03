#!/usr/bin/env python
# coding:utf-8

"""lex definition for C"""
#pylint: disable=C0103

from pyre import *
import lexer

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
t_PLUS             = escape('+')
t_MINUS            = escape('-')
t_TIMES            = escape('*')
t_DIVIDE           = escape('/')
t_MODULO           = escape('%')
t_OR               = escape('|')
t_AND              = escape('&')
t_NOT              = escape('~')
t_XOR              = escape('^')
t_LSHIFT           = concat(list('<<'))
t_RSHIFT           = concat(list('>>'))
t_LOR              = concat(list('||'))
t_LAND             = concat(list('&&'))
t_LNOT             = escape('!')
t_LT               = escape('<')
t_GT               = escape('>')
t_LE               = concat(list('<='))
t_GE               = concat(list('>='))
t_EQ               = concat(list('=='))
t_NE               = concat(list('!='))

# Assignment operators

t_EQUALS           = escape('=')
t_TIMESEQUAL       = concat(list('*='))
t_DIVEQUAL         = concat(list('/='))
t_MODEQUAL         = concat(list('%='))
t_PLUSEQUAL        = concat(list('+='))
t_MINUSEQUAL       = concat(list('-='))
t_LSHIFTEQUAL      = concat(list('<<='))
t_RSHIFTEQUAL      = concat(list('>>='))
t_ANDEQUAL         = concat(list('&='))
t_OREQUAL          = concat(list('|='))
t_XOREQUAL         = concat(list('^='))

# Increment/decrement
t_INCREMENT        = concat(list('++'))
t_DECREMENT        = concat(list('--'))

# ->
t_ARROW            = concat(list('->'))

# ?
t_TERNARY          = escape('?')

# Delimeters
t_LPAREN           = escape('(')
t_RPAREN           = escape(')')
t_LBRACKET         = escape('[')
t_RBRACKET         = escape(']')
t_LBRACE           = escape('{')
t_RBRACE           = escape('}')
t_COMMA            = escape(',')
t_PERIOD           = escape('.')
t_SEMI             = escape(';')
t_COLON            = escape(':')
t_ELLIPSIS         = concat(list('...'))

# Identifiers: r'[A-Za-z_][A-Za-z0-9_]*'
t_ID = concat([
    select([LOWERCASE, UPPERCASE, escape('_')]),
    loop(
        select([LOWERCASE, UPPERCASE, escape('_'), DIGIT])
    )
])

# Integer literal
def t_INTEGER(t):
    i = compile(loop_(DIGIT))
    t.value = int(t.value[:i.match_prefix(t.value)])
    return t

t_INTEGER.__doc__ = concat([
    loop_(DIGIT),
    optional(
        select([
            select(list('uU')),
            select(list('lL')),
            concat([select(list('uU')), select(list('lL'))]),
            concat([select(list('lL')), select(list('uU'))]),
        ])
    ),
])

# Floating literal:
def t_FLOAT(t):
    f = compile(select([
            concat([
                loop_(DIGIT),
                concat(['.', loop_(DIGIT)]),
                optional(
                    concat([
                        'e',
                        optional(select(list('+-'))),
                        loop_(DIGIT),
                    ])
                ),
            ]),
            concat([
                loop_(DIGIT),
                'e',
                optional(select(list('+-'))),
                loop_(DIGIT),
            ])
        ])
    )
    t.value = float(t.value[:f.match_prefix(t.value)])
    return t

t_FLOAT.__doc__ = concat([
    select([
        concat([
            loop_(DIGIT),
            concat(['.', loop_(DIGIT)]),
            optional(
                concat([
                    'e',
                    optional(select(list('+-'))),
                    loop_(DIGIT),
                ])
            ),
        ]),
        concat([
            loop_(DIGIT),
            'e',
            optional(select(list('+-'))),
            loop_(DIGIT),
        ])
    ]),
    optional(
        select([
            select(list('lL')),
            select(list('fF')),
        ])
    )
])

# String literal: r'\"([^\\\n]|(\\.))*?\"'
t_STRING = concat([
    '"',
    loop(
        select([
            diff(['\n', '"', '\\']),
            concat(['\\', WILDCARD]),
        ])
    ),
    '"',
])

# Character constant 'c' or L'c': r'(L)?\'([^\\\n]|(\\.))*?\''
t_CHARACTER = concat([
    optional('L'),
    escape("'"),
    select([
        diff(list('\\\n\r\f\v')),
        concat([
            '\\',
            select(["'", LOWERCASE, loop_(DIGIT)]),
        ]),
    ]),
    escape("'"),
])

# Comment (C-Style)
def t_COMMENT(t):
    t.lexer.lineno += t.value.count('\n')
    return t

t_COMMENT.__doc__ = concat([
    '/',
    '*',
    select([
        diff(['*']),
        concat(['*', diff(['/'])]),
    ]),
    '*',
    '/'
])

# Comment (C++-Style)
def t_CPPCOMMENT(t):
    t.lexer.lineno += 1
    return t

t_CPPCOMMENT.__doc__ = concat([
    '/',
    '/',
    diff(['\n']),
    '\n',
])

# scanner = lexer.lex()

# for token in scanner.get_next_token():
#     print token
