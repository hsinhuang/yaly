#!/usr/bin/env python
# coding:utf-8

"""syntax analysis"""

class TokenStream:
    """an input stream of tokens, read from a string"""
    def __init__(self, lexer):
        self.__cache__ = None
        self.__tokens__ = lexer.get_next_token()
    def get_next_token(self):
        """
        return the next token(type: Token), None when no token remains
        """
        if self.__cache__:
            token = self.__cache__
            self.__cache__ = None
            return token
        try:
            return self.__tokens__.next()
        except StopIteration:
            return None
    def push_back(self, token):
        """
        push the token back to stream
        """
        if self.__cache__:
            raise IOError(
                'cannot push token back when there is a token cached'
            )
        self.__cache__ = token


class LL1:
    """a defined LL(1) CFG"""
    def __init__(self, rules, precedences, terminals):
        """
        `rules` is a map from a non-terminal to a set of possible
        replacement and each replacement is a tuple, of which the
        first element is a proccessing fucntion, the second is a list
        of terminals or non-terminals that can replace the non-terminal
        """
        self.__stream__ = None
        self.__rules__ = rules
        self.__precedences__ = precedences
        self.__terminals__ = terminals
    def parse(self, string):
        """parse the string"""
        import sys
        all_vars = sys._getframe(1).f_locals
        if 'lexer' not in all_vars:
            raise NotImplementedError(
                'Yacc need variable `lexer` but not defined'
            )
        lexer = all_vars['lexer']
        lexer.set_string(string)
        self.__stream__ = TokenStream(lexer)

def __strip_im_left_recr__(rule, nonterminals):
    """
    strip all the immediate left recursion in the rule

    `rule`: a tuple -- the first element is the lhs of the rule,
    the second element is a list of all rhs'

    return the stripped rules -- a map from a non-terminal to a list of
    possible rhs and each rhs is a list of possible replacement
    """
    def randomword(length):
        import random, string
        return ''.join(random.choice(string.lowercase) for i in range(length))
    left_recr = []
    non_left_recr = []
    lhs = rule[0]
    for rhs in rule[1]:
        if rhs[0] == lhs:
            left_recr.append(rhs)
        else:
            non_left_recr.append(rhs)
    lhs_ = lhs
    while lhs_ in nonterminals:
        lhs_ = randomword(16)
    rules = {}
    rules[lhs] = []
    for beta in non_left_recr:
        rules[lhs].append(beta+[lhs_])
    rules[lhs_] = [ 'epsilon' ]
    for alpha in left_recr:
        rules[lhs_].append(alpha[1:]+[lhs_])
    return rules

def __strip_left_recr__(rules, nonterminals):
    """strip all the left recursion in the rules"""
    for i in range(len(nonterminals)):
        for j in range(i):
            Ys = [rhs[1:] for rhs in rules[nonterminals[i]][1] \
                if rhs[0] == rules[nonterminals[j]]]
            for y in Ys:
                rules[nonterminals[i]][1] = \
                    [delta+[y] for delta in rules[nonterminals[j]][1]]
        rules[nonterminals[i]][1] = \
            __strip_im_left_recr__(
                (nonterminals[i], rules[nonterminals[i]][1]),
                nonterminals
            )

def yacc():
    """return a LL1"""
    import sys
    all_vars = sys._getframe(1).f_locals
    terminals = all_vars['tokens']
    nonterminals = set()
    rules = {}
    precedences = None if 'precedences' not in all_vars \
        else all_vars['precedences']
    import inspect
    for func in all_vars:
        if inspect.isfunction(func) and func.__name__.startswith('p_'):
            raw_rule = func.__doc__
            if not raw_rule:
                raise SyntaxError(
                    '`%s` recognised as a grammar proccessing function \
                    but no docstring found' % var.__name__
                )
            rp_rule = raw_rule.split(':')
            if len(rp_rule) != 2:
                raise SyntaxError(
                    'Syntax rule `%s` not valid' % raw_rule
                )
            lhs, rhs = rp_rule[0].strip(), rp_rule[1].strip()
            import re
            replacements = re.split(r'\s+', rhs)
            if not all([s.isupper() or s.islower() for s in replacements]):
                raise SyntaxError(
                    'every identifier in rules should be uppercase \
                    or lowercase'
                )
            nonterminals.update([s for s in replacements if s.islower()])
            rules.setdefault(lhs, set())
            rules[lhs].add((func, replacements,))
    nonterminals = list(nonterminals)
    __strip_left_recr__(rules, nonterminals)
    return LL1(rules, precedences, terminals)
