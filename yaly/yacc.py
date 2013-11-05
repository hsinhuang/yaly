#!/usr/bin/env python
# coding:utf-8

"""syntax analysis"""

class TokenStream:
    """an input stream of tokens, read from a string"""
    def __init__(self, string):
        self.__string__ = string

class Syntax:
    """a defined syntax"""
    pass

def yacc():
    """return a Syntax"""
    import sys
    all_vars = sys._getframe(1).f_locals
    if 'tokens' not in all_vars:
        raise NotImplementedError(
            'Yacc need variable `tokens` but not defined'
        )
    tokens = all_vars['tokens']
    if not hasattr(tokens, '__iter__'):
        raise TypeError(
            'Yacc expected variable `tokens` to be iterable'
        )
    rules = {} # map from a non-terminal to a list of possible replacement
    import inspect
    for var in all_vars:
        if inspect.isfunction(var) and var.__name__.startswith('p_'):
            raw_rule = var.__doc__
            rp_rule = raw_rule.split(':')
            if len(rp_rule) != 2:
                raise SyntaxError(
                    'Syntax rule `%s` not valid' % raw_rule
                )
            lhs, rhs = rp_rule[0].strip(), rp_rule[1].strip()
            import re
            replacements = re.split('\s+', rhs)
            # TODO
