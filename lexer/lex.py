#!/usr/bin/env python
# coding:utf-8

"""lexical analysis"""

import inspect
import pyre

class Token:
    """
    A token is a string of one or more characters that is significant
    as a group.
    """
    def __init__(self, lexical_unit, value, lexer):
        assert type(lexical_unit) == str
        self.__raw__ = lexical_unit
        self.__lexical_unit__ = lexical_unit
        self.value = value
        self.__lexer__ = lexer
    def __str__(self):
        return self.__raw__
    def lexical_unit(self):
        """getter : __lexical_unit__"""
        return self.__lexical_unit__

class Lexer:
    """Lexer performs lexical analysis"""
    def __init__(self, tokens, regex):
        """
        `tokens` is a dict map token name (i.e. lexical unit) to a tuple,
        of which the first position is a compiled regular expression
        (type: pyre.RegEx) and the second one is the function

        `regex` is a compiled RegEx object which accepts all valid
        string
        """
        self.__tokens__ = tokens
        self.__string__ = None
        self.__re__ = regex
        self.lineno = 0
    def get_next_token(self):
        """
        return next token(type: Token)
        """
        while self.__string__:
            next_idx = self.__re__.match_prefix(self.__string__)
            if not next_idx:
                raise SyntaxWarning("remaining `%s` cannot be parsed" % \
                    self.__string__)
            lexeme = self.__string__[:next_idx]
            self.__string__ = self.__string__[next_idx:]
            for token in self.__tokens__:
                if self.__tokens__[token][0].match(lexeme):
                    yield self.__tokens__[token][1](
                        Token(token, lexeme, self)
                        )
                    break
            else:
                raise AssertionError("lexeme `%s` is valid but not " + \
                    "found the corresponding lexical unit" % lexeme)
    def set_string(self, string):
        """set input string"""
        self.__string__ = string

__default_token_func_template__ = """
def %s(t):
    "%s"
    return t
"""

def lex():
    """
    return a Lexer
    """
    compiled_tokens = {}
    regexs = []
    all_vars = globals()
    tokens = all_vars['tokens']
    for token in tokens:
        func_name = 't_' + token
        if func_name not in all_vars:
            raise NotImplementedError(
                'declared token `%s` but not define `%s`' % \
                (token, func_name)
            )
        func = all_vars[func_name]
        if type(func) is str:
            exec (__default_token_func_template__ % (func_name, func))
            func = globals()[func_name]
        try:
            compiled_tokens[token] = (pyre.compile(func.__doc__), func)
        except SyntaxError:
            raise SyntaxError(
                'regular expression `%s` specified \
                in function `%s` not valid' % \
                (func.__doc__, func_name)
            )
        regexs.append(func.__doc__)
    return Lexer(compiled_tokens, pyre.compile(pyre.select(regexs)))

def glo():
    return globals()
