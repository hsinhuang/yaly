%loadpy yacc.py

r0 = Rule('a : A B C a', 0)
r1 = Rule('a : A B a', 1)
r2 = Rule('a : A a', 2)

rules = Rules()
rules.add(r0)
rules.add(r1)
rules.add(r2)

a = rules['a']

common_factor = a.common_factor()

print common_factor
