#!/usr/bin/env python
# coding:utf-8

"""yacc definition for C--"""

from yaly.yacc import *
from cmm_lex import lexer, tokens

def p_prog_epsilon():
    'prog : epsilon'
    return None

def p_prog_frag_prog():
    'prog : frag prog'
    return None

def p_frag_dcl():
    'frag : dcl SEMI'
    return None

def p_frag_func():
    'frag : func'
    return None

def p_dcl_type():
    'dcl : type var_decl var_decls'
    return None

def p_dcl_extern():
    'dcl : EXTERN intern_dcl'
    return None

def p_dcl_intern():
    'dcl : intern_dcl'
    return None

def p_var_decls_ep():
    'var_decls : epsilon'
    return None

def p_var_decls_comma():
    'var_decls : COMMA var_decl var_decls'
    return None

def p_intern_type():
    'intern_dcl : type func_decl'
    return None

def p_intern_void():
    'intern_dcl : VOID func_decl'
    return None

def p_func_decls_id():
    'func_decl : ID LPAREN parm_types RPAREN func_decls'
    return None

def p_func_decls_ep():
    'func_decls : epsilon'
    return None

def p_func_decls_comma():
    'func_decls : COMMA ID LPAREN parm_types RPAREN func_decls'
    return None

def p_var_decl_id():
    'var_decl : ID'
    return None

def p_var_decl_id_lb():
    'var_decl : ID LBRACKET INTCON RBRACKET'
    return None

def p_type_char():
    'type : CHAR'
    return None

def p_type_int():
    'type : INT'
    return None

def p_param_void():
    'parm_types : VOID'
    return None

def p_param_type_id_more():
    'parm_types : type ID more_param_types'
    return None

def p_param_type_id_lb():
    'parm_types : type ID LBRACKET RBRACKET more_param_types'
    return None

def p_morepa_ep():
    'more_param_types : epsilon'
    return None

def p_morepa_comma_more():
    'more_param_types : COMMA type ID more_param_types'
    return None

def p_morepa_comma_lb():
    'more_param_types : COMMA type ID LBRACKET RBRACKET more_param_types'
    return None

def p_func_type():
    'func : type ID LPAREN parm_types RPAREN LBRACE in_func_decls stmts RBRACE'
    return None

def p_func_void():
    'func : VOID ID LPAREN parm_types RPAREN LBRACE in_func_decls stmts RBRACE'
    return None

def p_infds_ep():
    'in_func_decls : epsilon'
    return None

def p_infds_inf():
    'in_func_decls : in_func_decl SEMI in_func_decls'
    return None

def p_infd_type():
    'in_func_decl : type var_decl var_decls'
    return None

def p_stmts_ep():
    'stmts : epsilon'
    return None

def p_stmts_stmt():
    'stmts : stmt stmts'
    return None

def p_stmt_if():
    'stmt : IF LPAREN expr RPAREN stmt'
    return None

def p_stmt_if_else():
    'stmt : IF LPAREN expr RPAREN stmt ELSE stmt'
    return None

def p_stmt_while():
    'stmt : WHILE LPAREN expr RPAREN stmt'
    return None

def p_stmt_for():
    'stmt : FOR LPAREN assg SEMI stmt_for_2'
    return None

def p_stmt_for2():
    'stmt : FOR LPAREN SEMI stmt_for_2'
    return None

def p_stmt_for3():
    'stmt_for_2 : expr stmt_for_3 SEMI'
    return None

def p_for2():
    'stmt_for_2 : stmt_for_3 SEMI'
    return None

def p_for3_assg():
    'stmt_for_3 : assg RPAREN stmt'
    return None

def p_for3():
    'stmt_for_3 : RPAREN stmt'
    return None

def p_return_exp():
    'stmt : RETURN expr SEMI'
    return None

def p_return():
    'stmt : RETURN SEMI'
    return None

def p_stmt_assg():
    'stmt : assg SEMI'
    return None

def p_stmt_id():
    'stmt : ID LPAREN exprs RPAREN SEMI'
    return None

def p_stmt_lb():
    'stmt : LBRACE stmts RBRACE'
    return None

def p_stmt_semi():
    'stmt : SEMI'
    return None

def p_exprs_ep():
    'exprs : epsilon'
    return None

def p_exprs_exp():
    'exprs : expr more_exprs'
    return None

def p_moreex_ep():
    'more_exprs : epsilon'
    return None

def p_moreex_comma():
    'more_exprs : COMMA expr more_exprs'
    return None

def p_assg_as():
    'assg : ID ASSIGN expr'
    return None

def p_assg_lb():
    'assg : ID LBRACKET expr RBRACKET ASSIGN expr'
    return None

def p_expr_mi():
    'expr : MINUS expr'
    return None

def p_expr_no():
    'expr : NOT expr'
    return None

def p_expr_bi():
    'expr : expr binop expr'
    return None

def p_expr_re():
    'expr : expr relop expr'
    return None

def p_expr_lo():
    'expr : expr logical_op expr'
    return None

def p_expr_id():
    'expr : ID'
    return None

def p_expr_fn():
    'expr : ID LPAREN exprs RPAREN'
    return None

def p_expr_fn2():
    'expr : ID LBRACKET expr RBRACKET'
    return None

def p_expr_exp():
    'expr : LPAREN expr RPAREN'
    return None

def p_expr_int():
    'expr : INTCON'
    return None

def p_expr_char():
    'expr : CHARCON'
    return None

def p_expr_str():
    'expr : STRINGCON'
    return None

def p_binop_pl():
    'binop : PLUS'
    return None

def p_binop_mi():
    'binop : MINUS'
    return None

def p_binop_ti():
    'binop : TIMES'
    return None

def p_binop_di():
    'binop : DIVIDE'
    return None

def p_relop_eq():
    'relop : EQ'
    return None

def p_relop_ne():
    'relop : NE'
    return None

def p_relop_le():
    'relop : LE'
    return None

def p_relop_lt():
    'relop : LT'
    return None

def p_relop_ge():
    'relop : GE'
    return None

def p_relop_gt():
    'relop : GT'
    return None

def p_log_and():
    'logical_op : AND'
    return None

def p_log_or():
    'logical_op : OR'
    return None

if __name__ == '__main__':
    parser = yacc()
    print parser.rules()
