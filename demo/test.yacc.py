from cmm.lex import tokens, lexer

def p_1(p):
    'e : e PLUS t'
    return p

def p_2(p):
    'e : t'
    return p

def p_3(p):
    't : t TIMES f'
    return p

def p_4(p):
    't : f'
    return p

def p_5(p):
    'f : LPAREN e RPAREN'
    return p

def p_6(p):
    'f : ID'
    return p
