#!/usr/bin/env python
# coding:utf-8

"""syntax analysis"""

__EPSILON__ = 'epsilon'
__END__ = '$'

class Rule:
    """
    a single rule for a nonterminal, and maybe this nonterminal
    has other rules
    """
    def __init__(self, rule_spec, func=None):
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
        return term.isupper() or term == __EPSILON__
    @staticmethod
    def is_nonterminal(term):
        """whether the term is nonterminal"""
        return term.islower() and term != __EPSILON__
    @staticmethod
    def is_valid_term(term):
        """whether the term is valid"""
        return Rule.is_nonterminal(term) or Rule.is_terminal(term)
    def is_epsilon(self):
        """check whether a Rule is epsilon"""
        return self.__rhs__ == [ __EPSILON__ ]
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
        self.__first__ = set()
        self.__follow__ = set()
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
        self.__first__ = set()
        self.__follow__ = set()
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
        self.__first__ = set()
        self.__follow__ = set()
    def first(self, rules):
        """return FIRST set of term"""
        if not self.__first__:
            first_set = set()
            for rule in self:
                if rule.is_epsilon():
                    first_set.add(__EPSILON__)
                else:
                    rule_rhs = rule.rhs()
                    end = True
                    for term in rule_rhs:
                        first_set.update(rules.first(term))
                        if __EPSILON__ not in rules.first(term):
                            end = False
                            break
                    if end:
                        first_set.add(__EPSILON__)
            self.__first__ = first_set
        return self.__first__

class Rules:
    """a container of all CompleteRule's"""
    def __init__(self):
        self.__rules__ = {}
        self.__terminals__ = set()
        self.__nonterminals__ = set()
        self.__start__ = None # CompleteRule
        self.__follows__ = {}
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
    def is_start(self, term):
        """check whether the term is a start symbol"""
        if not self.__start__:
            return False
        return self.__start__.lhs() == term
    def start_symbol(self):
        """getter : start symbol"""
        if not self.__start__:
            return None
        return self.__start__.lhs()
    def set_start_rule(self, rule):
        """setter : start symbol"""
        self.__start__ = self[rule.lhs()]
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
    def first(self, term):
        """return FIRST set of term"""
        if type(term) == tuple or type(term) == list:
            if not term:
                return set()
            if Rule.is_nonterminal(term[0]) and \
                __EPSILON__ in self.first(term[0]):
                return self.first(term[0]).union(self.first(term[1:]))
            else:
                return self.first(term[0])
        if Rule.is_terminal(term):
            return { term }
        import copy
        return copy.deepcopy(self[term].first(self))
    def follows(self):
        """calculate FOLLOW sets of all nonterminals"""
        assert self.__start__
        new_follows = {}
        for term in self:
            new_follows.setdefault(term, set())
            self.__follows__.setdefault(term, set())
        new_follows[self.start_symbol()].add(__END__)
        for nonterm in self:
            com_rule = self[nonterm]
            for rule in com_rule:
                rule_rhs = rule.rhs()
                for i, term in enumerate(rule_rhs):
                    if Rule.is_terminal(term):
                        continue
                    j = i+1
                    while j < len(rule_rhs):
                        end = True
                        first_beta = self.first(rule_rhs[j])
                        if __EPSILON__ in first_beta:
                            end = False
                            first_beta.remove(__EPSILON__)
                        new_follows[term].update(first_beta)
                        if end:
                            break
                        else:
                            j += 1
                    if j == len(rule_rhs):
                        new_follows[term].update(self.__follows__[rule.lhs()])
        return new_follows
    def follow(self, term):
        """return FOLLOW set of term"""
        assert Rule.is_nonterminal(term)
        if not self.__follows__:
            new_follows = self.follows()
            while new_follows != self.__follows__:
                self.__follows__ = new_follows
                new_follows = self.follows()
        import copy
        return copy.deepcopy(self.__follows__[term])

class LL1Parser:
    """a defined LL(1) CFG Parser"""
    def __init__(self, lexer, rules):
        """
        `rules` is a Rules
        """
        self.__lexer__ = lexer
        self.__rules__ = rules
        self.__parsing_table__ = {}
        for nonterm in self.__rules__.nonterminals():
            self.__parsing_table__.setdefault(nonterm, {})
            self.__parsing_table__[nonterm].setdefault(__END__, set())
            for term in self.__rules__.terminals():
                self.__parsing_table__[nonterm].setdefault(term, set())
        for nonterm in self.__rules__:
            com_rule = self.__rules__[nonterm]
            for rule in com_rule:
                if __EPSILON__ in self.__rules__.first(rule.rhs()):
                    for term in self.__rules__.follow(rule.lhs()):
                        if Rule.is_terminal(term) and term != __EPSILON__:
                            self.__parsing_table__[nonterm][term].add(rule)
                for term in self.__rules__.first(rule.rhs()):
                    if Rule.is_terminal(term) and term != __EPSILON__:
                        self.__parsing_table__[nonterm][term].add(rule)
    def parse(self, string):
        """parse the string"""
        self.__lexer__.set_string(string)
        input_stack = list(reversed([ token.lexical_unit() \
            for token in self.__lexer__.get_next_token() ] + [__END__]))
        grammar_stack = [self.__rules__.start_symbol()]
        while grammar_stack:
            X, a = grammar_stack[-1], input_stack[-1]
            if X == a or (X == __EPSILON__ and a == __END__):
                print 'Match =>', a
                grammar_stack.pop()
                input_stack.pop()
            elif Rule.is_terminal(X):
                raise ValueError('parse stop: `%s` is terminal' % X)
            elif not self.__parsing_table__[X][a]:
                raise ValueError('parse stop: no rule for `%s`, `%s`' %\
                    (X, a))
            elif len(self.__parsing_table__[X][a]) > 1:
                raise ValueError('parse stop: ambiguious `%s`, `%s`' %\
                    (X, a))
            else:
                rule = list(self.__parsing_table__[X][a])[0]
                print 'Using =>', rule
                grammar_stack.pop()
                if not rule.is_epsilon():
                    grammar_stack += list(reversed(rule.rhs()))
    def __print_parsing_table__(self):
        from prettytable import PrettyTable
        table = PrettyTable(
            [''] + [term for term in self.__rules__.terminals()] + [__END__]
        )
        for nonterm in self.__rules__.nonterminals():
            row = [ nonterm ]
            for term in self.__rules__.terminals():
                row.append('; '.join([str(rule) \
                    for rule in self.__parsing_table__[nonterm][term]])
                )
            row.append('; '.join([str(rule) \
                for rule in self.__parsing_table__[nonterm][__END__]])
            )
            table.add_row(row)
        print table

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
    if 'grammar' not in all_vars:
        raise NotImplementedError(
            'Yacc need variable `grammar` but not defined'
        )
    grammar = all_vars['grammar']
    first = True
    for raw_rule in grammar:
        rule = Rule(raw_rule, None)
        rules.setdefault(rule.lhs())
        rules[rule.lhs()].add(rule)
        if first:
            rules.set_start_rule(rule)
            first = False
    tokens = set(all_vars['tokens'])
    for term in rules.terminals():
        if term != __EPSILON__ and term not in tokens:
            raise NameError(
                'terminal `%s` not defined as a token' % term
            )
    return LL1Parser(lexer, rules)
