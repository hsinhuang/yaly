#!/usr/bin/env python
# coding:utf-8

"""lexical analysis"""

class Token:
    """
    A token is a string of one or more characters that is significant
    as a group.
    """
    def __init__(self, lexical_unit, value, lineno, lexer):
        assert type(lexical_unit) == str
        self.__lexical_unit__ = lexical_unit
        self.__raw__ = value
        self.skip = False
        self.value = value
        self.lexer = lexer
        self.lineno = lineno
    def __str__(self):
        return "<%s, %s, line %d>" % \
            (self.__lexical_unit__, repr(self.value), self.lineno)
    def lexical_unit(self):
        """getter : __lexical_unit__"""
        return self.__lexical_unit__

class Lexer:
    """Lexer performs lexical analysis"""
    def __init__(self, tokens, raw_tokens, regex):
        """
        `tokens` is a dict map token name (i.e. lexical unit) to a tuple,
        of which the first position is a compiled regular expression
        (type: pyre.RegEx) and the second one is the function

        `raw_tokens` is an iterable object which contains all tokens name
        and the order in it is the precedence of each token

        `regex` is a compiled RegEx object which accepts all valid
        string
        """
        self.__tokens__ = tokens
        self.__raw_tokens__ = raw_tokens
        self.__string__ = None
        self.__re__ = regex
        self.lineno = 0
    def get_next_token(self):
        """
        return a token(type: Token) stream
        """
        if self.__string__ is None:
            raise UserWarning('having not specify input string')
        while self.__string__:
            next_idx = self.__re__.match_prefix(self.__string__)
            if not next_idx:
                raise SyntaxWarning("remaining `%s` cannot be parsed" % \
                    self.__string__)
            lexeme = self.__string__[:next_idx]
            self.__string__ = self.__string__[next_idx:]
            found = False
            for token in self.__raw_tokens__:
                assert token in self.__tokens__
                if self.__tokens__[token][0].match(lexeme):
                    found = True
                    next_token = self.__tokens__[token][1](
                        Token(token, lexeme, self.lineno, self)
                    )
                    if next_token.skip:
                        continue
                    yield next_token
                    break
            if not found:
                raise AssertionError("lexeme `%s` is valid " % lexeme  + \
                    "but not found the corresponding lexical unit" )
    def set_string(self, string):
        """set input string"""
        self.__string__ = string
        self.lineno = 1

def lex():
    """
    return a Lexer
    """
    compiled_tokens = {}
    regexs = []
    import sys
    all_vars = sys._getframe(1).f_locals
    if 'tokens' not in all_vars:
        raise NotImplementedError(
            'Lex need variable `tokens` but not defined'
        )
    tokens = all_vars['tokens']
    if not hasattr(tokens, '__iter__'):
        raise TypeError(
            'Lex expected variable `tokens` to be iterable'
        )
    for token in tokens:
        if not token.isupper():
            raise SyntaxError(
                'token `%s` is not uppercase' % token
            )
        if tokens.count(token) > 1:
            raise SyntaxWarning(
                'declared token `%s` %d times' % \
                (token, tokens.count(token))
            )
        func_name = 't_' + token
        if func_name not in all_vars:
            raise NotImplementedError(
                'declared token `%s` but not define `%s`' % \
                (token, func_name)
            )
        func = all_vars[func_name]
        if type(func) is str:
            all_vars[func_name] = lambda t : t
            all_vars[func_name].__doc__ = func
            func = all_vars[func_name]
        import yare
        try:
            compiled_tokens[token] = (yare.compile(func.__doc__), func)
        except SyntaxError:
            raise SyntaxError(
                'regular expression `%s` specified' % func.__doc__ + \
                'in function `%s` not valid' % func_name
            )
        regexs.append(func.__doc__)
    return Lexer(compiled_tokens, tokens, yare.compile(yare.select(regexs)))
