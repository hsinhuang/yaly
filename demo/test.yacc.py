import yaly.yacc as yacc

from cmm_lex import tokens, lexer

grammar = (
    "e  : t e'",
    "e' : PLUS t e'",
    "e' : epsilon",
    "t  : f t'",
    "t' : TIMES f t'",
    "t' : epsilon",
    "f  : LPAREN e RPAREN",
    "f  : ID",
)

parser = yacc.yacc()

while True:
    parser.parse(raw_input('>>> '))
