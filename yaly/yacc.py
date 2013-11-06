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
        `rule_spec` is a string which specifies the rule

        format: `lhs : t1 t2 t3 ...`
        """
        self.__func__ = func
        rp_rule = rule_spec.split(':')
        if len(rp_rule) != 2:
            raise SyntaxError(
                'Syntax rule `%s` not valid' % rule_spec
            )
        self.__lhs__, rhs = rp_rule[0].strip(), rp_rule[1].strip()
        import re
        self.__rhs__ = re.split(r'\s+', rhs)
        if not all([s.isupper() or s.islower() \
            for s in self.__rhs__] + [self.__lhs__.islower()]):
            raise SyntaxError(
                'terminals in rules should be uppercase, \
                while nonterminals in rules should be lowercase'
            )
        self.__nonterminals__ = { self.__lhs__ }
        self.__terminals__ = set()
        for _id in self.__rhs__:
            if _id.islower():
                self.__nonterminals__.add(_id)
            else:
                self.__terminals__.add(_id)
        self.__rule_spec__ = ' '.join([self.__lhs__, ':'] + self.__rhs__)
    def __str__(self):
        return self.__rule_spec__
    def __eq__(self, other):
        return self.__lhs__ == other.__lhs__ and \
            self.__rhs__ == other.__rhs__
    def __ne__(self, other):
        return not self.__eq__(other)
    def __hash__(self):
        return self.__rule_spec__.__hash__()
    def terminals(self):
        """getter : terminals in this rule"""
        return self.__terminals__
    def nonterminals(self):
        """getter : nonterminals in this rule"""
        return self.__nonterminals__
    def lhs(self):
        """getter : lhs nonterminal in this rule"""
        return self.__lhs__
    def rhs(self):
        """getter : list of rhs identifiers in this rule"""
        return self.__rhs__
    def rinsert(self, term):
        """insert a term in the rightmost position of rhs"""
        assert type(term) == str and (term.isupper() or term.islower())
        self.__rhs__.append(term)
    def linsert(self, term):
        """insert a term in the leftmost position of rhs"""
        assert type(term) == str and (term.isupper() or term.islower())
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
        return self.__rules__
    def __eq__(self, other):
        return self.__lhs__ == other.__lhs__ and \
            self.__rules__ == other.__rules__
    def __ne__(self, other):
        return not self.__eq__(other)
    def __str__(self):
        return ' | '.join([rule.__str__() for rule in self.__rules__])
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

class Rules:
    """a container of all CompleteRule's"""
    EPSILON = 'epsilon'
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
        self.__terminals__.update(complete_rule.terminals())
        self.__nonterminals__.update(complete_rule.nonterminals())
        return self
    def __delitem__(self, key):
        del self.__rules__[key]
    def __len__(self):
        return len(self.__rules__)
    def __iter__(self):
        return self.__rules__.__iter__()
    def __str__(self):
        return '\n'.join([self[lhs].__str__() for lhs in self])
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
        if lhs not in self:
            self.setdefault(lhs)
        self[lhs].add(rule)
    def strip_im_left_recr__(self, complete_rule):
        """
        strip all the immediate left recursion in the CompleteRule

        return a two-element tuple containing stripped CompleteRule
        """
        left_recr = []
        non_left_recr = []
        for rule in complete_rule:
            if rule.rhs()[0] == complete_rule.lhs():
                left_recr.append(rule)
            else:
                non_left_recr.append(rule)
        lhs_ = complete_rule.lhs() + '\''
        while lhs_ in self.nonterminals():
            lhs_ += '\''
        c_rule_a = CompleteRule(complete_rule.lhs())
        c_rule_a_ =CompleteRule(lhs_)
        import copy
        for beta in non_left_recr:
            if len(beta) == 1 and beta[0] == Rules.EPSILON:
                betaa_ = copy.deepcopy(beta)
                betaa_.rinsert(lhs_)
                c_rule_a.add(betaa_)
            else:
                rules[lhs].append(beta+[lhs_])
        rules[lhs_] = [ ['epsilon'] ]
        for a_alpha in left_recr:
            rules[lhs_].append(a_alpha[1:]+[lhs_])
        return rules
    def strip_left_recr(self):
        """
        strip all the left recursion in the rules

        return a new rule
        """
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
                ai_ = __strip_im_left_recr__((ai_lhs, new_ai_rhs), nonterminals)
                for lhs in ai_:
                    if lhs not in nonterminals:
                        nonterminals.append(lhs)
                        rules[lhs] = [None, ai_[lhs]]
                    else:
                        rules[lhs] = [rules[ai_lhs][0], ai_[lhs]]

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
        self.__terminals__ = terminals
        self.__nonterminals__ = nonterminals
        len_nont = 0
        new_len_nont = len(self.__nonterminals__)
        while True:
            for i in range(len_nont, new_len_nont):
                self.__extract_left_common_factor__(self.__nonterminals__[i])
            len_nont = new_len_nont
            new_len_nont = len(self.__nonterminals__)
            if new_len_nont == len_nont:
                break
    @staticmethod
    def __max_leading_intersection__(list1, list2):
        """return then max leading intersection of list1 and list2"""
        if len(list1) > len(list2):
            list1, list2 = list2, list1
        for i in range(len(list1), -1, -1):
            if list1[:i] == list2[:i]:
                return list1[:i]
        return []
    def __max_lcf__(self, lhs):
        """
        find max left common factor of lhs, if thers's none,
        return empty list
        """
        common_factor = []
        all_rhs = self.__rules__[lhs][1]
        for i in range(len(all_rhs)):
            for j in range(i+1, len(all_rhs)):
                lcf = LL1Parser.__max_leading_intersection__(
                    all_rhs[i], all_rhs[j]
                )
                if len(lcf) > len(common_factor):
                    common_factor = lcf
        return common_factor
    def __extract_left_common_factor__(self, lhs):
        """
        extract left common factor of lhs
        """
        alpha = self.__max_lcf__(lhs)
        while alpha:
            len_alpha = len(alpha)
            lhs_ = lhs + '\''
            while lhs_ in self.__nonterminals__:
                lhs_ += '\''
            new_all_rhs1 = [alpha+[lhs_]]
            all_rhs_1 = []
            for rhs in self.__rules__[lhs][1]:
                if alpha == rhs[:len_alpha]:
                    all_rhs_1.append(rhs[len_alpha:] \
                        if len_alpha < len(rhs) else ['epsilon'])
                else:
                    new_all_rhs1.append(rhs)
            self.__rules__[lhs_] = [None, all_rhs_1]
            self.__nonterminals__.append(lhs_)
            self.__rules__[lhs][1] = new_all_rhs1
            alpha = self.__max_lcf__(lhs)
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
    for func in all_vars:
        if inspect.isfunction(func) and func.__name__.startswith('p_'):
            raw_rule = func.__doc__
            rule = Rule(raw_rule, func)
            rules.setdefault(rule.lhs())
            rules[rule.lhs()].add(rule)
    tokens = set(all_vars['tokens'])
    for term in rules.terminals():
        if term not in tokens:
            raise NameError(
                'terminal `%s` not defined as a token' % term
            )
    __strip_left_recr__(rules, rules.nonterminals())
    return LL1Parser(lexer, rules, precedences)
