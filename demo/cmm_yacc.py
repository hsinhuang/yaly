#!/usr/bin/env python
# coding:utf-8

"""yacc definition for C--"""

import os.path as p

import yaly.yacc as yacc
from cmm_lex import lexer, tokens

with open(p.join(p.dirname(__file__), 'cmm.bnf.txt'), 'r') as f:
    grammar = [ line.strip() for line in f.xreadlines() if line.strip() ]

parser = yacc.yacc()

with open(p.join(p.dirname(__file__), 'cmm_input.c'), 'r') as f:
    s = f.read()
parser.parse(s)
