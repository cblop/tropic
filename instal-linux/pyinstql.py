#!/usr/bin/python

#------------------------------------------------------------------------
# REVISION HISTORY
# add new entries here at the top tagged by date and initials
# 20130401 GDB: added a definition of disjunction that allows for comma
# 20130325 GDB: modified the 'show' option to include 'occurred' and 'holdsat'
# 20130225 GDB: added function to flatten the nested list into a single flat list
# 20130222 GDB: removed the conditionCounter function 
# 20130220 GDB: added functions for 'observe' and 'show'
# 20130220 GDB: added code to accept input file at command line using the -i option
#------------------------------------------------------------------------

from __future__ import print_function
import re
import sys
import ply.yacc as yacc
import argparse # GDB added this

sys.path.insert(0,"../..")

if sys.version_info[0] >= 3:
    raw_input = input

# class instalparserclass():

instal_output = sys.stdout

def instql_print(p): print(p,file=instql_output)

def instql_error(p): print(p,file=sys.stderr)

def instql_warn(p): print(p,file=sys.stderr)

#show_debug = False
show_debug = True

def debug(*p):
    if show_debug: print(p)

#------------------------------------------------------------------------
# LEXER + PARSER for instql

reserved = {
    'and'         : 'AND',
    'not'         : 'NOT',
    'or'          : 'OR',
    'while'       : 'WHILE',
    'after'       : 'AFTER',
    'holds'       : 'HOLDS',
    'happens'     : 'HAPPENS',
    'condition'   : 'CONDITION',
    'constraint'  : 'CONSTRAINT',
    'violates'    : 'VIOLATES',         #GDB added
    'show'        : 'SHOW',		#GDB added	
    'observe'     : 'OBSERVE'		# GDB added
}

tokens =  ['NAME','VARIABLE','INTEGER','LPAR','RPAR','SEMI','COMMA','COLON'] + list(reserved.values())

# Tokens

t_SEMI  = r';'
t_COMMA  = r','
t_COLON  = r':'
t_LPAR  = r'\('
t_RPAR  = r'\)'

def t_NAME(t):
    r'[a-z][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value,'NAME')    # Check for reserved words
    return t

def t_VARIABLE(t):
    r'[A-Z][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value,'VARIABLE')    # Check for reserved words
    return t

def t_INTEGER(t):
    # note: numbers are parsed but not converted into integers
    r'\d+'
    # t.value = int(t.value)
    return t

t_ignore = " \t\r"

# Comments
def t_COMMENT(t):
    r'%.*'
    pass
    # No return value. Token discarded

def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")

def t_error(t):
    instql_error("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

# Build the lexer
import ply.lex as lex
lex.lex()

ast = []

def p_instqlExpr(p): #GDB added observe, show
    """ instqlExpr : 
        instqlExpr : instqlExpr conditionDecl
        instqlExpr : instqlExpr constraint
        instqlExpr : instqlExpr observe
        instqlExpr : instqlExpr show
    """
    global ast
#    debug("instqlExpr:")
    if len(p)<2:
        ast = []
        p[0] = []
    else:
        ast = [p[2]] + p[1]
        p[0] = ast

def p_variable_list(p):
    """ variable_list :
        variable_list : VARIABLE
        variable_list : variable_list COMMA VARIABLE
    """
#    debug("variable_list:")
    if len(p)>2: p[0] = p[1] + [p[3]] # general case
    elif len(p)==2: p[0] = [p[1]]     # unary case
    # nullary case

def p_identifier(p):
    # second rule not in grammar, but derives from example
    #GDB: added the third rule
    """ identifier : NAME
        identifier : VARIABLE
        identifier : INTEGER
        identifier : NAME LPAR variable_list RPAR
        identifier : NAME LPAR NAME RPAR
    """
#    debug("identifier:")
    if len(p)>4:
        p[0] = [p[1],p[3]]
    else:
        p[0] = p[1]
        
#GDB: added the second rule 
def p_happens(p):
    """ happens : HAPPENS LPAR identifier RPAR
        happens : HAPPENS LPAR identifier COMMA identifier RPAR
    """
#    debug("happens:")
    if len(p)>5:
        p[0] = ['HAPPENS',p[3],p[5]]
    else:
        p[0] = ['HAPPENS',p[3]]

def p_violates(p):
    """ violates : VIOLATES LPAR identifier RPAR
        violates : VIOLATES LPAR identifier COMMA identifier RPAR
    """
#    debug("violates:")
    if len(p)>5:
        p[0] = ['VIOLATES',p[3],p[5]]
    else:
        p[0] = ['VIOLATES',p[3]]
    
def p_holds(p):
    """ holds : HOLDS LPAR identifier RPAR
        holds : HOLDS LPAR identifier COMMA identifier RPAR
    """
#    debug("happens:")
    if len(p)>5:
        p[0] = ['HOLDS',p[3],p[5]]
    else:
#    debug("holds:")
        p[0] = ['HOLDS',p[3]]

def p_literal(p): 
    """ literal : NOT happens
        literal : NOT holds
        literal : happens
        literal : holds
        literal : violates
    """ 
#    debug("literal:")
    if len(p)>2:
        p[0] = ['NOT',p[2]]
    else:
        p[0] = p[1]

def p_whileExpr(p):
    """ whileExpr : literal
        whileExpr : literal WHILE whileExpr
    """
#    debug("whileExpr:")
    if len(p)>3:
        p[0] = ['WHILE',p[1],p[3]]
    else:
        p[0] = p[1]

def p_after(p):
    """ after : AFTER
        after : AFTER LPAR INTEGER RPAR
    """
#    debug("after:",len(p))
    if len(p)>2:
        debug("after:",p[3])
        p[0] = ['AFTER',p[3]]
    else:
#        debug("after:")
        p[0] = 'AFTER'

def p_afterExpr(p):
    """ afterExpr : whileExpr
        afterExpr : whileExpr after afterExpr
    """
#    debug("afterExpr:")
    if len(p)>3:
        if p[2]=='AFTER':
            p[0] = [p[2],p[1],p[3]]
        else:
            p[0] = [p[2][0],p[2][1],p[1],p[3]]
    else:
        p[0] = p[1]

def p_conditionLiteral(p):
    """ conditionLiteral : NOT identifier
        conditionLiteral : identifier
        conditionLiteral : identifier LPAR identifier COMMA identifier RPAR
    """
#    debug("conditionLiteral:")
    if len(p)>2:
        p[0] = ['NOT',p[2]]
    else:
        p[0] = p[1]

def p_term(p):
    """ term : afterExpr
        term : conditionLiteral
    """
#    debug("term:")
    p[0] = p[1]

def p_conjunction(p):
    """ conjunction : term
        conjunction : conjunction AND term
    """
#    debug("conjunction:")
    if len(p)>3:
        p[0] = ['AND',p[1],p[3]]
    else:
        p[0] = p[1]
#GDB: added a rule that accepts comma
def p_disjunction(p):
    """ disjunction : conjunction
        disjunction : disjunction COMMA conjunction 
        disjunction : disjunction OR conjunction
    """
#    debug("disjunction:")
    if len(p)>3:
        p[0] = ['OR',p[1],p[3]]
    else:
        p[0] = p[1]

def p_conditionDecl(p):
    """ conditionDecl : CONDITION term COLON disjunction SEMI
    """
#    debug("conditionDecl:")
    p[0] = ['CONDITION',p[2],p[4]]

def p_constraint(p):
    """ constraint : CONSTRAINT disjunction SEMI
    """
#    debug("constraint:")
    p[0] = ['CONSTRAINT',p[2]]

# GDB: functions for observe and show
def p_observe(p):
    """ observe : OBSERVE disjunction SEMI
    """
#    debug("observe:")
    p[0] = ['OBSERVE',p[2]]

def p_show(p):
    """ show : SHOW disjunction SEMI
    """
#    debug("show:")
    p[0] = ['SHOW',p[2]]
    
def p_error(p):
    if p:
        debug("Syntax error at '%s'" % p.value)
    else:
        debug("Syntax error at EOF")

#------------------------------------------------------------------------

def instql_parse(d):
    yacc.yacc()
    yacc.parse(d)

def id2string(p): #GDB: modified
#    debug("is2string: p = ",p)
    if isinstance(p,str): return p
    args = p[1]
    r=''
    if isinstance(args,str):
        r=p[0]+'('+args+')'
    else:
        r=p[0]+'('+args[0]+','+args[1]+')'
    #if len(args)==0:
    #    r=p[0]
    #elif len(args)==1:
    #    r=p[0]+'('+args[0]+')'
    #else:
    #    r='('+args[0]
    #    for x in args[1:]: r=r+','+x
    #    r=p[0]+r+')'
    return r

instantCounter = 0

def newInstant():
    global instantCounter
    instantCounter+=1
    return `instantCounter`
    
def thisInstant():
    global instantCounter
#    debug('thisInstant =',instantCounter)
    return `instantCounter`
    
def flatten(L): #GDB: Added this function to flatten out nested lists
    if not L:
        return L
    elif isinstance(L,str):
        return L
    elif type(L[0]) == type([]):
        return flatten(L[0]) + flatten(L[1:])
    else:
        return [L[0]] + flatten(L[1:])
        
def instql_print(t):
    #debug("instql_print: ",t)
    newInstant() 
    if t==[]: return ""
    k=t[0]
    a=t[1:]

    if k=='WHILE':
        # not convinced that handling of instant is correct
        global instantCounter
        z = instantCounter
        r = instql_print(a[0])
        instantCounter = z
        for x in a[1:]: r += ',' + instql_print(x)
        return r
    if k=='AFTER': #GDB: modified to handle instants correctly
        d = ''
        if (len(a)==3):
            d = a[0]
            a = a[1:]
            r = instql_print(a[0])
            for x in a[1:]:
                z = thisInstant()
                r += ',' + instql_print(x) + (
                    ',after({i1},{i2},{d})'
                    .format(i1='I'+z,i2='I'+thisInstant(),d=d))
        else:
            r = instql_print(a[0])
            for x in a[1:]:
                z = thisInstant()
                w = instql_print(x)
                r += ',' + w + (
                    ',after({i1},{i2})'
                    .format(i1='I'+z,i2='I'+str(instantCounter)))
                instantCounter = z
                
        return r
    
    if k=='HAPPENS':  #GDB: modeified for parameterisation
        if len(a)>1:
            return('occurred({ev},{inst}),event({ev}))'
               .format(ev=a[0],inst=a[1]))
        else:
            return('occurred({ev},{inst}),event({ev}),instant({inst})'
               .format(ev=a[0],inst='I'+thisInstant()))

    if k=='VIOLATES': #GDB: Added
        if len(a)>1:
            return('occurred(viol({ev}),{inst}),event({ev})))'
               .format(ev=a[0],inst=a[1]))
        else:
            return('occurred(viol({ev}),{inst}),event({ev}),instant({inst})))'
               .format(ev=a[0],inst='I'+thisInstant()))
                    
    if k=='HOLDS':  #GDB: Modified for parameterisation
        if len(a)>1:
            if a[1] == 'F':
                return('holdsat({f1},{inst}),ifluent({f1}),final({inst}))'
               .format(f1=a[0],inst=a[1]))
            else:
                return('holdsat({f1},{inst}),ifluent({f1}))'
                       .format(f1=a[0],inst=a[1]))
        else:
            return('holdsat({fl},{inst}),ifluent({fl}),instant({inst})'
               .format(fl=a[0],inst='I'+thisInstant()))
    if k=='NOT':
        return('not {pred}'
               .format(pred=instql_print(a[0])))
    if k=='OR':
        return [instql_print(x) for x in a]
    if k=='AND':
        r = instql_print(a[0])
        for x in a[1:]: r += ',' + instql_print(x)
        return r
    if k=='CONDITION':
#        debug('condition',a)
        r = ''
        s = instql_print(a[1])
        f = flatten(s)
        # check for string or list
        if isinstance(f,str):
            r = ('{name} :- {body}.\n'
                 .format(name=id2string(a[0]),body=f))
        else:
            for x in f:
                r += ('{name} :- {body}.\n'
                      .format(name=id2string(a[0]),body=x))
        return r
    if k=='CONSTRAINT': # modified by GDB
#        debug('constraint',a)
        r = ''
        s = instql_print(a[0])
        f = flatten(s)
        if isinstance(f,str): # check for string or list
            if (f[0:3] == 'not'):
                r = (':- {body}.\n'
                 .format(body=f[3:]))
            else:
                r = (':- not {body}.\n'
                 .format(body=f))
        else:
            for x in f:
                if (x[0:3] == 'not'):
                    r += (':- {body}.\n'
                     .format(body=x[3:]))
                else:
                    r += (':- not {body}.\n'
                       .format(body=x))
        return r

    # GDB: prints the observed events
    if k=='OBSERVE':
        r = ''
        s = instql_print(a[0])
        f = flatten(s)
        # check for string or list
        if isinstance(f,str):
            instantCounter = 0
            r = ('observed({ev}, {inst}).\n'
                 .format(ev=f, inst=thisInstant()))
              #   .format(ev=a[0], inst=thisInstant()))
        else:
            instantCounter = 0
            for x in f:
                r += ('observed({ev}, {inst}).\n'
                             .format(ev=x, inst=thisInstant()))   
                 #.format(ev=a[0], inst=thisInstant()))
                instantCounter+=1
        return r
    # GDB: prints the show conditions
    if k=='SHOW':
#        debug('show',a)
        r = ''
        r = '#hide.\n'
        s = instql_print(a[0])
        f = flatten(s)
        if isinstance(f,str):
            #debug('This is f:',f)
            if f == 'events':
                r += ('#show({ev}).\n'
                      .format(ev='occurred(E,I)'))
            elif f == 'states':
                r += ('#show({ev}).\n'
                      .format(ev='holdsat(F,I)'))
            else:
                r += ('#show({ev}).\n'
                     .format(ev=f))
        else:
            for x in f:
                if x == 'events':
                    r += ('#show({ev}).\n'
                          .format(ev='occurred(E,I)'))
                elif x == 'states':
                    r += ('#show({ev}).\n'
                          .format(ev='holdsat(F,I)'))
                else:
                    r += ('#show({ev}).\n'
                       .format(ev=x))
        return r
       
    
    return id2string(t)

def instql_to_asp(instql):
	instql_parse(instql)
	ast.reverse()
	output = ""
	for x in ast:
		output += instql_print(x)
	return output

if __name__ == "__main__":
	#GDB 20130220: code for file input at command line
	parser = argparse.ArgumentParser()
	parser.add_argument("-i","--input-file")
	args = parser.parse_args()

	inp = open(args.input_file,'r')

	document = " "

	if args.input_file: document = inp.read(-1)
	else: document = sys.stdin.read(-1)
	#debug("input: ",document)
	instql_to_asp(document)

	    
