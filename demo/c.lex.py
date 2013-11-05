#!/usr/bin/env python
# coding:utf-8

"""lex definition for C"""
#pylint: disable=C0103

from yare import *
import yaly as lex

# Reserved words

tokens = (
    # Types
    'CHAR', 'INT', 'LONG', 'FLOAT', 'DOUBLE', 'VOID',
    'CONST', 'SIGNED', 'UNSIGNED', 'STATIC', 'STRUCT',
    'UNION',

    # Other keywords
    'AUTO', 'BREAK', 'CASE', 'CONTINUE', 'DEFAULT',
    'DO', 'ELSE', 'ENUM', 'EXTERN', 'FOR', 'GOTO',
    'IF', 'REGISTER', 'RETURN', 'SIZEOF', 'SWITCH',
    'TYPEDEF', 'VOLATILE', 'WHILE',

    # Literals
    'INTEGER', 'REAL', 'STRING', 'CHARACTER',

    # Comment
    'COMMENT', 'CPPCOMMENT',

    # Operators (+,-,*,/,%,|,&,~,^,<<,>>, ||, &&, !, <, <=, >, >=, ==, !=)
    'PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'MOD',
    'OR', 'AND', 'NOT', 'XOR', 'LSHIFT', 'RSHIFT',
    'LOR', 'LAND', 'LNOT',
    'LT', 'LE', 'GT', 'GE', 'EQ', 'NE',

    # Assignment (=, *=, /=, %=, +=, -=, <<=, >>=, &=, ^=, |=)
    'EQUAL', 'TIMESEQUAL', 'DIVEQUAL', 'MODEQUAL', 'PLUSEQUAL', 'MINUSEQUAL',
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

    # Newline \n
    'NEWLINE',

    # whitespace
    'WHITESPACE',

    # Identifier
    'ID',
)

#Types
t_CHAR             = concat(list('char'))
t_INT              = concat(list('int'))
t_LONG             = concat(list('long'))
t_FLOAT            = concat(list('float'))
t_DOUBLE           = concat(list('double'))
t_VOID             = concat(list('void'))
t_CONST            = concat(list('const'))
t_SIGNED           = concat(list('signed'))
t_UNSIGNED         = concat(list('unsigned'))
t_STATIC           = concat(list('static'))
t_STRUCT           = concat(list('struct'))
t_UNION            = concat(list('union'))
t_AUTO             = concat(list('auto'))
t_BREAK            = concat(list('break'))
t_CASE             = concat(list('case'))
t_CONTINUE         = concat(list('continue'))
t_DEFAULT          = concat(list('default'))
t_DO               = concat(list('do'))
t_ELSE             = concat(list('else'))
t_ENUM             = concat(list('enum'))
t_EXTERN           = concat(list('extern'))
t_FOR              = concat(list('for'))
t_GOTO             = concat(list('goto'))
t_IF               = concat(list('if'))
t_REGISTER         = concat(list('register'))
t_RETURN           = concat(list('return'))
t_SIZEOF           = concat(list('sizeof'))
t_SWITCH           = concat(list('switch'))
t_TYPEDEF          = concat(list('typedef'))
t_VOLATILE         = concat(list('volatile'))
t_WHILE            = concat(list('while'))

# Operators
t_PLUS             = escape('+')
t_MINUS            = escape('-')
t_TIMES            = escape('*')
t_DIVIDE           = escape('/')
t_MOD              = escape('%')
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

t_EQUAL            = escape('=')
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
t_PLUSPLUS         = concat(list('++'))
t_MINUSMINUS       = concat(list('--'))

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
t_WHITESPACE       = loop_(select([' ', '\t']))

# Identifiers: r'[A-Za-z_][A-Za-z0-9_]*'
t_ID = concat([
    select([LOWERCASE, UPPERCASE, escape('_')]),
    loop(
        select([LOWERCASE, UPPERCASE, escape('_'), DIGIT])
    )
])

# Integer literal
def t_INTEGER(t):
    t.value = int(t.value)
    return t

t_INTEGER.__doc__ = concat([
    loop_(DIGIT),
])

# Floating literal:
def t_REAL(t):
    t.value = float(t.value)
    return t

t_REAL.__doc__ = select([
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

# String literal: r'\"([^\\\n]|(\\.))*?\"'
t_STRING = concat([
    '"',
    loop(
        select([
            diff(list('\\\n\r\f\v\t"')),
            concat([
                '\\',
                select(['\\', '"', 'a', 'b', 'f',
                    'n', 'r', 't', 'v', loop_(DIGIT),
                    concat(['x',
                        loop_(
                            select([DIGIT, range('A', 'F'),
                                range('a', 'f')])
                        )
                    ])
                ]),
            ]),
        ])
    ),
    '"',
])

# Character constant 'c' or L'c': r'(L)?\'([^\\\n]|(\\.))*?\''
t_CHARACTER = concat([
    escape("'"),
    select([
        diff(list('\\\n\r\f\v\t\'')),
        concat([
            '\\',
            select(['\\', '\'', 'a', 'b', 'f',
                'n', 'r', 't', 'v', loop_(DIGIT),
                concat(['x',
                    loop_(
                        select([DIGIT, range('A', 'F'),
                            range('a', 'f')])
                    )
                ])
            ]),
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
    loop(
        select([
            diff(['*']),
            concat(['*', diff(['/'])]),
        ])
    ),
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
    loop(diff(['\n'])),
    '\n',
])

# Newline
def t_NEWLINE(t):
    t.lexer.lineno += 1
    return t

t_NEWLINE.__doc__ = escape('\n')

scanner = lex.lex()

import os.path as p
with open(p.join(p.dirname(__file__), 'temp.c'), 'r') as f:
    s = f.read()
scanner.set_string(s)
for token in scanner.get_next_token():
    print token
