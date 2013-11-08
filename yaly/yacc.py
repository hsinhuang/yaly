#!/usr/bin/env python
# coding:utf-8

"""syntax analysis"""

class TokenStream:
    """an input stream of tokens, read from a string"""
    def __init__(self, lexer):
        self.__cache__ = None
        self.__tokens__ = lexer.get_next_token()
    def __iter__(self):
        return self
    def next(self):
        """
        return the next token(type: Token), None when no token remains
        """
        if self.__cache__:
            token = self.__cache__
            self.__cache__ = None
            return token
        return self.__tokens__.next()
    def push_back(self, token):
        """
        push the token back to stream
        """
        if self.__cache__:
            raise IOError(
                'cannot push token back when there is a token cached'
            )
        self.__cache__ = token

class Rule:
    """
    a single rule for a nonterminal, and maybe this nonterminal
    has other rules
    """
    def __init__(self, rule_spec, func):
        """
        `rule_spec` is a string or tuple which specifies the rule
        format: 'lhs : t1 t2 t3 ...' or ('lhs', ['t1', 't2', 't3', ...])
        """
        assert type(rule_spec) == str or type(rule_spec) == tuple
        self.__func__ = func
        rp_rule = rule_spec.split(':') if type(rule_spec) == str \
            else rule_spec
        if len(rp_rule) != 2:
            raise SyntaxError(
                'Syntax rule `%s` not valid' % rule_spec
            )
        self.__lhs__, rhs = rp_rule[0].strip(), rp_rule[1].strip() \
            if type(rule_spec) == str else rp_rule[0]
        import re
        self.__rhs__ = re.split(r'\s+', rhs) \
            if type(rule_spec) == str else rp_rule[1]
        if not all([ Rule.is_valid_term(s) for s in self.__rhs__] + \
            [ Rule.is_nonterminal(self.__lhs__) ]):
            raise SyntaxError(
                'terminals in rules should be uppercase, \
                while nonterminals in rules should be lowercase'
            )
        self.__nonterminals__ = { self.__lhs__ }
        self.__terminals__ = set()
        for _id in self.__rhs__:
            if Rule.is_nonterminal(_id):
                self.__nonterminals__.add(_id)
            else:
                self.__terminals__.add(_id)
    def __str__(self):
        return ' '.join([self.__lhs__, ':'] + self.__rhs__)
    def __eq__(self, other):
        return self.__lhs__ == other.__lhs__ and \
            self.__rhs__ == other.__rhs__
    def __ne__(self, other):
        return not self.__eq__(other)
    def __hash__(self):
        return self.__str__().__hash__()
    @staticmethod
    def epsilon(lhs, func):
        """make an epsilon Rule"""
        return Rule((lhs, ['epsilon']), func)
    @staticmethod
    def is_terminal(term):
        """whether the term is terminal"""
        return term.isupper()
    @staticmethod
    def is_nonterminal(term):
        """whether the term is nonterminal"""
        return term.islower()
    @staticmethod
    def is_valid_term(term):
        """whether the term is valid"""
        return Rule.is_nonterminal(term) or Rule.is_terminal(term)
    def is_epsilon(self):
        """check whether a Rule is epsilon"""
        return self.__rhs__ == [ 'epsilon' ]
    def terminals(self):
        """getter : terminals in this rule"""
        return self.__terminals__
    def nonterminals(self):
        """getter : nonterminals in this rule"""
        return self.__nonterminals__
    def lhs(self):
        """getter : lhs nonterminal in this rule"""
        return self.__lhs__
    def change_lhs(self, lhs):
        """setter : lhs nonterminal in this rule"""
        self.__lhs__ = lhs
    def rhs(self):
        """getter : list of rhs identifiers in this rule"""
        return self.__rhs__
    def rinsert(self, term):
        """insert a term in the rightmost position of rhs"""
        assert type(term) == str and Rule.is_valid_term(term)
        self.__rhs__.append(term)
    def linsert(self, term):
        """insert a term in the leftmost position of rhs"""
        assert type(term) == str and Rule.is_valid_term(term)
        self.__rhs__.insert(0, term)
    def rremove(self):
        """remove a term in the rightmost position of rhs"""
        assert self.__rhs__
        return self.__rhs__.pop()
    def lremove(self):
        """remove a term in the leftmost position of rhs"""
        assert self.__rhs__
        self.__rhs__.remove(self.__rhs__[0])

class CompleteRule:
    """a grammar rule for a nonterminal"""
    def __init__(self, lhs):
        self.__lhs__ = lhs
        self.__rules__ = set()
        self.__terminals__ = set()
        self.__nonterminals__ = { self.__lhs__ }
    def __iter__(self):
        return self.__rules__.__iter__()
    def __eq__(self, other):
        return self.__lhs__ == other.__lhs__ and \
            self.__rules__ == other.__rules__
    def __ne__(self, other):
        return not self.__eq__(other)
    def __str__(self):
        return ' | '.join([rule.__str__() for rule in self.__rules__])
    def __hash__(self):
        return self.__str__().__hash__()
    def add(self, rule):
        """add a rule"""
        if rule.lhs() != self.__lhs__:
            raise TypeError(
                'add a Rule of `%s` to a CompleteRule of `%s`' %\
                (rule.lhs(), self.__lhs__)
            )
        self.__rules__.add(rule)
        self.__terminals__.update(rule.terminals())
        self.__nonterminals__.update(rule.nonterminals())
        return self
    def terminals(self):
        """getter : terminals in all rules"""
        return self.__terminals__
    def nonterminals(self):
        """getter : nonterminals in all rules"""
        return self.__nonterminals__
    def lhs(self):
        """getter : lhs nonterminal in all rules"""
        return self.__lhs__
    def rules(self):
        """getter : all rules"""
        return self.__rules__
    def remove(self, rule):
        """remove a rule"""
        self.__rules__.remove(rule)

class Rules:
    """a container of all CompleteRule's"""
    def __init__(self):
        self.__rules__ = {}
        self.__terminals__ = set()
        self.__nonterminals__ = set()
    def __getitem__(self, lhs):
        self.__terminals__ = None
        self.__nonterminals__ = None
        return self.__rules__[lhs]
    def __setitem__(self, lhs, complete_rule):
        if not complete_rule:
            complete_rule = CompleteRule(lhs)
        self.__rules__[lhs] = complete_rule
        self.__terminals__ = self.terminals().\
            update(complete_rule.terminals())
        self.__nonterminals__ = self.nonterminals().\
            update(complete_rule.nonterminals())
        return self
    def __delitem__(self, key):
        del self.__rules__[key]
    def __len__(self):
        return len(self.__rules__)
    def __iter__(self):
        return self.__rules__.__iter__()
    def __str__(self):
        return '\n'.join([self[lhs].__str__() for lhs in self])
    def __hash__(self):
        return self.__str__().__hash__()
    def terminals(self):
        """getter : terminals in all rules"""
        if not self.__terminals__:
            self.__terminals__ = reduce(lambda x, y : x.union(y),
                [self[lhs].terminals() for lhs in self],
                set())
        return self.__terminals__
    def nonterminals(self):
        """getter : nonterminals in all rules"""
        if not self.__nonterminals__:
            self.__nonterminals__ = reduce(lambda x, y : x.union(y),
                [self[lhs].nonterminals() for lhs in self],
                set())
        return self.__nonterminals__
    def setdefault(self, lhs):
        """set default map value of lhs"""
        self.__rules__.setdefault(lhs, CompleteRule(lhs))
    def add(self, rule):
        """add a new Rule"""
        lhs = rule.lhs()
        self.setdefault(lhs)
        self[lhs].add(rule)

class LL1Parser:
    """a defined LL(1) CFG Parser"""
    def __init__(self, lexer, rules, precedences=None):
        """
        `rules` is a Rules, and `precedences` is a tuple or list
        where tokens are ordered from lowest to highest precedence

        e.g.    precedence = (
                    ('left', 'PLUS', 'MINUS'),
                    ('left', 'TIMES', 'DIVIDE'),
                )
        """
        self.__stream__ = None
        self.__lexer__ = lexer
        self.__rules__ = rules
        self.__precedences__ = precedences
    def parse(self, string):
        """parse the string"""
        self.__lexer__.set_string(string)
        self.__stream__ = TokenStream(self.__lexer__)

def yacc():
    """return a Parser"""
    import sys
    all_vars = sys._getframe(1).f_locals
    if 'lexer' not in all_vars:
        raise NotImplementedError(
            'Yacc need variable `lexer` but not defined'
        )
    lexer = all_vars['lexer']
    rules = Rules()
    precedences = None if 'precedences' not in all_vars \
        else all_vars['precedences']
    import inspect
    for func_name in all_vars:
        if not func_name.startswith('p_'):
            continue
        func = all_vars[func_name]
        if inspect.isfunction(func):
            raw_rule = func.__doc__
            if raw_rule.find('\'') != -1:
                raise SyntaxWarning(
                    'no single quote mark is allowed in grammar, but found \
                    `%s` in `%s`' % (raw_rule, func.__name__))
            rule = Rule(raw_rule, func)
            rules.setdefault(rule.lhs())
            rules[rule.lhs()].add(rule)
    tokens = set(all_vars['tokens'])
    for term in rules.terminals():
        if term not in tokens:
            raise NameError(
                'terminal `%s` not defined as a token' % term
            )
    return LL1Parser(lexer, rules, precedences)
