#------------------------------------------------------------------------
# VERSION TWO REVISION HISTORY:
# 20140618 JAP: removed ) that caused parse error in initiation of null events
# 20140601 TL: corrected other aspects regarding noninertial fluents
# 20140528 TL: corrected noninertial initiation to holdsat from initiated
# 20140528 TL: merged with the missing changes. 
# 20140131 TL: add time condition to generation rules 
# 20131229 TL: obligation now can have fluent as the obliged condition as well. e.g. obl(fluent/event, d, v)
# 20131228 TL: obligation now can have fluent as deadline as well. e.g. obl(e, fluent/event, v)
# 20131218 TL: added fluent(F,In) for inertial, non-inertial and obligation fluents
# 20131218 TL: added function instal_print_constraints(mode) with mode passed by the option -m  
# 20131218 TL: added option '-m', s/S for single, c/C for composite
# 20131218 TL: added unknown and gap warning for unknown events. 
# 20131218 TL: appended inst-id as the 2nd argument of evtype, oblfluent 
# 20131218 TL: added handling of unknown events -- function instal_print_nullevent()
# 20131218 TL: changed initiation rule for non-inertial fluents
# 20131218 TL: appended inst-id as the second argument of ifluent
# 20131218 TL: appended inst-id as the third argument of holdsat,occurred,observed,initiated,terminated. 
#------------------------------------------------------------------------
# REVISION HISTORY
# add new entries here at the top tagged by date and initials
# 20130813 JAP: fixed bug in antecedent parsing of not terms
# 20130801 JAP: revised parsing of when to permit perm/pow on lhs
# 20130724 JAP: added == and != to condition parsing
#               major reorganization to allow fluents on lhs of rules
#               made crevent initially printing consistent with non cr case
# 20130207 JAP: class-ified the parser
# 20130205 JAP: created parser module (this file)
# COMMON HISTORY FOLLOWS:
# 20130205 JAP: code for unique naming + predicates in (noninertial) fluents
# 20130118 TL: bug fixed at printing of conditions for initially
# 20130117 JAP: added arity check for events in check_event etc.
# 20130117 JAP: added parsing and printing of conditions for initially
# 20121128 TL: fixed a bug of closing instal_output file.
# 20121128 JL,TL: fixed a bug to initiate obligation
# 20121124 JAP: code for -t option
# 20121121 TL: fixed a bug at instal_error of function getVar()
# 20121121 JAP: added p1 and p2 parameters and associated logic
# 20121121 JAP: packaged output formatting into functions
# 20121119 JAP: made error checking more careful in p_generates
# 20121118 JAP: code for -o option, instal_print, instal_error and instal_warn
# 20121115 JAP: code for -i option
# 20121115 JAP: added warning for undeclared obligations
# 20121115 JAP: code for -d option
# 20121115 JAP: code for command line arguments
# 20121115 TL: added code to handle use of undeclared obligations
# 20121114 JAP: started history and made up pre-history
# 20121114 JAP: Added standard prelude text and code to output it
# 20121108 TL: Fixed three bugs
#------------------------------------------------------------------------

from __future__ import print_function
# import re # JAP 20140618 pychecker reports not used
import sys
import ply.lex as lex
import ply.yacc as yacc

# import argparse

# sys.path.insert(0,"../..")

# if sys.version_info[0] >= 3:
#     raw_input = input

#------------------------------------------------------------------------
# LEXER for instal

class myLexer():

    # Build the lexer
    # def build(self,**kwargs):
    #    self.lexer = lex.lex(object=self, **kwargs)

    def __init__(self):
        self.lexer = lex.lex(module=self)

    reserved = {
        #    'and'         : 'AND',
        'create'      : 'CREATE',
        'dissolve'    : 'DISSOLVE',
        'event'       : 'EVENT',
        'exogenous'   : 'EXOGENOUS',
        'fluent'      : 'FLUENT',
        'generates'   : 'GENERATES',
        'if'          : 'IF',
        'in'          : 'IN',        # TL20140129
        'initially'   : 'INITIALLY',
        'initiates'   : 'INITIATES',
        'inst'        : 'INST',
        'institution' : 'INSTITUTION',
        'noninertial' : 'NONINERTIAL',
        'not'         : 'NOT',
        'obl'         : 'OBL',
        'obligation'  : 'OBLIGATION',
        'perm'        : 'PERM',
        'pow'         : 'POW',
        'terminates'  : 'TERMINATES',
        'type'        : 'TYPE',
        'viol'        : 'VIOL',
        'violation'   : 'VIOLATION',
        #    'with'        : 'WITH',
        'when'        : 'WHEN',
        }

    tokens =  ['NAME','TYPE_NAME','NUMBER','LPAR','RPAR','SEMI','COMMA','EQUALS','NOTEQUAL'] + list(reserved.values())

    # Tokens

    t_SEMI  = r';'
    t_COMMA  = r','
    t_LPAR  = r'\('
    t_RPAR  = r'\)'
    t_EQUALS = r'=='
    t_NOTEQUAL = r'!='

    def t_NAME(self,t):
        r'[a-z][a-zA-Z_0-9]*'
        t.type = self.reserved.get(t.value,'NAME')    # Check for reserved words
        return t
    
    def t_TYPE_NAME(self,t):
        r'[A-Z][a-zA-Z_0-9]*'
        return t

    def t_NUMBER(self,t):
        # note: numbers are parsed but not converted into integers
        r'\d+'
        # t.value = int(t.value)
        return t

    t_ignore = " \t\r"

    # Comments
    def t_COMMENT(self,t):
        r'%.*'
        pass
    # No return value. Token discarded

    def t_newline(self,t):
        r'\n+'
        t.lexer.lineno += t.value.count("\n")

    def t_error(self,t):
        self.instal_error("Illegal character '%s'" % t.value[0])
        t.lexer.skip(1)

    def instal_error(self,p): print(p,file=sys.stderr)

#------------------------------------------------------------------------
# PARSER for instal

class makeInstalParser():

    def __init__(self):
        self.lexer = myLexer()
        self.tokens = self.lexer.tokens
        self.parser = yacc.yacc(module=self,write_tables=0,debug=False)

    instal_output = sys.stdout

    instal_err = sys.stderr

    def instal_print(self,p): print(p,file=self.instal_output)

    def instal_error(self,p): print(p,file=self.instal_err)

    def instal_warn(self,p): print(p,file=self.instal_err)

    # TL 20131218: defined for mode option passed by command argument 
    mode = ""

    # dictionaries
    names = { "institution":"noname" }
    types = { }
    exevents = { }
    inevents = { }
    vievents = { }
    crevents = { }
    dievents = { }
    fluents = { }
    noninertial_fluents = { }
    violation_fluents = { }
    obligation_fluents = [ ]
    generates = [ ]
    initiates = [ ]
    terminates = [ ]
    noninertials = [ ]
    initials = [ ]
    thisinitials = [ ]

    # start = 'institution'

    # def p_empty(p):
    #     'empty :'
    #     pass

    def check_fluent(self,p):
        if not ((p[0] in self.fluents) or (p[0] in self.noninertial_fluents)):
            self.instal_error(
                "% ERROR: Not a fluent in {x}"
                .format(x=p)) # needs prettifying
            exit(-1)

    def check_fluent_or_op(self,p):
        if not ((p[0] in self.fluents) or
                (p[0] in self.noninertial_fluents) or
                (p[0] in ['==','!='])):
            self.instal_error(
                "% ERROR: Not a fluent/operator in {x}"
                .format(x=p)) # needs prettifying
            exit(-1)

    def check_event(self,p):
        args = -1
        if (p[0] in self.exevents): args = self.exevents[p[0]]
        if (p[0] in self.inevents): args = self.inevents[p[0]]
        if (p[0] in self.vievents): args = self.vievents[p[0]]
        if args==-1:
            # needs prettifying
            self.instal_error("% ERROR: Not an event in {x}"
                              .format(x=p))
        if not(len(p[1])==len(args)):
            self.instal_error(
                "% ERROR: argument number mismatch between"
                " definition {x} and use {y}"
                .format(x=[p[0],args],y=p))
        #        exit(-1)

    def check_in_or_vi_event(self,p):
        args = -1
        if (p[0] in self.inevents): args = self.inevents[p[0]]
        if (p[0] in self.vievents): args = self.vievents[p[0]]
        if args==-1:
            # needs prettifying
            self.instal_error(
                "% ERROR: Not an institutional or violation event in {x}"
                .format(x=p))
        if not(len(p[1])==len(args)):
            self.instal_error(
                "% ERROR: argument number mismatch between"
                " definition {x} and use {y}"
                .format(x=[p[0],args],y=p))
        #        exit(-1)

    def check_inevent(self,p):
        if not (p[0] in self.inevents):
            # needs prettifying
            self.instal_error("% ERROR: Not an institutional event in {x}"
                              .format(x=p))
        if not(len(p[1])==len(self.inevents[p[0]])):
            self.instal_error(
                "% ERROR: argument number mismatch between"
                " definition {x} and use {y}"
                .format(x=[p[0],self.inevents[p[0]]],y=p))
        #        exit(-1)

    def check_exevent(self,p):
        if not (p[0] in self.exevents):
            # needs prettifying
            self.instal_error("% ERROR: Not an exogenous event in {x}"
                              .format(x=p))
            if not(len(p[1])==len(self.exevents[p[0]])):
                self.instal_error(
                    "% ERROR: argument number mismatch between"
                    " definition {x} and use {y}"
                    .format(x=[p[0],self.exevents[p[0]]],y=p))
        #    exit(-1)

    def check_variables(self,p3,p0):
        for v in p3:
            if self.isVar(v): continue
            self.instal_error(
                "% ERROR: variable expected. Found {x} in {y}"
                .format(x=v,y=p0))

    def p_institution(self,p):
        """
        institution : INSTITUTION NAME SEMI declaration_list
        institution : INSTITUTION TYPE_NAME SEMI declaration_list
        """
        self.names["institution"] = p[2]

    def p_declaration_list(self,p):
        """
        declaration_list :
        declaration_list :  declaration_list declaration
        """
        if len(p)==2: p[0] = p[1] + [p[2]]

    def p_declaration_type(self,p):
        """
        declaration : TYPE TYPE_NAME SEMI
        """
        self.types[p[2]] = p[2].lower()

    def p_declaration_event(self,p):
        """
        declaration : exevent
        declaration : crevent
        declaration : dievent
        declaration : inevent
        declaration : vievent
        declaration : fluent_declaration
        declaration : noninertial_fluent
        declaration : violation_fluent
        declaration : obligation_fluent_declaration
        declaration : generates
        declaration : initiates
        declaration : terminates
        declaration : noninertial_rule
        declaration : initially
        """
        p[0] = [p[1]]

    def p_exevent(self,p):
        """
        exevent : EXOGENOUS EVENT typed_term SEMI
        """
        event = p[3][0]
        args = p[3][1]
        self.exevents[event]=args
        p[0] = [p[1]]

    def p_crevent(self,p):
        """
        crevent : CREATE EVENT typed_term SEMI
        """
        event = p[3][0]
        args = p[3][1]
        self.crevents[event]=args
        p[0] = [p[1]]

    def p_dievent(self,p):
        """
        dievent : DISSOLVE EVENT typed_term SEMI
        """
        event = p[3][0]
        args = p[3][1]
        self.dievents[event]=args
        p[0] = [p[1]]

    def p_inevent(self,p):
        """
        inevent : INST EVENT typed_term SEMI
        """
        event = p[3][0]
        args = p[3][1]
        self.inevents[event]=args
        p[0] = [p[1]]

    def p_vievent(self,p):
        """
        vievent : VIOLATION EVENT typed_term SEMI
        """
        event = p[3][0]
        args = p[3][1]
        self.vievents[event]=args
        p[0] = [p[1]]

    def p_fluent_declaration(self,p):
        """
        fluent_declaration : FLUENT typed_term SEMI
        """
        fluent = p[2][0]
        args = p[2][1]
        self.fluents[fluent]=args
        p[0] = [p[1]]

    def p_noninertial_fluent(self,p):
        """
        noninertial_fluent : NONINERTIAL FLUENT typed_term SEMI
        """
        fluent = p[3][0]
        args = p[3][1]
        self.noninertial_fluents[fluent]=args
        p[0] = [p[1]]

    def p_violation_fluent(self,p):
        """
        violation_fluent : VIOLATION FLUENT typed_term SEMI
        """
        fluent = p[3][0]
        args = p[3][1]
        self.violation_fluents[fluent]=args
        p[0] = [p[1]]

    def p_obligation_fluent_declaration(self,p):
        """
        obligation_fluent_declaration : OBLIGATION FLUENT OBL LPAR typed_term COMMA typed_term COMMA typed_term RPAR SEMI
        """
        self.obligation_fluents = [[p[5],p[7],p[9]]] + self.obligation_fluents
        p[0] = [p[1]]

    def violp(self,x): return x[0]=='viol'

    # extended_typed_term is too permissive (I think)
    # remind me to ask me why
    # TL20140129: add time
    def p_generates(self,p):
        # typed_term or fluent on lhs??
        # typed_term_list or fluent_list on rhs??
        """
        generates : fluent GENERATES fluent_list SEMI
        generates : fluent GENERATES fluent_list condition SEMI
        generates : fluent GENERATES fluent_list IN NUMBER SEMI
        generates : fluent GENERATES fluent_list condition IN NUMBER SEMI
        """
#        print("p_generates: ",p[1],p[2],p[3],"*****")
        exev = p[1]
        if self.violp(p[1]): # JAP 20121119 more careful error checking
            self.check_event(p[1][1])
        else:
            self.check_event(p[1])
        genev = p[3]
        for x in genev: # JAP 20121119 more careful error checking
            self.check_in_or_vi_event(x)
        time = []
        cond = []
        if len(p)>5: # process conditions
            if len(p) == 8: #process conditions and time
                cond = p[4]
                time = p[6]
            elif len(p) == 7: # process time 
                time = p[5]
            else:
                cond = p[4]
        self.generates = [[exev,genev,cond,time]] + self.generates
        p[0] = [p[1]]

    def p_condition(self,p):
        """ condition : IF antecedent
        """
        p[0] = p[2]

    def p_expr(self,p):
        """ expr : term EQUALS term
            expr : term NOTEQUAL term
        """
        p[0] = [p[2],[p[1],p[3]]]

    def p_antecedent(self,p):
        """
            antecedent : antecedent COMMA fluent
            antecedent : antecedent COMMA NOT fluent
            antecedent : antecedent COMMA expr
            antecedent : fluent
            antecedent : NOT fluent
            antecedent : expr
        """
        # print("p_antecedent: ",p[1])
        if len(p)==2:
            self.check_fluent_or_op(p[1])
            p[0] = p[1]
        elif len(p)==3:
            self.check_fluent(p[2])
            p[0] = ['not',p[2]]
        elif len(p)==4:
            p[0] = ['and',p[1],p[3]]
        else:
            p[0] = ['and',p[1],['not',p[4]]]

    def p_initiates(self,p):
        """
        initiates : fluent INITIATES fluent_list SEMI
        initiates : fluent INITIATES fluent_list condition SEMI
        """
#        print("p_initiates: ",p[1],p[2],p[3],"*****")
        inev = p[1]
        if inev[0] in ['viol']:
            self.check_event(inev[1])
        else:
            self.check_event(inev)
        inf = p[3]
        # print p[3]
        cond = []
        if len(p)>5: # process conditions
            cond = p[4]
        self.initiates = [[inev,inf,cond]] + self.initiates
        p[0] = [p[1]]

    def p_terminates(self,p):
        """
        terminates : fluent TERMINATES fluent_list SEMI
        terminates : fluent TERMINATES fluent_list condition SEMI
        """
        inev = p[1]
        self.check_event(p[1])
        inf = p[3]
        cond = []
        if len(p)>5: # process conditions
            cond = p[4]
        self.terminates = [[inev,inf,cond]] + self.terminates
        p[0] = [p[1]]

    def p_noninertial_rule(self,p):
        """
        noninertial_rule : fluent WHEN antecedent SEMI
        """
        nif = p[1]
        ante = p[3]
        self.noninertials = [[nif,ante]] + self.noninertials
        p[0] = [p[1]]

    def p_initially_list(self,p):
        """
        initially_list : fluent
        initially_list : initially_list COMMA fluent
        """
        if (len(p)==4):
#            print("p_initially_list(4): ",p[3])
            self.thisinitials = self.thisinitials + [p[3]]
            p[0] = [p[3]]
        else:
#            print("p_initially_list(1): ",p[1])
            self.thisinitials = self.thisinitials + [p[1]]
            p[0] = [p[1]]

    def p_initially(self,p):
        """
        initially : INITIALLY initially_list SEMI
        initially : INITIALLY initially_list condition SEMI
        """
        cond = []
        if len(p)>4: # process conditions
            cond = p[3]
        # associate each initially with the controlling condition
        for i in self.thisinitials: self.initials = self.initials + [[i,cond]]
        # and reset the local accumulation list
        self.thisinitials = []

# simple (non-recursive) rules above here

    def p_typed_term1(self,p):
        """ typed_term : NAME """
        p[0] = [p[1],[]]

    def p_typed_term2(self,p):
        """ typed_term : NAME LPAR term_list RPAR """
        p[0] = [p[1],p[3]]
        # check p[3] are all variables
        # use a permissive parsing rule then check elements are all variables
        # a slightly questionable way of eliding the reduce/reduce conflict
        # arising from the original version of this rule and the fluent rule
        self.check_variables(p[3],p[0])

    # def p_typed_term_list(self,p):
    #     """
    #     typed_term_list :
    #     typed_term_list : typed_term
    #     typed_term_list : typed_term_list COMMA typed_term
    #     """
    #     if len(p)>2:
    #         p[0] = [p[1]] + p[3] # general case
    #     elif len(p)==2:
    #         p[0] = [p[1]]     # unary case
    #     # nullary case

    def p_term_list1(self,p):
        """ term_list : term_list COMMA term """
        p[0] = p[1] + [p[3]] # general case

    def p_term_list2(self,p):
        """ term_list : term """
        p[0] = [p[1]]     # unary case
        # nullary case

    # def p_term_list3(self,p):
    #     """ term_list : empty"""

    def p_fluent(self,p):
        """ 
        fluent : NAME
        fluent : NAME LPAR term_list RPAR
        fluent : POW LPAR fluent RPAR
        fluent : PERM LPAR fluent RPAR
        fluent : VIOL LPAR fluent RPAR
        fluent : OBL LPAR fluent COMMA fluent COMMA fluent RPAR
        """
#        print("p_fluent????")
        if len(p)==2:
#            print("p_fluent: ",p[1],"*****")
            p[0] = [p[1], []]
        elif len(p)==5:
#            print("p_fluent: ",p[1],p[2],p[3],p[4],"*****")
            p[0] = [p[1],p[3]]
        else: # must be an obligation
            p[0] = [p[1],[p[3],p[5],p[7]]]
            # TL: 20121115
            # if the obligation is not declared, but only occurs in rules
            # then it needs to be added to the list obligation_fluents explicitly
            # NOTE: the variable names may not be the standard ones, e.g. Agent1, Agent2
            # so standardize them (e.g. Agent1 -> Agent) by calling getVars() before added to obligation_fluents
            declared = False
            for of in self.obligation_fluents:
                [e, d, v] = of
                if e[0] == p[3][0] and d[0] == p[5][0] and v[0] == p[7][0]:
                    declared = True
            if not declared:
                self.instal_warn(
                    "WARNING: obligation {obl} used but not declared\n"
                    .format(obl=p[0]))
                p[3][1] = self.getVars(p[3][0])
                p[5][1] = self.getVars(p[5][0])
                p[7][1] = self.getVars(p[7][0])
                self.obligation_fluents = self.obligation_fluents + [[p[3],p[5],p[7]]]

    def p_term(self,p):
        """
        term : NAME
        term : TYPE_NAME
        term : NUMBER
        """
#        print("p_term: ",p[1])
        p[0] = p[1]

    # def p_fluent_arg_list(self,p):
    #     """ 
    #     fluent_arg_list : fluent_arg_list COMMA term
    #     fluent_arg_list : term
    #     """
    #     if len(p)>2:
    #         p[0] = p[1] + [p[3]] # general case
    #     elif len(p)==2:
    #         p[0] = [p[1]]     # unary case
    #     print("p_fluent_arg_list: ",p[0])
    #     # nullary case

    def p_fluent_list(self,p):
        """
        fluent_list : fluent_list COMMA fluent
        fluent_list : fluent
        fluent_list :
        """
        if len(p)==2:
            p[0] = [p[1]] # unary case
        else:
            p[0] = p[1] + [p[3]]  # other three

    def p_error(self,p):
        if p:
            self.instal_error("Syntax error at '%s'" % p.value)
            s = []
            while 1:
                tok = yacc.token()             # Get the next token
                s = s + [tok.value]
                if not tok or tok.type == 'SEMI': break
            print("discarding "," ".join(s))
            yacc.errok()
        else:
            self.instal_error("Syntax error at EOF")

    def term2string(self,p):
        # print "term2string: p = ",p
        args = p[1]
        r=''
        if len(args)==0:
            r=p[0]
        elif len(args)==1:
            r=p[0]+'('+args[0]+')'
        else:
            r='('+args[0]
            for x in args[1:]: r=r+','+x
            r=p[0]+r+')'
        return r

    def extendedterm2string(self,p):
        #if p[0] in ['perm','viol','pow']:
        #    r=p[0]+'('+term2string(p[1])+')'
        if p[0] in ['perm','viol']:
            r=p[0]+'('+self.term2string(p[1])+')'
        elif p[0] == 'pow':  # special handling for pow.-- TL: 20121108
            r=p[0]+'('+ self.names['institution']+','+self.term2string(p[1])+')'
        elif p[0] == 'obl':
            r=p[0]+'('+self.term2string(p[1][0])+','+self.term2string(p[1][1])+','+self.term2string(p[1][2])+')'
        else:
            r=self.term2string(p)
        return r

    # Global state variable used by typecheck and args2string

    saved_enumerator=0

    def typecheck(self,p,cont=False):
        # used in processing event declarations and fluents when clearing the
        # institutional state
        # parameters must be unique so that the type predicates do
        # not over-constrain parameters, ie. multiple occurrences of the same
        # formal parameter do not lead to them being grounded to the same value
        # this depends on the same enumeration occurring in args2string
        # Sometimes, uniqueness is required across more than one term, so save
        # the counter and start from there if cont is True
        # if cont: print "typecheck: ",p,cont,saved_enumerator
        if p==[]: return 'true'
        if not cont: self.saved_enumerator=0
        i=self.saved_enumerator
        r=self.types[p[0]]+'('+p[0]+str(i)+')'
        for j,t in enumerate(p[1:]): r=r+','+self.types[t]+'('+t+str(i+j+1)+')'
        self.saved_enumerator=i+len(p)
        return r

    def args2string(self,p,cont=False):
        # variables are enumerated to ensure uniqueness and is consistent with
        # that applied in typecheck.  Sometimes, uniqueness is required across
        # more than one term, so save the counter and start from there if cont
        # is True
        # if cont: print "args2string: ",p,cont,saved_enumerator
        if p==[]: return ''
        if not cont: self.saved_enumerator=0
        i=self.saved_enumerator
        r='('+p[0]+str(i)
        for j,x in enumerate(p[1:]): r=r+','+x+str(i+j+1)
        r=r+')'
        self.saved_enumerator=i+len(p)
        return r

    def printCondition(self,c):
        # print("printCondition: c = ",c)
        if c==[]: return
        if c[0]=='and':
            self.printCondition(c[1])
            self.printCondition(c[2])
        elif c[0]=='not':
            self.instal_print("   not")
            self.printCondition(c[1])
        elif c[0]=='==':
            self.instal_print("   {l}=={r},".format(l=c[1][0],r=c[1][1]))
        elif c[0]=='!=':
            self.instal_print("   {l}!={r},".format(l=c[1][0],r=c[1][1]))
        else:
            self.instal_print("   holdsat({fluent},{inst},I),"
                              .format(fluent=self.term2string(c), inst=self.names["institution"]))



    def isVar(self,t):
        return t[0]<>t[0].lower()

    def collectVars(self,t,d):
        # print("collectVars(top): t = ",t,"d = ",d)
        if t==[]: return
        if t[0]=='and':
            # print "collectVars(and): t = ",t
            self.collectVars(t[1],d)
            self.collectVars(t[2],d)
        elif t[0]=='not':
            self.collectVars(t[1],d)
        elif t[0]=='obl':
            for x in t[1]: self.collectVars(x,d)
        else:
            if t[0] in ['perm','pow','viol']: t = t[1]
            op = t[0]
            args = t[1]
            # print("*** collectVars op = ", op, "args = ",args)
            # not considering exogenous or creation events or violation fluents
            for evd in [self.exevents,self.inevents,self.vievents,
                        self.fluents,self.noninertial_fluents,
                        self.obligation_fluents]:
                if op in evd:
                    for (t1,t2) in zip(evd[op],args):
                        if t2 in d:
                            if t1<>d[t2]:
                                self.instal_error("% ERROR: {v} has type {t1} and type {t2}".format(v=t2,t1=t1,t2=d[t2]))
                        # only remember t2 if it is a variable (not a literal)
                        if self.isVar(t2): d[t2] = t1
                    # print "after collectVars: d = ",d
                    return # assume that once found can stop searching
            # reaching here means the term was not in any of the tables
            self.instal_warn("% WARNING: {t} not found in collectVars"
                             .format(t=t))

    # TL: 20121115
    # returns the standard variable names given the event/fluent name h
    def getVars(self,h):
        if self.inevents.has_key(h):
            varH = self.inevents[h]
        elif self.exevents.has_key(h):
            varH = self.exevents[h]
        elif self.vievents.has_key(h):
            varH = self.vievents[h]
        elif self.fluents.has_key(h):
            varH = self.fluents[h]
        else:
            # TL: 20121121 instal_error only takes one argument
            self.instal_error("ERROR: Unknown Type of {h}".format(h=h))
            #instal_error("ERROR: Unknown Type of", h)
            return
        return varH

    #------------------------------------------------------------------------
    # JAP: 20121121
    # output formatting functions

    # JAP: 20121114
    standard_prelude = "\
% suppress clingo warnings in absence of inertials, non-inertials or obligations\n\
ifluent(0,0).\n\
nifluent(0,0).\n\
oblfluent(0,0). \n\
% fluent rules\n\
holdsat(P,In,J):- holdsat(P,In,I),not terminated(P,In,I),\n\
    next(I,J),ifluent(P, In),instant(I),instant(J), inst(In).\n\
holdsat(P,In,J):- initiated(P,In,I),next(I,J),\n\
    ifluent(P, In),instant(I),instant(J), inst(In).\n\
holdsat(P,In,J):- initiated(P,In,I),next(I,J), \n\
    oblfluent(P, In),instant(I),instant(J), inst(In).\n\
% all observed events occur\n\
occurred(E,In,I):- evtype(E,In,ex),observed(E,In,I),instant(I), inst(In).\n\
% produces null for unknown events \n\
occurred(null,In,I) :- not evtype(E,In,ex), observed(E,In,I), \n\
    instant(I), inst(In). \n\
% produces gap warning for unknown events \n\
unknown(E, In, I) :- not evtype(E,In,ex), observed(E,In,I), \n\
    instant(I), inst(In). \n\
warninggap(In, I) :- unknown(E,In,I), inst(In), instant(I). \n\
% a violation occurs for each non-permitted action \n\
occurred(viol(E),In,I):-\n\
    occurred(E,In,I),\n\
    evtype(E,In,ex),\n\
    not holdsat(perm(E),In,I),\n\
    holdsat(live(In),In,I),evinst(E,In),\n\
    event(E),instant(I),event(viol(E)),inst(In).\n\
occurred(viol(E),In,I):-\n\
    occurred(E,In,I),\n\
    evtype(E,In,inst),\n\
    not holdsat(perm(E),In,I),\n\
    event(E),instant(I),event(viol(E)), inst(In).\n\
% needed until I tidy up some of the constraint generation \n\
true.\
"

    def instal_print_standard_prelude(self):
        # JAP: 2012114
        # Printing of standard prelude should be conditional on whether
        # we are extending an existing definition or not.  For now, that
        # option is not supported.
        self.instal_print("%\n% Standard prelude for {institution}\n%"
                          .format(**self.names))
        self.instal_print(self.standard_prelude)
        self.instal_print("%\n% Rules for Institution {institution}\n%\n"
                          "  ifluent(live({institution}), {institution}).\n"
                          "  fluent(live({institution}), {institution}).\n"
                          "  inst({institution})."
                          .format(**self.names))

    def instal_print_constraints(self):
        self.instal_print("%\n% Constraints for obserable events depending on mode option\n%".format(**self.names))
        if self.mode == "single":
            self.instal_print( "%%  mode SINGLE is chosen:\n"  
                        "{observed(E,In,J)}:- evtype(E,In,ex),instant(J), not final(J), inst(In).\n"
                        ":- observed(E,In,J),observed(F,In,J),instant(J),evtype(E,In,ex),\n"
                            "evtype(F,In,ex), E!=F,inst(In). \n"
                        "obs(In,I):- observed(E,In,I),evtype(E,In,ex),instant(I),inst(In).\n"
                        "         :- not obs(In,I), not final(I), instant(I), inst(In).\n")
        elif self.mode == "composite":
            self.instal_print("%%  mode COMPOSITE is chosen:\n" 
                        "{compObserved(E, J)}:- evtype(E,In,ex),instant(J), not final(J), inst(In).\n"
                        ":- compObserved(E,J),compObserved(F,J),instant(J),evtype(E,InX,ex),\n"
                        "   evtype(F,InY,ex), E!=F,inst(InX;InY). \n"
                        "obs(I):- compObserved(E,I),evtype(E,In,ex),instant(I),inst(In).\n"
                        "      :- not obs(I), not final(I), instant(I), inst(In).\n"
                        "observed(E,In,I) :- compObserved(E,I), inst(In), instant(I).")
        elif self.mode == "default":
            self.instal_print("%%  mode DEFAULT is chosen:\n"
                    "{observed(E,In,J)}:- evtype(E,In,ex),instant(J), not final(J), inst(In).\n"
                    ":- observed(E,In,J),observed(F,In,J),instant(J),evtype(E,In,ex),\n"
                    "evtype(F,In,ex), E!=F,inst(In). \n"
                    "obs(In,I):- observed(E,In,I),evtype(E,In,ex),instant(I),inst(In).\n"
                    "         :- not obs(In,I), not final(I), instant(I), inst(In).\n")



    def instal_print_types(self):
        # print types
        self.instal_print("%\n% The following types were declared:\n%")
        for t in self.types: self.instal_print("% {x}".format(x=t))

    def instal_print_exevents(self):
        # print exevents
        self.instal_print("%\n% Exogenous events")
        for ev in self.exevents:
            self.instal_print(
                "% Event: {ev} (type: ex)\n"
                "  event({ev}{args}) :- {rhs}.\n" #args1(Arg1) etc.
                "  evtype({ev}{args},{inst},ex) :- {rhs}.\n"
                "  evinst({ev}{args},{inst}) :- {rhs}.\n"
                "  ifluent(perm({ev}{args}), {inst}) :- {rhs}.\n"
                "  fluent(perm({ev}{args}), {inst}) :- {rhs}.\n"
                "  event(viol({ev}{args})) :- {rhs}.\n"
                "  evtype(viol({ev}{args}), {inst}, viol) :- {rhs}.\n"
                "  evinst(viol({ev}{args}),{inst}) :- {rhs}."
                .format(ev=ev,
                        args=self.args2string(self.exevents[ev]),
                        rhs=self.typecheck(self.exevents[ev]),
                        inst=self.names["institution"]))

    def instal_print_nullevent(self):
    # print nullevents
        self.instal_print("%\n% null event for unknown events")
        self.instal_print("% Event: null (type: ex)\n"
                 "  event(null).\n" 
                 "  evtype(null,{inst},ex).\n"
                 "  evinst(null,{inst}).\n"
                 "  ifluent(perm(null), {inst}).\n"
                 "  fluent(perm(null), {inst}).\n"
                 "  event(viol(null)).\n"
                 "  evtype(viol(null),{inst},viol).\n"
                 "  evinst(viol(null),{inst})."
                 .format(inst=self.names["institution"]))

    def instal_print_inevents(self):
        # print inevents
        self.instal_print("% Institutional events")
        for ev in self.inevents:
            self.instal_print(
                "% Event: {ev} (type: in)\n"
                "  event({ev}{args}) :- {rhs}.\n" # as above
                "  evtype({ev}{args},{inst},inst) :- {rhs}.\n"
                "  evinst({ev}{args},{inst}) :- {rhs}.\n"
                "  ifluent(pow({inst},{ev}{args}),{inst}) :- {rhs}.\n"
                "  ifluent(perm({ev}{args}),{inst}) :- {rhs}.\n"
                "  fluent(pow({inst},{ev}{args}),{inst}) :- {rhs}.\n"
                "  fluent(perm({ev}{args}),{inst}) :- {rhs}.\n"
                "  event(viol({ev}{args})) :- {rhs}.\n"
                "  evtype(viol({ev}{args}),{inst},viol) :- {rhs}.\n"
                "  evinst(viol({ev}{args}),{inst}) :- {rhs}."
                .format(ev=ev,
                        args=self.args2string(self.inevents[ev]),
                        rhs=self.typecheck(self.inevents[ev]),
                        inst=self.names["institution"]))

    def instal_print_vievents(self):
        # print vievents
        self.instal_print("%\n% Violation events\n%")
        for ev in self.vievents:
            self.instal_print(
                "% Event: {ev} (type: in)\n"
                "  event({ev}{args}) :- {rhs}.\n"
                "  evtype({ev}{args},{inst},viol) :- {rhs}.\n"
                "  evinst({ev}{args},{inst}) :- {rhs}."
                .format(ev=ev,
                        args=self.args2string(self.vievents[ev]),
                        rhs=self.typecheck(self.vievents[ev]),
                        inst=self.names["institution"]))

    def instal_print_crevents(self):
        # print crevents
        self.instal_print("%\n% Creation events\n%")
        for ev in self.crevents:
            self.instal_print(
                "% Event: {ev} (type: ex)\n"
                "  event({ev}{args}) :- {rhs}.\n" #args1(Arg1) etc.
                "  evtype({ev}{args},{inst},ex) :- {rhs}.\n"
                "  evinst({ev}{args},{inst}) :- {rhs}.\n"
                "  ifluent(perm({ev}{args}),{inst}) :- {rhs}.\n"
                "  fluent(perm({ev}{args}),{inst}) :- {rhs}.\n"
                "  event(viol({ev}{args})) :- {rhs}.\n"
                "  evtype(viol({ev}{args}),{inst},viol) :- {rhs}.\n"
                "  evinst(viol({ev}{args}),{inst}) :- {rhs}."
                .format(ev=ev,
                        args=self.args2string(self.crevents[ev]),
                        rhs=self.typecheck(self.crevents[ev]),
                        inst=self.names["institution"]))

    def instal_print_dievents(self):
        # print dievents
        self.instal_print("%\n% Dissolution events\n%")
        for ev in self.dievents:
            self.instal_print(
                "% Event: {ev} (type: ex)\n"
                "  event({ev}{args}) :- {rhs}.\n" #args1(Arg1) etc.
                "  evtype({ev}{args},{inst},ex) :- {rhs}.\n"
                "  evinst({ev}{args},{inst}) :- {rhs}.\n"
                "  ifluent(perm({ev}{args}),{inst}) :- {rhs}.\n"
                "  fluent(perm({ev}{args}),{inst}) :- {rhs}.\n"
                "  event(viol({ev}{args})) :- {rhs}.\n"
                "  evtype(viol({ev}{args}),{inst},viol) :- {rhs}.\n"
                "  evinst(viol({ev}{args}),{inst}) :- {rhs}."
                .format(ev=ev,
                        args=self.args2string(self.dievents[ev]),
                        rhs=self.typecheck(self.dievents[ev]),
                        inst=self.names["institution"]))

    def instal_print_inertial_fluents(self):
        # inertial fluents
        self.instal_print("%\n% inertial fluents\n%")
        for inf in self.fluents:
            # JAP 20130205: added code for unique naming + predicates
            self.instal_print(
                "ifluent({name}{args},{inst}) :-\n"
                "  {preds}.\n"
                "fluent({name}{args},{inst}) :-\n"
                "  {preds}.\n"
                .format(name=inf,
                        args=self.args2string(self.fluents[inf]),
                        preds=self.typecheck(self.fluents[inf]),
                        inst=self.names["institution"]))
            # for t in fluents[inf]:
            #     instal_print("   {pred}({tvar}),".format(pred=t.lower(),tvar=t))
            # instal_print("   true.")

    def instal_print_noninertial_fluents(self):
        # noninertial fluents
        self.instal_print("%\n% noninertial fluents\n%")
        for nif in self.noninertial_fluents:
            # JAP 20130205: added code for unique naming + predicates
            self.instal_print(
                "nifluent({name}{args}, {inst}) :-\n"
                "  {preds}.\n"
                "fluent({name}{args}, {inst}) :-\n"
                "  {preds}.\n"
                .format(name=nif,
                        args=self.args2string(self.noninertial_fluents[nif]),
                        preds=self.typecheck(self.noninertial_fluents[nif]), inst=self.names["institution"]))
            # for t in noninertial_fluents[nif]:
            #     instal_print("   {pred}({tvar}),".format(pred=t.lower(),tvar=t))
            # instal_print("   true.")

    def instal_print_violation_fluents(self):
        # violation fluents
        self.instal_print("%\n% violation fluents (to be implemented)\n")
        # for vf in fluents:
        #     print "ifluent({name}).".format(name=vf)

    def instal_print_obligation_fluents(self):
        # obligation fluents
        self.instal_print("%\n% obligation fluents\n%")
        for of in self.obligation_fluents:
            # e=term2string(of[0])
            # d=term2string(of[1])
            # v=term2string(of[2])
            e=of[0][0]+self.args2string(of[0][1])
            d=of[1][0]+self.args2string(of[1][1],cont=True)
            v=of[2][0]+self.args2string(of[2][1],cont=True)
            te=self.typecheck(of[0][1])
            td=self.typecheck(of[1][1],cont=True)
            tv=self.typecheck(of[2][1],cont=True)
            
            # TL20131228: set values for boolean e_event, e_fluent, d_event and d_fluent to indicate the type of e and d 
            e_event = False
            e_fluent = False
            d_event = False
            d_fluent = False
            if self.exevents.has_key(of[0][0]) or self.inevents.has_key(of[0][0]) or self.vievents.has_key(of[0][0]) or self.crevents.has_key(of[0][0]) or self.dievents.has_key(of[0][0]):
                e_event = True #TL 20131228: if e is an obliged event
            elif self.fluents.has_key(of[0][0]) or self.noninertial_fluents.has_key(of[0][0]):
                e_fluent = True  #TL 20131228: if e is an obliged fluent to achieve 
            else:
                self.instal_error("Type of obliged event/fluent {e} in the obligation is unknown. ".format(e=e))
                exit(-1) 
            if self.exevents.has_key(of[1][0]) or self.inevents.has_key(of[1][0]) or self.vievents.has_key(of[1][0]) or self.crevents.has_key(of[1][0]) or self.dievents.has_key(of[1][0]):
                d_event = True #TL 20131228: if d is an event 
            elif self.fluents.has_key(of[1][0]) or self.noninertial_fluents.has_key(of[1][0]):
                d_fluent = True #TL 20131228: if d is a fluent 
            else:
                self.instal_error("Type of obliged event/fluent {d} in the obligation is unknown. ".format(d=d))
                exit(-1)              

            # The first obligation rule 
            self.instal_print("oblfluent(obl({e},{d},{v}), {inst}) :-".format(e=e,d=d,v=v,inst=self.names["institution"]))
            if e_event:
                self.instal_print("   event({e}),".format(e=e))       
            if e_fluent:
                self.instal_print("   fluent({e},{inst}),".format(e=e,inst=self.names["institution"])) 
            if d_event:
                self.instal_print("   event({d}),".format(d=d))
            if d_fluent:
                self.instal_print("   fluent({d},{inst}),".format(d=d,inst=self.names["institution"])) 
            self.instal_print("   event({v}), {te},{td},{tv},inst({inst})."
                                      .format(e=e,d=d,v=v,te=te,td=td,tv=tv,inst=self.names["institution"]))
               
            # The 2nd obligation rule 
            self.instal_print("fluent(obl({e},{d},{v}), {inst}) :-".format(e=e,d=d,v=v,inst=self.names["institution"]))
            if e_event:
                self.instal_print("   event({e}),".format(e=e))       
            if e_fluent:
                self.instal_print("   fluent({e},{inst}),".format(e=e,inst=self.names["institution"])) 
            if d_event:
                self.instal_print("   event({d}),".format(d=d))
            if d_fluent:
                self.instal_print("   fluent({d},{inst}),".format(d=d,inst=self.names["institution"])) 
            self.instal_print("   event({v}), {te},{td},{tv},inst({inst})."
                                      .format(e=e,d=d,v=v,te=te,td=td,tv=tv,inst=self.names["institution"]))

            #The 3rd obligation rule 
            self.instal_print("terminated(obl({e},{d},{v}),{inst},I) :-".format(e=e,d=d,v=v,inst=self.names["institution"]))
            if e_event:
                self.instal_print("   event({e}), occurred({e},{inst},I),".format(e=e,inst=self.names["institution"]))       
            if e_fluent:
                self.instal_print("   fluent({e},{inst}), holdsat({e},{inst},I),".format(e=e,inst=self.names["institution"])) 
            if d_event:
                self.instal_print("   event({d}),".format(d=d))
            if d_fluent:
                self.instal_print("   fluent({d},{inst}),".format(d=d,inst=self.names["institution"])) 
            self.instal_print("   holdsat(obl({e},{d},{v}),{inst},I),\n"   
                              "   event({v}), {te},{td},{tv},inst({inst})."
                                      .format(e=e,d=d,v=v,te=te,td=td,tv=tv,inst=self.names["institution"]))

            #The fourth obligation rule 
            self.instal_print("terminated(obl({e},{d},{v}),{inst},I) :-".format(e=e,d=d,v=v,inst=self.names["institution"]))
            if e_event:
                self.instal_print("   event({e}), ".format(e=e))       
            if e_fluent:
                self.instal_print("   fluent({e},{inst}),".format(e=e,inst=self.names["institution"])) 
            if d_event:
                self.instal_print("   event({d}), occurred({d},{inst},I),".format(d=d,inst=self.names["institution"]))
            if d_fluent:
                self.instal_print("   fluent({d},{inst}),  holdsat({d},{inst},I),".format(d=d,inst=self.names["institution"])) 
            self.instal_print("   holdsat(obl({e},{d},{v}),{inst},I),\n"   
                              "   event({v}), {te},{td},{tv},inst({inst})."
                                      .format(e=e,d=d,v=v,te=te,td=td,tv=tv,inst=self.names["institution"]))

            #The fifth obligation rule 
            self.instal_print("occurred({v},{inst},I) :-".format(v=v,inst=self.names["institution"]))
            if e_event:
                self.instal_print("   event({e}), ".format(e=e))       
            if e_fluent:
                self.instal_print("   fluent({e},{inst}), not holdsat({e}, {inst}, I),".format(e=e,inst=self.names["institution"])) 
            if d_event:
                self.instal_print("   event({d}), occurred({d},{inst},I),".format(d=d,inst=self.names["institution"]))
            if d_fluent:
                self.instal_print("   fluent({d},{inst}),  holdsat({d},{inst},I),".format(d=d,inst=self.names["institution"])) 
            self.instal_print("   holdsat(obl({e},{d},{v}),{inst},I),\n"   
                              "   event({v}), {te},{td},{tv},inst({inst})."
                                      .format(e=e,d=d,v=v,te=te,td=td,tv=tv,inst=self.names["institution"]))
    

# TL 20140129
    def instal_print_generates(self):
        #self.instal_print("generates: {g}".format(g =self.generates))
        # generates
        self.instal_print("%\n% generate rules\n%")
        for rl in self.generates:
            [inorexev,inev,cond, ti] = rl
            vars1 = {}
            self.collectVars(inorexev,vars1)
            self.collectVars(cond,vars1)
            if ti == []:
                time = ""
            else:
                time = "+"+ str(ti)
            for x in inev:
                vars2 = {}
                self.collectVars(x,vars2)
                self.instal_print(
                    "%\n"
                    "% Translation of {exev} generates {inev} if {condition} in {time}\n"
                    "occurred({inev},{inst},I{time}) :- occurred({exev},{inst},I),\n"
                    "   holdsat(pow({inst},{inev}),{inst},I{time}),"
                    .format(exev=self.extendedterm2string(inorexev),
                            inev=self.extendedterm2string(x),
                            inst=self.names["institution"],
                            condition=cond, time = time))
                self.printCondition(cond)
                for k in vars1:
                    self.instal_print(
                        "   {pred}({tvar}),"
                        .format(pred=self.types[vars1[k]],tvar=k))
                for k in vars2:
                    # should check for consistent usage of k in vars1 and vars2
                    if k not in vars1:
                        self.instal_print(
                            "   {pred}({tvar}),"
                            .format(pred=self.types[vars2[k]],tvar=k))
                self.instal_print("   inst({inst}), instant(I).".format(inst=self.names["institution"]))

    def instal_print_initiates(self):
        # initiates
        self.instal_print("%\n% initiate rules\n%")
        for rl in self.initiates:
            [inev,inits,cond] = rl
            vars1 = {}
            self.collectVars(inev,vars1)
            self.collectVars(cond,vars1)
            for x in inits:
                vars2 = {}
                self.collectVars(x,vars2)
                self.instal_print(
                    "%\n% Translation of {inev} initiates {inits} if {condition}"
                    .format(inev=self.extendedterm2string(inev),inits=x,condition=cond))
                self.instal_print("%\ninitiated({inf},{inst},I) :-\n"
                                  "   occurred({ev},{inst},I),\n"
                                  "   holdsat(live({inst}),{inst},I), inst({inst}),"
                                  .format(inf=self.extendedterm2string(x),
                                          ev=self.extendedterm2string(inev),
                                          inst=self.names["institution"]))
                self.printCondition(cond)
                for k in vars1:
                    self.instal_print(
                        "   {pred}({tvar}),"
                        .format(pred=self.types[vars1[k]],tvar=k))
                for k in vars2:
                    # should check for consistent usage of k in vars1 and vars2
                    if k not in vars1:
                        self.instal_print(
                            "   {pred}({tvar}),"
                            .format(pred=self.types[vars2[k]],tvar=k))
                self.instal_print("   inst({inst}), instant(I).".format(inst=self.names["institution"]))

    def instal_print_terminates(self):
        # terminates
        self.instal_print("%\n% terminate rules\n%")
        for rl in self.terminates:
            [inev,terms,cond] = rl
            vars1 = {}
            self.collectVars(inev,vars1)
            self.collectVars(cond,vars1)
            for x in terms: # TL: 20121108
                vars2 = {}
                self.collectVars(x,vars2)
                self.instal_print(
                    "%\n% Translation of {inev} terminates {terms} if {condition}"
                    .format(inev=self.term2string(inev),terms=x,condition=cond))
                self.instal_print("%\nterminated({inf},{inst},I) :-\n"
                                  "   occurred({ev},{inst},I),\n"
                                  "   holdsat(live({inst}),{inst},I),inst({inst}),"
                                  .format(inf=self.extendedterm2string(x),
                                          ev=self.term2string(inev),
                                          inst=self.names["institution"]))
                self.printCondition(cond)
                for k in vars1:
                    self.instal_print(
                        "   {pred}({tvar}),"
                        .format(pred=self.types[vars1[k]],tvar=k))
                for k in vars2:
                    # should check for consistent usage of k in vars1 and vars2
                    if k not in vars1:
                        self.instal_print(
                            "   {pred}({tvar}),"
                            .format(pred=self.types[vars2[k]],tvar=k))
                self.instal_print("   inst({inst}), instant(I).".format(inst=self.names["institution"]))

    def instal_print_noninertials(self):
        # noninertials
        self.instal_print("%\n% noninertial rules\n%")
        for rl in self.noninertials:
            [nif,ante] = rl
            vars1 = {}
            self.collectVars(nif,vars1)
            # JAP 20130108: use extendedterm2string to support perm/pow
            self.instal_print("%\n% Translation of {nif} when {ante}\n"
                              "holdsat({nif},{inst},I) :-"
                              .format(nif=self.extendedterm2string(nif),ante=ante, inst=self.names["institution"]))
            self.printCondition(ante)
            self.collectVars(ante,vars1)
            for k in vars1:
                self.instal_print("   {pred}({tvar}),".
                                  format(pred=self.types[vars1[k]],tvar=k))
            self.instal_print("   inst({inst}), instant(I).".format(inst=self.names["institution"]))

    def instal_print_initially(self):
        # initially
        self.instal_print("%\n% initially\n%")
        # note this needs revision to time.lp
        if len(self.crevents) == 0:
            self.instal_print("% no creation event")
            self.instal_print("holdsat(live({inst}),{inst},I) :- start(I), inst({inst})."
                              .format(inst=self.names["institution"]))
            self.instal_print("holdsat(perm(null),{inst},I) :- start(I), inst({inst})."
                              .format(inst=self.names["institution"]))
            for inits in self.initials:
                [i,cond] = inits
                fvars = {}
                self.instal_print("% initially: {x}"
                                  .format(x=self.extendedterm2string(i)))
                if not(cond==[]):
                    self.instal_print(
                        "% condition: {x}"
                        .format(x=self.extendedterm2string(cond)))
                self.instal_print("holdsat({inf},{inst},I) :-"
                             .format(inst=self.names["institution"], inf=self.extendedterm2string(i)))
                self.collectVars(i,fvars)
                for k in fvars:
                    self.instal_print(
                        "   {pred}({tvar}),"
                        .format(pred=self.types[fvars[k]],tvar=k))
                if not(cond==[]):
                    #instal_print("   {x},".format(x=extendedterm2string(cond)))
                    self.instal_print(
                        "   holdsat({x},{inst},I),"
                        .format(inst=self.names["institution"], x=self.extendedterm2string(cond))) #TL:20130118
                self.instal_print("   inst({inst}), start(I).".format(inst=self.names["institution"]))
        else:
            self.instal_print("% at least one create event")
            self.instal_print("%\n% clear state to allow for re-creation\n%")
            # terminate(f,I) :- occurred(create{name},I), holdsat(f,I), instant(I), type(...) because f may be a fluent
            for c in self.crevents:
                self.instal_print("terminated(F,{inst},I) :-\n"
                                  "   occurred({cev},{inst},I),\n"
                                  "   not holdsat(live({inst}),{inst},I),\n"
                                  "   holdsat(F,{inst},I),\n"
                                  "   instant(I), inst({inst})."
                                  .format(cev=c,
                                          inst=self.names["institution"]))
                # to add the effect of creation event:
                # initiated(live(inst_1),I) :- occurred(logisticsStartEU,I),not holdsat(live(inst_1),I),instant(I). -- TL: 20121108
                self.instal_print("initiated(live({inst}),{inst},I) :-\n"
                                  "   occurred({cev},{inst},I),\n"
                                  "   not holdsat(live({inst}),{inst},I),\n"
                                  "   instant(I),inst({inst})."
                                  .format(cev=c,
                                          inst=self.names["institution"]))
                ##TL20131105:initiates the permission of null events 
                self.instal_print("initiated(perm(null),{inst},I) :-\n"
                                  "   occurred({cev},{inst},I),\n"
                                  "   not holdsat(live({inst}),{inst},I),\n"
                                  "   instant(I),inst({inst})."
                                  .format(cev=c,
                                          inst=self.names["institution"]))
                # process the initials
                self.instal_print("%\n% set up initial state\n%")
                for c in self.crevents:
                    for inits in self.initials:
                        [i,cond] = inits
                        fvars = {}
                        self.instal_print("% initially: {x}"
                                          .format(x=self.extendedterm2string(i)))
                        # JAP 20130224: copied from non-create case
                        if not(cond==[]):
                            self.instal_print(
                                "% condition: {x}"
                                .format(x=self.extendedterm2string(cond)))
                        self.instal_print(
                            "initiated({inf},{inst},I) :-\n"
                            "   occurred({cname},{inst},I),\n"
                            "   not holdsat(live({inst}),{inst},I), inst({inst}),"
                            .format(cname=c,
                                    inf=self.extendedterm2string(i),
                                    inst=self.names["institution"]))
                        self.collectVars(i,fvars)
                        for k in fvars:
                            self.instal_print(
                                "   {pred}({tvar}),"
                                .format(pred=self.types[fvars[k]],tvar=k))
                        # JAP 20130224: copied from non-create case
                        if not(cond==[]):
                            #instal_print("   {x},".format(x=extendedterm2string(cond)))
                            self.instal_print(
                                "   holdsat({x},I),"
                                .format(x=self.extendedterm2string(cond))) #TL:20130118
                        # JAP 20130224: instant or start??
                        self.instal_print("   instant(I).")

    def instal_print_dissolve(self):
        # dissolve
        self.instal_print("%\n% dissolve events\n%")
        for d in self.dievents:
            self.instal_print(
                "terminated(live({inst}),{inst},I) :-\n"
                "   occurred({dev},{inst},I),inst({inst}),\n"
                "   {args}, % true if dissolve event has no parameters"
                .format(dev=d,
                        args=self.typecheck(self.dievents[d]),
                        inst=self.names["institution"]))
            self.instal_print("   instant(I).")

#------------------------------------------------------------------------

    # def instal_parse(d):
    #     yacc.yacc()
    #     yacc.parse(d)

    def instal_parse(self,data):
        if data:
            return self.parser.parse(data,self.lexer.lexer,0,0,None)
        else:
            return []

    
    def clear_all_dicts(self):
        self.names.clear()
        self.types.clear()
        self.exevents.clear()
        self.inevents.clear()
        self.vievents.clear()
        self.crevents.clear()
        self.dievents.clear()
        self.fluents.clear()
        self.noninertial_fluents.clear()
        self.violation_fluents.clear()



