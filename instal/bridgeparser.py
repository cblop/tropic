#!/usr/bin/python
# REVISION HISTORY
#------------------------------------------------------------------------
# Pending: wrong print for ifluent(ipow(obl
# Pending: xinitiate obligation is not working
# 20150807 TL: fix the error on the termination rules from fluent to ifluent.
# 20140609 TL: fix the getInst(): now returns a list of institutions 
# 20140528 TL: fix the bugs to print ipow and tpow with perm/pow inside
# 20140507 TL: fix the cross consequence rules semantics  
# 20140214 TL: done the first working version
# 20140211 TL: created the parser
# 
#            
#------------------------------------------------------------------------

from __future__ import print_function
import re
import sys
import ply.lex as lex
import ply.yacc as yacc

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
        'xgenerates'  : 'XGENERATES',
        'if'          : 'IF',
        'in'          : 'IN',        # TL20140129
        'initially'   : 'INITIALLY',
        'inst'        : 'INST',
        'institution' : 'INSTITUTION',
        'noninertial' : 'NONINERTIAL',
        'not'         : 'NOT',
        'obl'         : 'OBL',
        'obligation'  : 'OBLIGATION',
        'gpow'        : 'GPOW',
        'ipow'        : 'IPOW',
        'tpow'        : 'TPOW',
        'cross'       : 'CROSS',
        'perm'        : 'PERM',
        'pow'         : 'POW',
        'xinitiates'  : 'XINITIATES' ,
        'xterminates' : 'XTERMINATES',
        'type'        : 'TYPE',
        'viol'        : 'VIOL',
        'violation'   : 'VIOLATION',
        #    'with'        : 'WITH',
        'when'        : 'WHEN',
        }

    tokens =  ['NAME','TYPE_NAME','NUMBER','LPAR','RPAR','SEMI','COMMA'] + list(reserved.values())

    # Tokens

    t_SEMI  = r';'
    t_COMMA  = r','
    t_LPAR  = r'\('
    t_RPAR  = r'\)'

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
        #t.value = int(t.value)  
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
    names = { }
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
    cross_generation_fluents = [ ]   # TL: lists for cross fluents new 
    cross_initiation_fluents = [ ]
    cross_termination_fluents = [ ]
    xgenerates = [ ]
    xinitiates = [ ]
    xterminates = [ ]
    noninertials = [ ]
    initials = [ ]
    thisinitials = [ ]

    all_lists = [] 

    # def p_empty(p):
    #     'empty :'
    #     pass

    def check_fluent(self,p):
        if not ((p[0] in self.fluents) or (p[0] in self.noninertial_fluents)):
            self.instal_error(
                "% ERROR: Not a fluent in {x}"
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

    def p_institution(self,p):
        """ institution : INSTITUTION NAME SEMI declaration_list
        """
        self.names["institution"] = p[2]

    def p_declaration_list(self,p):
        """ declaration_list :
            declaration_list :  declaration_list declaration
        """
        if len(p)==2: p[0] = p[1] + [p[2]]

    def p_declaration_type(self,p):
        """ declaration : TYPE TYPE_NAME SEMI
        """
        self.types[p[2]] = p[2].lower()

    def p_declaration_event(self,p):
        """ declaration : exevent
            declaration : crevent
            declaration : dievent
            declaration : inevent
            declaration : vievent
            declaration : fluent_declaration
            declaration : noninertial_fluent
            declaration : violation_fluent
            declaration : obligation_fluent_declaration
            declaration : cross_fluent_declaration
            declaration : xgenerates
            declaration : xinitiates
            declaration : xterminates
            declaration : noninertial_rule
            declaration : initially
        """
        p[0] = [p[1]]

    def p_type_name_list(self,p):
        """ type_name_list :
            type_name_list : TYPE_NAME
            type_name_list : TYPE_NAME COMMA type_name_list
        """
        if len(p)>2:
            p[0] = [p[1]] + p[3] # general case
        elif len(p)==2:
            p[0] = [p[1]]     # unary case
        # nullary case

# def p_name_list(p):
#     """ name_list :
#         name_list : NAME
#         name_list : NAME COMMA name_list
#     """
#     if len(p)>2: p[0] = [p[1]] + p[3] # general case
#     elif len(p)==2: p[0] = [p[1]]     # unary case
#     # nullary case

# def p_term(p):
#     """ term : NAME
#         term : NAME LPAR name_list RPAR
#     """
#     p[0] = [p[1],p[3]]

    def p_typed_term(self,p):
        """ typed_term : NAME
            typed_term : NAME LPAR type_name_list RPAR
        """
        if len(p)>2:
            p[0] = [p[1],p[3]]
        else:
            p[0] = [p[1], []]

    def p_typed_term_list(self,p):
        """ typed_term_list :
            typed_term_list : typed_term
            typed_term_list : typed_term COMMA typed_term_list
        """
        if len(p)>2:
            p[0] = [p[1]] + p[3] # general case
        elif len(p)==2:
            p[0] = [p[1]]     # unary case
        # nullary case

    def p_extended_typed_term(self,p):
        """ extended_typed_term : violation_typed_term
            extended_typed_term : permission_typed_term
            extended_typed_term : power_typed_term
            extended_typed_term : typed_term
        """
        #        extended_typed_term : obligation_typed_term
        p[0] = p[1]

# def p_extended_typed_term_list(p):
#     """ extended_typed_term_list :
#         extended_typed_term_list : extended_typed_term
#         extended_typed_term_list : extended_typed_term COMMA extended_typed_term_list
#     """
#     if len(p)>2: p[0] = [p[1]] + p[3] # general case
#     elif len(p)==2: p[0] = [p[1]]     # unary case
#     # nullary case

    def p_violation_typed_term(self,p):
        """ violation_typed_term : VIOL LPAR typed_term RPAR
        """
        p[0] = [p[1],p[3]]

    def p_permission_typed_term(self,p):
        """ permission_typed_term : PERM LPAR typed_term RPAR
        """
        p[0] = [p[1],p[3]]

    def p_power_typed_term(self,p):
        """ power_typed_term : POW LPAR typed_term RPAR
        """
        p[0] = [p[1],p[3]]

    def p_exevent(self,p):
        """ exevent : EXOGENOUS EVENT typed_term SEMI
        """
        event = p[3][0]
        args = p[3][1]
        self.exevents[event]=args
        p[0] = [p[1]]

    def p_crevent(self,p):
        """ crevent : CREATE EVENT typed_term SEMI
        """
        event = p[3][0]
        args = p[3][1]
        self.crevents[event]=args
        p[0] = [p[1]]

    def p_dievent(self,p):
        """ dievent : DISSOLVE EVENT typed_term SEMI
        """
        event = p[3][0]
        args = p[3][1]
        self.dievents[event]=args
        p[0] = [p[1]]

    def p_inevent(self,p):
        """ inevent : INST EVENT typed_term SEMI
        """
        event = p[3][0]
        args = p[3][1]
        self.inevents[event]=args
        p[0] = [p[1]]

    def p_vievent(self,p):
        """ vievent : VIOLATION EVENT typed_term SEMI
        """
        event = p[3][0]
        args = p[3][1]
        self.vievents[event]=args
        p[0] = [p[1]]

    def p_fluent_declaration(self,p):
        """ fluent_declaration : FLUENT typed_term SEMI
        """
        fluent = p[2][0]
        args = p[2][1]
        self.fluents[fluent]=args
        p[0] = [p[1]]

    def p_noninertial_fluent(self,p):
        """ noninertial_fluent : NONINERTIAL FLUENT typed_term SEMI
        """
        fluent = p[3][0]
        args = p[3][1]
        self.noninertial_fluents[fluent]=args
        p[0] = [p[1]]

    def p_violation_fluent(self,p):
        """ violation_fluent : VIOLATION FLUENT typed_term SEMI
        """
        fluent = p[3][0]
        args = p[3][1]
        self.violation_fluents[fluent]=args
        p[0] = [p[1]]

    def p_obligation_fluent_declaration(self,p):
        """ obligation_fluent_declaration : OBLIGATION FLUENT OBL LPAR typed_term COMMA typed_term COMMA typed_term RPAR SEMI
        """
        self.obligation_fluents = [[p[5],p[7],p[9]]] + self.obligation_fluents
        p[0] = [p[1]]

    #  TL 20140215 rule for declaraing cross fluents. new 
    def p_cross_fluent_declaration(self,p):
        """ cross_fluent_declaration : CROSS FLUENT GPOW LPAR TYPE_NAME COMMA typed_term COMMA TYPE_NAME RPAR SEMI
            cross_fluent_declaration : CROSS FLUENT TPOW LPAR TYPE_NAME COMMA fluent COMMA TYPE_NAME RPAR SEMI
            cross_fluent_declaration : CROSS FLUENT IPOW LPAR TYPE_NAME COMMA fluent COMMA TYPE_NAME RPAR SEMI
        """
        if p[3] == "gpow":
            self.cross_generation_fluents = [[p[5],p[7],p[9]]] + self.cross_generation_fluents
        elif p[3] == "ipow":
            self.cross_initiation_fluents = [[p[5],p[7],p[9]]] + self.cross_initiation_fluents
        #print(self.cross_fluents)
        else:
            self.cross_termination_fluents = [[p[5],p[7],p[9]]] + self.cross_termination_fluents
        p[0] = [p[1]]
        
        



    def violp(self,x): return x[0]=='viol'

    # extended_typed_term is too permissive (I think)
    # remind me to ask me why
    # TL20140129: add time
    # TL20140215: for cross-generation rules. new 
    def p_xgenerates(self,p):
        """ xgenerates : extended_typed_term XGENERATES typed_term_list SEMI
            xgenerates : extended_typed_term XGENERATES typed_term_list condition SEMI
            xgenerates : extended_typed_term XGENERATES typed_term_list IN NUMBER SEMI
            xgenerates : extended_typed_term XGENERATES typed_term_list condition IN NUMBER SEMI
        """
        exev = p[1]
        #if self.violp(p[1]): # JAP 20121119 more careful error checking
        #    self.check_event(p[1][1])
        #else:
        #    self.check_event(p[1])
        genev = p[3]
        #for x in genev: # JAP 20121119 more careful error checking
        #    self.check_in_or_vi_event(x)
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
        self.xgenerates = [[exev,genev,cond,time]] + self.xgenerates
        p[0] = [p[1]]
        

    def p_condition(self,p):
        """ condition : IF antecedent
        """
        p[0] = p[2]

    #  TL 20140215: cross for initiation rules  new 
    def p_xinitiates(self,p):
        """ xinitiates : extended_typed_term XINITIATES fluent_list SEMI
            xinitiates : extended_typed_term XINITIATES fluent_list condition SEMI
        """
        sf = p[1]
        #self.check_event(p[1])
        df = p[3]
        # print p[3]
        cond = []
        if len(p)>5: # process conditions
            cond = p[4]
        self.xinitiates = [[sf,df,cond]] + self.xinitiates
        p[0] = [p[1]]

    #  TL 20140215 new 
    def p_xterminates(self,p):
        """ xterminates : extended_typed_term XTERMINATES fluent_list SEMI
            xterminates : extended_typed_term XTERMINATES fluent_list condition SEMI
        """
        sf = p[1]
        #self.check_event(p[1])
        df = p[3]
        # print p[3]
        cond = []
        if len(p)>5: # process conditions
            cond = p[4]
        self.xterminates = [[sf,df,cond]] + self.xterminates
        p[0] = [p[1]]


    def p_fluent(self,p):
        """ fluent : NAME
            fluent : POW LPAR fluent RPAR
            fluent : PERM LPAR fluent RPAR
            fluent : OBL LPAR fluent COMMA fluent COMMA fluent RPAR
            fluent : GPOW LPAR fluent COMMA fluent COMMA fluent RPAR 
            fluent : IPOW LPAR fluent COMMA fluent COMMA fluent RPAR 
            fluent : TPOW LPAR fluent COMMA fluent COMMA fluent RPAR 
            fluent : NAME LPAR fluent_arg_list RPAR
        """
        if len(p)==2:
            p[0] = [p[1], []]
        elif len(p)==5:
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
            #for of in self.instal_fluents:
            #    [e, d, v] = of
            #    if e[0] == p[3][0] and d[0] == p[5][0] and v[0] == p[7][0]:
            #        declared = True
            if not declared:
                if p[1][0] == 'obl':
                    self.instal_warn(
                        "WARNING: obligation {obl} used but not declared\n"
                        .format(obl=p[0]))
                    p[3][1] = self.getVars(p[3][0])
                    p[5][1] = self.getVars(p[5][0])
                    p[7][1] = self.getVars(p[7][0])
                    self.obligation_fluents = self.obligation_fluents + [[p[3],p[5],p[7]]]
                #else:
                #    self.instal_warn(
                #        "WARNING: bridge power {pow} used but not declared\n"
                #        .format(pow=p[0]))
                    #p[3][1] = self.getVars(p[3][0])
                #    p[5][1] = self.getVars(p[5][0])
                    #p[7][1] = self.getVars(p[7][0])
                #    self.instal_fluents = self.instal_fluents + [[p[3],p[5],p[7]]] 

    def p_fluent_arg_list(self,p):
        """ fluent_arg_list : NAME
            fluent_arg_list : TYPE_NAME
            fluent_arg_list : NUMBER
            fluent_arg_list : NAME COMMA fluent_arg_list
            fluent_arg_list : TYPE_NAME COMMA fluent_arg_list
            fluent_arg_list : NUMBER COMMA fluent_arg_list
        """
        if len(p)>2:
            p[0] = [p[1]] + p[3] # general case
        elif len(p)==2:
            p[0] = [p[1]]     # unary case
        # nullary case

    def p_fluent_list(self,p):
        """ fluent_list :
            fluent_list : fluent
            fluent_list : fluent COMMA fluent_list
        """
        if len(p)==2:
            p[0] = [p[1]] # unary case
        else:
            p[0] = [p[1]] + p[3]  # other three

    def p_antecedent(self,p):
        """ antecedent : antecedent COMMA antecedent
            antecedent : NOT fluent
            antecedent : fluent
        """
        # print p[1]
        if len(p)==2:
            self.check_fluent(p[1])
            p[0] = p[1]
        elif len(p)==3:
            self.check_fluent(p[2])
            p[0] = ['not',p[2]]
        else: p[0] = ['and',p[1],p[3]]


    def p_noninertial_rule(self,p):
        """ noninertial_rule : typed_term WHEN antecedent SEMI
        """
        nif = p[1]
        ante = p[3]
        self.noninertials = [[nif,ante]] + self.noninertials
        p[0] = [p[1]]

    def p_initially_list(self,p):
        """ initially_list : fluent
            initially_list : fluent COMMA initially_list
        """
        self.thisinitials = self.thisinitials + [p[1]]
        p[0] = [p[1]]


    def p_initially(self,p):
        """ initially : INITIALLY initially_list SEMI
            initially : INITIALLY initially_list condition SEMI
        """
        cond = []
        if len(p)>4: # process conditions
            cond = p[3]
        # associate each initially with the controlling condition
        for i in self.thisinitials: self.initials = self.initials + [[i,cond]]
        # and reset the local accumulation list
        self.thisinitials = []
        

    def p_error(self,p):
        if p:
            self.instal_error("Syntax error at '%s'" % p.value)
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

    # add cross initials 
    def extendedterm2string(self,p):
        #if p[0] in ['perm','viol','pow']:
        #    r=p[0]+'('+term2string(p[1])+')'
        if p[0] in ['perm','viol']:
            r=p[0]+'('+self.term2string(p[1])+')'
        elif p[0] == 'pow':  # special handling for pow.-- TL: 20121108
            r=p[0]+'('+ self.names['institution']+','+self.term2string(p[1])+')'
        elif p[0] == 'obl':
            r=p[0]+'('+self.term2string(p[1][0])+','+self.term2string(p[1][1])+','+self.term2string(p[1][2])+')'
        elif p[0] in ['gpow', 'tpow', 'ipow']:
            r=p[0]+'('+ p[1][0][0] +','+self.extendedterm2string(p[1][1])+ ','+ p[1][2][0] + ')'
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

    def printCondition(self,c,inst):
        # print "printCondition: c = ",c
        if c==[]: return
        if c[0]=='and':
            self.printCondition(c[1],inst)
            self.printCondition(c[2],inst)
        elif c[0]=='not':
            self.instal_print("   not")
            self.printCondition(c[1],inst)
        else:
            self.instal_print("   holdsat({fluent},{inst},I),"
                              .format(fluent=self.term2string(c), inst=inst))



    def isVar(self,t):
        return t[0]<>t[0].lower()

    # add for xpowers
    def collectVars(self,t,d):
        # print "collectVars(top): t = ",t,"d = ",d
        if t==[]: return
        if t[0]=='and':
            # print "collectVars(and): t = ",t
            self.collectVars(t[1],d)
            self.collectVars(t[2],d)
        elif t[0]=='not':
            self.collectVars(t[1],d)
        elif t[0]=='obl':
            for x in t[1]: self.collectVars(x,d)
        elif t[0] in ['gpow', 'tpow', 'ipow']:
            self.collectVars(t[1][1],d)
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

    # TL: get inst information from alllists. new  
    # structure of all_lists (collected in main file ): 
    #  all_lists[name] = [copy.deepcopy(parser.exevents), copy.deepcopy(parser.inevents), copy.deepcopy(parser.vievents), copy.deepcopy(parser.fluents), copy.deepcopy(parser.obligation_fluents), copy.deepcopy(parser.noninertial_fluents)]  
    def getInst(self,test):
        instList = [] 
        for inst, lists in self.all_lists.iteritems():
            #TL: if the test is not an obligation fluent 
            if type(test) <> type([ ]): 
                if lists[0].has_key(test) or lists[1].has_key(test) or lists[2].has_key(test) or lists[3].has_key(test) or lists[5].has_key(test):
                    #return inst
                    instList.append(inst)
            else:
                if test[0] == 'perm' or test[0] == 'pow':
                    if lists[0].has_key(test[1][0]) or lists[1].has_key(test[1][0]) or lists[2].has_key(test[1][0]) or lists[3].has_key(test[1][0]) or lists[5].has_key(test[1][0]):
                        #return inst
                        instList.append(inst)

                elif test[0] == 'obl':
                    test = test[1]
                    for of in lists[4]:
                        if of[0][0] == test[0][0] and of[1][0] == test[1][0] and of[2][0] == test[2][0]:
                            #return inst
                            instList.append(inst)
                else: # for normal flunets 
                    if lists[0].has_key(test[0]) or lists[1].has_key(test[0]) or lists[2].has_key(test[0]) or lists[3].has_key(test[0]) or lists[5].has_key(test[0]):
                            #return inst
                        instList.append(inst)
        if instList == []:
            self.instal_error("ERROR: Unknown event/fluent of {test}".format(test=test))
            exit(-1)
        else:
            return instList


    #------------------------------------------------------------------------
    # JAP: 20121121
    # output formatting functions

    # JAP: 20121114
    # JAP 20160315: replaced inst(In;InS) with inst(In), inst(InS)... why so?
    standard_prelude = "\
% fluent rules\n\
holdsat(P,In,J):- holdsat(P,In,I),not terminated(P,In,I), not xterminated(InS,P,In,I), \n\
    next(I,J),ifluent(P, In),instant(I),instant(J), inst(In), inst(InS).\n\
holdsat(P,In,J):- initiated(P,In,I),next(I,J),\n\
    ifluent(P, In),instant(I),instant(J), inst(In).\n\
holdsat(P,In,J):- initiated(P,In,I),next(I,J), \n\
    oblfluent(P, In),instant(I),instant(J), inst(In).\n\
holdsat(P,In,J):- initiated(P,In,I),next(I,J), \n\
    nifluent(P, In),instant(I),instant(J), inst(In).\n\
holdsat(P,In,J):- xinitiated(InS,P,In,I),next(I,J),\n\
    ifluent(P, In),instant(I),instant(J), inst(InS;In).\n\
holdsat(P,In,J):- xinitiated(InS,P,In,I),next(I,J), \n\
    oblfluent(P, In),instant(I),instant(J), inst(InS;In).\n\
holdsat(P,In,J):- xinitiated(InS,P,In,I),next(I,J), \n\
    nifluent(P, In),instant(I),instant(J), inst(InS;In).\n\
true.\
"

    def instal_print_standard_prelude(self):
        # JAP: 2012114
        # Printing of standard prelude should be conditional on whether
        # we are extending an existing definition or not.  For now, that
        # option is not supported.
        #self.instal_print(self.all_lists)
        self.instal_print("%\n% Standard prelude for {institution}\n%"
                          .format(**self.names))
        self.instal_print(self.standard_prelude)
        self.instal_print("%\n% Rules for Institution {institution}\n%\n"
                          "  ifluent(live({institution}), {institution}).\n"
                          "  fluent(live({institution}), {institution}).\n"
                          "  inst({institution})."
                          .format(**self.names))


    def instal_print_types(self):
        # print types
        self.instal_print("%\n% The following types were declared:\n%")
        for t in self.types: self.instal_print("% {x}".format(x=t))

    def instal_print_exevents(self):
        # print exevents
        self.instal_print("%\n% Exogenous events")
        for ev in self.exevents:
            for inst in self.getInst(ev):
                self.instal_print(
                    "% Event: {ev} (type: ex) of institution {inst}\n"
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
                            inst=inst))

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
            for inst in self.getInst(ev):
                self.instal_print(
                    "% Event: {ev} (type: in) of institution {inst}\n"
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
                            inst=inst))

    def instal_print_vievents(self):
        # print vievents
        self.instal_print("%\n% Violation events of institution {inst}\n%")
        for ev in self.vievents:
            for inst in self.getInst(ev):
                self.instal_print(
                    "% Event: {ev} (type: in)\n"
                    "  event({ev}{args}) :- {rhs}.\n"
                    "  evtype({ev}{args},{inst},viol) :- {rhs}.\n"
                    "  evinst({ev}{args},{inst}) :- {rhs}."
                    .format(ev=ev,
                            args=self.args2string(self.vievents[ev]),
                            rhs=self.typecheck(self.vievents[ev]),
                            inst=inst))

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
        self.instal_print("%\n% inertial fluents \n%")
        for inf in self.fluents:
            # JAP 20130205: added code for unique naming + predicates
            for inst in self.getInst(inf):
                self.instal_print(
                    "ifluent({name}{args},{inst}) :-\n"
                    "  {preds}.\n"
                    "fluent({name}{args},{inst}) :-\n"
                    "  {preds}.\n"
                    .format(name=inf,
                            args=self.args2string(self.fluents[inf]),
                            preds=self.typecheck(self.fluents[inf]),
                            inst=inst))
            # for t in fluents[inf]:
            #     instal_print("   {pred}({tvar}),".format(pred=t.lower(),tvar=t))
            # instal_print("   true.")

    def instal_print_noninertial_fluents(self):
        # noninertial fluents
        self.instal_print("%\n% noninertial fluents\n%")
        for nif in self.noninertial_fluents:
            # JAP 20130205: added code for unique naming + predicates
            for inst in self.getInst(inf):
                self.instal_print(
                    "nifluent({name}{args}, {inst}) :-\n"
                    "  {preds}.\n"
                    "fluent({name}{args}, {inst}) :-\n"
                    "  {preds}.\n"
                    .format(name=nif,
                            args=self.args2string(self.noninertial_fluents[nif]),
                            preds=self.typecheck(self.noninertial_fluents[nif]), inst=inst))
            # for t in noninertial_fluents[nif]:
            #     instal_print("   {pred}({tvar}),".format(pred=t.lower(),tvar=t))
            # instal_print("   true.")

    def instal_print_violation_fluents(self):
        # violation fluents
        self.instal_print("%\n% violation fluents (to be implemented)\n")
        # for vf in fluents:
        #     print "ifluent({name}).".format(name=vf)

#  TL 20140215 new 
    def instal_print_cross_fluents(self):
        self.instal_print("%\n% cross fluents\n%")
        for xf in self.cross_generation_fluents:
            sinst = self.args2string(xf[0][0]).strip('()')
            dinst = self.args2string(xf[2][0], cont = True).strip('()')
            e=xf[1][0]+self.args2string(xf[1][1])
            te = self.typecheck(xf[1][1])

            self.instal_print("fluent(gpow({sinst},{e},{dinst}), {inst}) :- \n"
                              # JAP 201603015: was "    inst({sinst}; {dinst}; {inst}), \n"
                              "    inst({sinst}), inst({dinst}), inst({inst}), \n"
                              "    event({e}), evinst({e}, {dinst}), evtype({e}, {dinst}, ex), {te}."
                              .format(e=e,te =te, sinst=sinst,dinst=dinst,inst=self.names["institution"]))
            self.instal_print("ifluent(gpow({sinst},{e},{dinst}), {inst}) :- \n"
                              # JAP 201603015: was "    inst({sinst}; {dinst}; {inst}), \n"
                              "    inst({sinst}), inst({dinst}), inst({inst}), \n"
                              "    event({e}), evinst({e}, {dinst}), evtype({e}, {dinst}, ex), {te}."
                              .format(e=e,te =te, sinst=sinst,dinst=dinst,inst=self.names["institution"]))
        for xf in self.cross_initiation_fluents:
            sinst = self.args2string(xf[0][0]).strip('()')
            dinst = self.args2string(xf[2][0], cont = True).strip('()')
            f=self.extendedterm2string(xf[1])
            fvars = {}
            tf = self.collectVars(xf[1],fvars)
           # tf = self.typecheck(xf[1][1])
            self.instal_print("fluent(ipow({sinst},{f},{dinst}), {inst}) :- \n"
                              # JAP 20160315: was "    inst({sinst}; {dinst}; {inst}), "
                              "    inst({sinst}), inst({dinst}), inst({inst}), "
                              .format(f=f,sinst=sinst,dinst=dinst,inst=self.names["institution"]))
            for k in fvars:
                self.instal_print(
                    "   {pred}({tvar}),"
                    .format(pred=self.types[fvars[k]],tvar=k))
            self.instal_print("    fluent({f}, {dinst})."
                              .format(f=f, dinst=dinst))

            self.instal_print("ifluent(ipow({sinst},{f},{dinst}), {inst}) :- \n"
                              # JAP 20160315: was "    inst({sinst}; {dinst}; {inst}), "
                              "    inst({sinst}), inst({dinst}), inst({inst}), "
                              .format(f=f,sinst=sinst,dinst=dinst,inst=self.names["institution"]))
            for k in fvars:
                self.instal_print(
                    "   {pred}({tvar}),"
                    .format(pred=self.types[fvars[k]],tvar=k))
            self.instal_print("    fluent({f}, {dinst})."
                              .format(f=f, dinst=dinst))
        for xf in self.cross_termination_fluents:
            sinst = self.args2string(xf[0][0]).strip('()')
            dinst = self.args2string(xf[2][0], cont = True).strip('()')
            f=self.extendedterm2string(xf[1])
            fvars = {}
            tf = self.collectVars(xf[1],fvars)
           # tf = self.typecheck(xf[1][1])
            self.instal_print("fluent(tpow({sinst},{f},{dinst}), {inst}) :- \n"
                              "    inst({sinst}; {dinst}; {inst}), "
                              .format(f=f,sinst=sinst,dinst=dinst,inst=self.names["institution"]))
            for k in fvars:
                self.instal_print(
                    "   {pred}({tvar}),"
                    .format(pred=self.types[fvars[k]],tvar=k))
            self.instal_print("    fluent({f}, {dinst})."
                              .format(f=f, dinst=dinst))

            self.instal_print("ifluent(tpow({sinst},{f},{dinst}), {inst}) :- \n"
                              "    inst({sinst}; {dinst}; {inst}), "
                              .format(f=f,sinst=sinst,dinst=dinst,inst=self.names["institution"]))
            for k in fvars:
                self.instal_print(
                    "   {pred}({tvar}),"
                    .format(pred=self.types[fvars[k]],tvar=k))
            self.instal_print("    fluent({f}, {dinst})."
                              .format(f=f, dinst=dinst))



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
            #inst = self.getInst(of)
            for inst in self.getInst(of):
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
                self.instal_print("%\n% Translation of the obligation fluent obl({e},{d},{v}) of {inst}: \n%".format(e=e,d=d,v=v,inst=inst))        
                # The first obligation rule 
                self.instal_print("oblfluent(obl({e},{d},{v}), {inst}) :-".format(e=e,d=d,v=v,inst=inst))
                if e_event:
                    self.instal_print("   event({e}),".format(e=e))       
                if e_fluent:
                    self.instal_print("   fluent({e},{inst}),".format(e=e,inst=inst)) 
                if d_event:
                    self.instal_print("   event({d}),".format(d=d))
                if d_fluent:
                    self.instal_print("   fluent({d},{inst}),".format(d=d,inst=inst)) 
                self.instal_print("   event({v}), {te},{td},{tv},inst({inst})."
                                          .format(e=e,d=d,v=v,te=te,td=td,tv=tv,inst=inst))
                   
                # The 2nd obligation rule 
                self.instal_print("fluent(obl({e},{d},{v}), {inst}) :-".format(e=e,d=d,v=v,inst=inst))
                if e_event:
                    self.instal_print("   event({e}),".format(e=e))       
                if e_fluent:
                    self.instal_print("   fluent({e},{inst}),".format(e=e,inst=inst)) 
                if d_event:
                    self.instal_print("   event({d}),".format(d=d))
                if d_fluent:
                    self.instal_print("   fluent({d},{inst}),".format(d=d,inst=inst)) 
                self.instal_print("   event({v}), {te},{td},{tv},inst({inst})."
                                          .format(e=e,d=d,v=v,te=te,td=td,tv=tv,inst=inst))

                #The 3rd obligation rule 
                self.instal_print("terminated(obl({e},{d},{v}),{inst},I) :-".format(e=e,d=d,v=v,inst=inst))
                if e_event:
                    self.instal_print("   event({e}), occurred({e},{inst},I),".format(e=e,inst=inst))       
                if e_fluent:
                    self.instal_print("   fluent({e},{inst}), holdsat({e},{inst},I),".format(e=e,inst=inst)) 
                if d_event:
                    self.instal_print("   event({d}),".format(d=d))
                if d_fluent:
                    self.instal_print("   fluent({d},{inst}),".format(d=d,inst=inst)) 
                self.instal_print("   holdsat(obl({e},{d},{v}),{inst},I),\n"   
                                  "   event({v}), {te},{td},{tv},inst({inst})."
                                          .format(e=e,d=d,v=v,te=te,td=td,tv=tv,inst=inst))

                #The fourth obligation rule 
                self.instal_print("terminated(obl({e},{d},{v}),{inst},I) :-".format(e=e,d=d,v=v,inst=inst))
                if e_event:
                    self.instal_print("   event({e}), ".format(e=e))       
                if e_fluent:
                    self.instal_print("   fluent({e},{inst}),".format(e=e,inst=inst)) 
                if d_event:
                    self.instal_print("   event({d}), occurred({d},{inst},I),".format(d=d,inst=inst))
                if d_fluent:
                    self.instal_print("   fluent({d},{inst}),  holdsat({d},{inst},I),".format(d=d,inst=inst)) 
                self.instal_print("   holdsat(obl({e},{d},{v}),{inst},I),\n"   
                                  "   event({v}), {te},{td},{tv},inst({inst})."
                                          .format(e=e,d=d,v=v,te=te,td=td,tv=tv,inst=inst))

                #The fifth obligation rule 
                self.instal_print("occurred({v},{inst},I) :-".format(v=v,inst=inst))
                if e_event:
                    self.instal_print("   event({e}), ".format(e=e))       
                if e_fluent:
                    self.instal_print("   fluent({e},{inst}), not holdsat({e}, {inst}, I),".format(e=e,inst=inst)) 
                if d_event:
                    self.instal_print("   event({d}), occurred({d},{inst},I),".format(d=d,inst=inst))
                if d_fluent:
                    self.instal_print("   fluent({d},{inst}),  holdsat({d},{inst},I),".format(d=d,inst=inst)) 
                self.instal_print("   holdsat(obl({e},{d},{v}),{inst},I),\n"   
                                  "   event({v}), {te},{td},{tv},inst({inst})."
                                          .format(e=e,d=d,v=v,te=te,td=td,tv=tv,inst=inst))



#  TL 20140215 new 
    def instal_print_xgenerates(self):
        #self.instal_print("generates: {g}".format(g =self.generates))
        # generates
        # inorexev -> inev   inev -> exev
        self.instal_print("%\n% cross generate rules\n%")
        for rl in self.xgenerates:
            [inev,exev,cond,ti] = rl
            vars1 = {}
            self.collectVars(inev,vars1)
            self.collectVars(cond,vars1)
            if ti == []:
                time = ""
            else:
                time = "+"+ str(ti)
            for x in exev:
                vars2 = {}
                self.collectVars(x,vars2)
                for sinst in self.getInst(inev[0]):
                    for dinst in self.getInst(x[0]):
                        if sinst == dinst: continue 
                        else:
                            self.instal_print(
                                "%\n"
                                "% Translation of {inev} of {sinst} xgenerates {x} of {dinst} if {condition} in {time}\n"
                                "occurred({x},{dinst},I{time}) :- occurred({inev},{sinst},I),\n"
                                "   holdsat(gpow({sinst},{x},{dinst}),{inst},I{time}), \n"
                                "   inst({dinst};{sinst}), "
                                .format(inev=self.extendedterm2string(inev),
                                        x=self.extendedterm2string(x),
                                        inst=self.names["institution"],
                                        sinst=sinst,   # TL: needs to call getInst  
                                        dinst=dinst,
                                        condition=cond, time = time))
                            self.printCondition(cond, sinst)
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

   
    def instal_print_xinitiates(self):
        # initiates
        # inev -> sf  inits -> df  
        self.instal_print("%\n% cross initiation rules\n%")
        for rl in self.xinitiates:
            [sf,df,cond] = rl
            vars1 = {}
            self.collectVars(sf,vars1)
            self.collectVars(cond,vars1)
            for x in df:
                vars2 = {}
                self.collectVars(x,vars2)
                #self.instal_print("x:{x}".format(x=x))
                for sinst in self.getInst(sf[0]):
                    for dinst in self.getInst(x):
                        if sinst == dinst: continue 
                        else:
                            self.instal_print(
                                "%\n% Translation of {sf} of {sinst} xinitiates {x} of {dinst} if {condition}"
                                .format(sf=self.term2string(sf),x=x,condition=cond, sinst = sinst, dinst = dinst))
                            self.instal_print("%\nxinitiated({sinst}, {x},{dinst},I) :-\n"
                                              "   occurred({sf},{sinst},I),\n"
                                              "   holdsat(ipow({sinst}, {x}, {dinst}), {inst}, I), \n"
                                              "   holdsat(live({inst}),{inst},I), inst({inst}), \n"
                                              "   inst({dinst};{sinst}), "
                                              .format(x=self.extendedterm2string(x),
                                                      sf=self.term2string(sf),
                                                      sinst = sinst,
                                                      dinst = dinst,
                                                      inst=self.names["institution"]))
                            self.printCondition(cond, sinst)
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

    def instal_print_xterminates(self):
        # terminates
        # inev -> sf  inits -> df  
        self.instal_print("%\n% cross termination rules\n%")
        for rl in self.xterminates:
            [sf,df,cond] = rl
            vars1 = {}
            self.collectVars(sf,vars1)
            self.collectVars(cond,vars1)
            for x in df:
                vars2 = {}
                self.collectVars(x,vars2)
                for sinst in self.getInst(sf[0]):
                    for dinst in self.getInst(x):
                        if sinst == dinst: continue 
                        else:
                            self.instal_print(
                                "%\n% Translation of {sf} of {sinst} xterminates {x} of {dinst} if {condition}"
                                .format(sf=self.term2string(sf),x=x,condition=cond, sinst = sinst, dinst = dinst))
                            self.instal_print("%\nxterminated({sinst}, {x}, {dinst}, I) :-\n"
                                              "   occurred({sf},{sinst},I),\n"
                                              "   holdsat(tpow({sinst}, {x}, {dinst}), {inst}, I), \n"
                                              "   holdsat(live({inst}),{inst},I), inst({inst}), \n"
                                              "   inst({dinst};{sinst}), "
                                              .format(x=self.extendedterm2string(x),
                                                      sf=self.term2string(sf),
                                                      sinst = sinst,
                                                      dinst = dinst,
                                                      inst=self.names["institution"]))
                            self.printCondition(cond, sinst)
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
                #print("i:{i}".format(i=i))
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
                # TL new for cross fluents 
                if i[0] in ['gpow', 'tpow', 'ipow']:
                    self.instal_print("   inst({dinst}; {sinst}), ".format(sinst=i[1][0][0] ,dinst=i[1][2][0],inst=self.names["institution"]))
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
                self.instal_print("initiated(perm(null)),{inst},I) :-\n"
                                  "   occurred({cev},{inst},I),\n"
                                  "   not holdsat(live({inst}),{inst},I),\n"
                                  "   instant(I),inst({inst})."
                                  .format(cev=c,
                                          inst=self.names["institution"]))
                # process the initials
                self.instal_print("%\n% set up initial state\n%")
                for c in self.crevents:
                    for i in self.initials: # JAP 20140618 added self
                        fvars = {}
                        self.instal_print("% initially: {x}"
                                          .format(x=i)) #extendedterm2string(i)
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

    # function to print domain file 
    def print_domain(self, domain_file):
        typename = r"([A-Z][a-zA-Z0-9_]*)"
        literal = r"([a-z|\d][a-zA-Z0-9_]*)"
        f = open(domain_file,'r')
        self.instal_print("%\n% Domain declarations for {institution}\n%".format(**self.names))
        for l in f.readlines():
            l = l.rstrip() # lose trailing \n
            [t,r] = re.split(": ",l)
            if not(re.search(typename,l)):
                self.instal_error("ERROR: No type name in {x}".format(x=l))
                exit(-1)
            #check t is declared
            if not(t in self.types):
                self.instal_error("ERROR: type not declared in {x}".format(x=l))
                exit(-1)
            t = self.types[t]
            r = re.split(" ",r)
            for s in r:
                if not(re.search(literal,s)):
                    self.instal_error("ERROR: Unrecognized literal in {x}".format(x=l))
                    exit(-1)
                self.instal_print("{typename}({literalname}).".format(
                        typename=t,literalname=s))
            f.close() 

    def instal_print_all(self):
        self.instal_print("%\n% "
                          "-------------------------------"
                          "PART 1"
                          "-------------------------------"
                          "\n%")
        self.instal_print_standard_prelude()
        # self.instal_print_constraints()
        self.instal_print_types()
        self.instal_print_exevents()
        self.instal_print_nullevent()
        self.instal_print_inevents()
        self.instal_print_vievents()
        self.instal_print_crevents()
        self.instal_print_dievents()
        self.instal_print_dissolve()
        self.instal_print_inertial_fluents()
        self.instal_print_noninertial_fluents()
        self.instal_print_violation_fluents()
        self.instal_print_obligation_fluents()
        self.instal_print_cross_fluents()
        self.instal_print("%\n% "
                          "-------------------------------"
                          "PART 2"
                          "-------------------------------"
                          "\n%")
        self.instal_print_xgenerates()
        self.instal_print_xinitiates()
        self.instal_print_xterminates()
        # self.instal_print_noninertials()
        self.instal_print("%\n% "
                          "-------------------------------"
                          "PART 3"
                          "-------------------------------"
                          "\n%")
        self.instal_print_initially()
        self.instal_print("%\n% End of file\n%")

    # def instal_parse(d):
    #     yacc.yacc()
    #     yacc.parse(d)

    def instal_parse(self,data):
        if data:
            return self.parser.parse(data,self.lexer.lexer,0,0,None)
        else:
            return []
