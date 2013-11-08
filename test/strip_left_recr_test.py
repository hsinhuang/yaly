r0 = Rule('s : q C', 0)
r1 = Rule('s : C', 1)
r2 = Rule('q : r B', 2)
r3 = Rule('q : B', 3)
r4 = Rule('r : s A', 4)
r5 = Rule('r : A', 5)

rules = Rules()
rules.add(r0)
rules.add(r1)
rules.add(r2)
rules.add(r3)
rules.add(r4)
rules.add(r5)

print rules

new_rules = rules.strip_left_recr()
