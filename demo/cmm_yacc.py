#!/usr/bin/env python
# coding:utf-8

"""yacc definition for C--"""

from yaly.yacc import *
from cmm_lex import lexer, tokens

with open('cmm.bnf.txt', 'r') as f:
    grammar = [ line.strip() for line in f.xreadlines() if line.strip() ]

parser = yacc()
