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
        replacement and each replacement is a two-element list, of which
        the first element is a proccessing fucntion, the second is a
        list of terminals or non-terminals that can replace the
        non-terminal
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
    left_recr = []
    non_left_recr = []
    lhs = rule[0]
    for rhs in rule[1]:
        if rhs[0] == lhs:
            left_recr.append(rhs)
        else:
            non_left_recr.append(rhs)
    lhs_ = lhs + '\''
    while lhs_ in nonterminals:
        lhs_ += '\''
    rules = {}
    rules[lhs] = []
    for beta in non_left_recr:
        if len(beta) == 1 and beta[0] == 'epsilon':
            rules[lhs].append([lhs_])
        else:
            rules[lhs].append(beta+[lhs_])
    rules[lhs_] = [ ['epsilon'] ]
    for a_alpha in left_recr:
        rules[lhs_].append(a_alpha[1:]+[lhs_])
    return rules

def __strip_left_recr__(rules, nonterminals):
    """strip all the left recursion in the rules"""
    length = len(nonterminals)
    for i in range(length):
        for j in range(i):
            ai_lhs, aj_lhs = nonterminals[i], nonterminals[j]
            ai_rhs, aj_rhs = [rhs for rhs in rules[ai_lhs][1]], \
                [rhs for rhs in rules[aj_lhs][1]]
            new_ai_rhs = []
            for ajy in ai_rhs:
                if ajy[0] == aj_lhs:
                    for delta in aj_rhs:
                        if len(delta) == 1 and delta[0] == 'epsilon':
                            new_ai_rhs.append(ajy[1:])
                        else:
                            new_ai_rhs.append(delta+ajy[1:])
                else:
                    new_ai_rhs.append(ajy)
            print 'new_ai_rhs =>', new_ai_rhs
            ai_ = __strip_im_left_recr__((ai_lhs, new_ai_rhs), nonterminals)
            print 'ai_ =>', ai_
            for lhs in ai_:
                if lhs not in nonterminals:
                    nonterminals.append(lhs)
                    rules[lhs] = [None, ai_[lhs]]
                else:
                    rules[lhs] = [rules[ai_lhs][0], ai_[lhs]]
            print 'rules =>', rules

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
                    but no docstring found' % func.__name__
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
