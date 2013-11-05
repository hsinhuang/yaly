#!/usr/bin/env python
# coding:utf-8

"""yacc definition for C--"""
#pylint: disable=C0103

import yaly as yacc

grammars = (
    'program : stmts',
    'stmts : stmt stmts',
    'stmts : stmt',
)
