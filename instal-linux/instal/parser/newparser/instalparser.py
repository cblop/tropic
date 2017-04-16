import ply.yacc as yacc

from .installexer import InstalLexer
from instal.instalexceptions import InstalParserSyntaxError, InstalParserTypeError, InstalParserError


class InstalParser(object):
    """
        InstalParser
        Converts .ial file to InstAL IR. Use instal_parse(self, data: str) where data is the IAL text.
        A significant chunk of this code is legacy and thus fragile.
    """

    def __init__(self):
        self.lexer = InstalLexer()
        self.tokens = self.lexer.tokens
        self.parser = yacc.yacc(module=self, write_tables=0, debug=False)
        # TL 20131218: defined for mode option passed by command argument
        self.mode = ""
        # dictionaries
        self.names = {"institution": None,
                      "bridge": None,
                      "source": None,
                      "sink": None}
        self.types = {}
        self.exevents = {}
        self.inevents = {}
        self.vievents = {}
        self.crevents = {}
        self.dievents = {}
        self.fluents = {}
        self.noninertial_fluents = {}
        self.violation_fluents = {}
        self.obligation_fluents = []
        self.generates = []
        self.initiates = []
        self.terminates = []
        self.noninertials = []
        self.initials = []
        self.thisinitials = []

        self.cross_initiation_fluents = []
        self.cross_termination_fluents = []
        self.cross_generation_fluents = []
        self.xgenerates = []
        self.xinitiates = []
        self.xterminates = []

    def instal_parse(self, data: str):
        if data:
            return self.parser.parse(data, self.lexer.lexer, 0, 0, None)
        else:
            return []

    def get_parsed_output(self) -> dict:
        return {
            "names": self.names,
            "types": self.types,
            "exevents": self.exevents,
            "inevents": self.inevents,
            "vievents": self.vievents,
            # "crevents" : self.crevents,
            # "dievents" : self.dievents,
            "fluents": self.fluents,
            "noninertial_fluents": self.noninertial_fluents,
            # "violation_fluents" : self.violation_fluents,
            "obligation_fluents": self.obligation_fluents,
            "generates": self.generates,
            "initiates": self.initiates,
            "terminates": self.terminates,
            "whens": self.noninertials,
            "initials": self.initials,
            "cross_initiation_fluents": self.cross_initiation_fluents,
            "cross_termination_fluents": self.cross_termination_fluents,
            "cross_generation_fluents": self.cross_generation_fluents,
            "xgenerates": self.xgenerates,
            "xinitiates": self.xinitiates,
            "xterminates": self.xterminates
        }

    def instal_warn(self, warning: str) -> None:
        print(warning)

    def p_start(self, p):
        """
        start : institution declaration_list
        start : bridge declaration_list
        """

    def p_institution(self, p):
        """
                institution : INSTITUTION NAME SEMI
                """
        self.names["institution"] = p[2]

    def p_bridge(self, p):
        """
                bridge : BRIDGE NAME SEMI
                """
        self.names["bridge"] = p[2]

    def p_source(self, p):
        """
                source : SOURCE NAME SEMI
                """
        self.names["source"] = p[2]

    def p_sink(self, p):
        """
                sink : SINK NAME SEMI
                """
        self.names["sink"] = p[2]

    def p_cross_fluent_declaration_gpow(self, p):
        """ cross_fluent_declaration : CROSS FLUENT GPOW LPAR NAME COMMA typed_term COMMA NAME RPAR SEMI
        """
        self.cross_generation_fluents = [
            [p[5], p[7], p[9]]] + self.cross_generation_fluents

        p[0] = [p[1]]

    def p_cross_fluent_declaration_tpow(self, p):
        """
            cross_fluent_declaration : CROSS FLUENT TPOW LPAR NAME COMMA typed_term COMMA NAME RPAR SEMI
        """

        self.cross_termination_fluents = [
            [p[5], p[7], p[9]]] + self.cross_termination_fluents
        p[0] = [p[1]]

    def p_cross_fluent_declaration_ipow(self, p):
        """
            cross_fluent_declaration : CROSS FLUENT IPOW LPAR NAME COMMA typed_term COMMA NAME RPAR SEMI
        """

        self.cross_initiation_fluents = [
            [p[5], p[7], p[9]]] + self.cross_initiation_fluents
        p[0] = [p[1]]

    def p_declaration_list(self, p):
        """
                declaration_list :
                declaration_list :  declaration_list declaration
                """
        if len(p) == 2:
            p[0] = p[1] + [p[2]]

    def p_declaration_type(self, p):
        """
                declaration : TYPE TYPE_NAME SEMI
                """
        self.types[p[2]] = p[2].lower()

    def p_declaration_event(self, p):
        """
                declaration : exevent
                declaration : crevent
                declaration : dievent
                declaration : inevent
                declaration : vievent
                declaration : fluent_declaration
                declaration : cross_fluent_declaration
                declaration : noninertial_fluent
                declaration : violation_fluent
                declaration : obligation_fluent_declaration
                declaration : generates
                declaration : initiates
                declaration : terminates
                declaration : noninertial_rule
                declaration : xgenerates
                declaration : xinitiates
                declaration : xterminates
                declaration : initially
                declaration : source
                declaration : sink
                """
        p[0] = [p[1]]

    def p_exevent(self, p):
        """
                exevent : EXOGENOUS EVENT typed_term SEMI
                """
        event = p[3][0]
        args = p[3][1]
        if self.exevents.get(event, None) is not None:
            raise InstalParserError(
                "Duplicate exogenous event of name {}".format(event))
        self.exevents[event] = args
        p[0] = [p[1]]

    def p_crevent(self, p):
        """
                crevent : CREATE EVENT typed_term SEMI
                """
        event = p[3][0]
        args = p[3][1]
        self.crevents[event] = args
        p[0] = [p[1]]
        raise InstalParserError(
            "NOT IMPLEMENTED: Creation events not implemented.")

    def p_dievent(self, p):
        """
                dievent : DISSOLVE EVENT typed_term SEMI
                """
        event = p[3][0]
        args = p[3][1]
        self.dievents[event] = args
        p[0] = [p[1]]
        raise InstalParserError(
            "NOT IMPLEMENTED: Dissolution events not implemented.")

    def p_inevent(self, p):
        """
                inevent : INST EVENT typed_term SEMI
                """
        event = p[3][0]
        args = p[3][1]
        if self.inevents.get(event, None) is not None:
            raise InstalParserError(
                "Duplicate institutional event of name {}".format(event))
        self.inevents[event] = args
        p[0] = [p[1]]

    def p_vievent(self, p):
        """
                vievent : VIOLATION EVENT typed_term SEMI
                """
        event = p[3][0]
        args = p[3][1]
        if self.vievents.get(event, None) is not None:
            raise InstalParserError(
                "Duplicate violation event of name {}".format(event))
        self.vievents[event] = args
        p[0] = [p[1]]

    def p_fluent_declaration(self, p):
        """
                fluent_declaration : FLUENT typed_term SEMI
                """
        fluent = p[2][0]
        args = p[2][1]
        if self.fluents.get(fluent, None) is not None:
            raise InstalParserError(
                "Duplicate fluent of name {}.".format(fluent))
        self.fluents[fluent] = args
        p[0] = [p[1]]

    def p_noninertial_fluent(self, p):
        """
                noninertial_fluent : NONINERTIAL FLUENT typed_term SEMI
                """
        fluent = p[3][0]
        args = p[3][1]
        if self.noninertial_fluents.get(fluent, None) is not None:
            raise InstalParserError(
                "Duplicate noninertial fluent of name {}.".format(fluent))
        self.noninertial_fluents[fluent] = args
        p[0] = [p[1]]

    def p_violation_fluent(self, p):
        """
                violation_fluent : VIOLATION FLUENT typed_term SEMI
                """
        fluent = p[3][0]
        args = p[3][1]
        self.violation_fluents[fluent] = args
        p[0] = [p[1]]
        raise InstalParserError(
            "NOT IMPLEMENTED: Violation fluents not implemented.")

    def p_obligation_fluent_declaration(self, p):
        """
                obligation_fluent_declaration : OBLIGATION FLUENT OBL LPAR typed_term COMMA typed_term COMMA typed_term RPAR SEMI
                """
        self.obligation_fluents = [
            [p[5], p[7], p[9]]] + self.obligation_fluents
        p[0] = [p[1]]

    def violp(self, x):
        return x[0] == 'viol'

    # TL 20140215: cross for initiation rules  new
    def p_xinitiates(self, p):
        """ xinitiates : typed_term XINITIATES fluent_list SEMI
            xinitiates : typed_term XINITIATES fluent_list condition SEMI
        """
        sf = p[1]
        df = p[3]
        cond = []
        if len(p) > 5:
            cond = p[4]
        self.xinitiates = [[sf, df, cond]] + self.xinitiates
        p[0] = [p[1]]

    # TL 20140215 new
    def p_xterminates(self, p):
        """ xterminates : typed_term XTERMINATES fluent_list SEMI
            xterminates : typed_term XTERMINATES fluent_list condition SEMI
        """
        sf = p[1]
        df = p[3]
        cond = []
        if len(p) > 5:  # process conditions
            cond = p[4]
        self.xterminates = [[sf, df, cond]] + self.xterminates
        p[0] = [p[1]]

    def p_xgenerates(self, p):
        """ xgenerates : typed_term XGENERATES fluent_list SEMI
            xgenerates : typed_term XGENERATES fluent_list condition SEMI
        """
        exev = p[1]
        genev = p[3]
        time = []
        cond = []
        if len(p) > 5:
            cond = p[4]
        self.xgenerates = [[exev, genev, cond, time]] + self.xgenerates
        p[0] = [p[1]]

    def p_generates(self, p):
        """
                generates : fluent GENERATES fluent_list SEMI
                generates : fluent GENERATES fluent_list condition SEMI
                """
        exev = p[1]
        genev = p[3]

        time = []
        cond = []
        if len(p) > 5:  # process conditions
            cond = p[4]
        self.generates = [[exev, genev, cond, time]] + self.generates
        p[0] = [p[1]]

    def p_condition(self, p):
        """ condition : IF antecedent
                """
        p[0] = p[2]

    def p_expr(self, p):
        """ expr : term EQUALS term
                        expr : term NOTEQUAL term
                        expr : term LESS term
                        expr : term LESSEQ term
                        expr : term GREATER term
                        expr : term GREATEREQ term
                """
        p[0] = [p[2], [p[1], p[3]]]

    def p_antecedent(self, p):
        """
                        antecedent : antecedent COMMA fluent
                        antecedent : antecedent COMMA NOT fluent
                        antecedent : antecedent COMMA expr
                        antecedent : antecedent COMMA NOT expr
                        antecedent : fluent
                        antecedent : NOT fluent
                        antecedent : expr
                        antecedent : NOT expr
                """
        if len(p) == 2:
            p[0] = p[1]
        elif len(p) == 3:
            p[0] = ['not', p[2]]
        elif len(p) == 4:
            p[0] = ['and', p[1], p[3]]
        else:
            p[0] = ['and', p[1], ['not', p[4]]]

    def p_initiates(self, p):
        """
                initiates : fluent INITIATES fluent_list SEMI
                initiates : fluent INITIATES fluent_list condition SEMI
                """
        inev = p[1]
        inf = p[3]
        cond = []
        if len(p) > 5:  # process conditions
            cond = p[4]
        self.initiates = [[inev, inf, cond]] + self.initiates
        p[0] = [p[1]]

    def p_terminates(self, p):
        """
                terminates : fluent TERMINATES fluent_list SEMI
                terminates : fluent TERMINATES fluent_list condition SEMI
                """
        inev = p[1]
        inf = p[3]
        cond = []
        if len(p) > 5:  # process conditions
            cond = p[4]
        self.terminates = [[inev, inf, cond]] + self.terminates
        p[0] = [p[1]]

    def p_noninertial_rule(self, p):
        """
                noninertial_rule : fluent WHEN antecedent SEMI
                """
        nif = p[1]
        ante = p[3]
        self.noninertials = [[nif, ante]] + self.noninertials
        p[0] = [p[1]]

    def p_initially_list(self, p):
        """
                initially_list : fluent
                initially_list : initially_list COMMA fluent
                """
        if len(p) == 4:
            self.thisinitials = self.thisinitials + [p[3]]
            p[0] = [p[3]]
        else:
            self.thisinitials = self.thisinitials + [p[1]]
            p[0] = [p[1]]

    def p_initially(self, p):
        """
                initially : INITIALLY initially_list SEMI
                initially : INITIALLY initially_list condition SEMI
                """
        cond = []
        if len(p) > 4:  # process conditions
            cond = p[3]
        # associate each initially with the controlling condition
        for i in self.thisinitials:
            self.initials = self.initials + [[i, cond]]
        # and reset the local accumulation list
        self.thisinitials = []

    # simple (non-recursive) rules above here

    def p_typed_term1(self, p):
        """ typed_term : NAME """
        p[0] = [p[1], []]

    def p_typed_term2(self, p):
        """ typed_term : NAME LPAR term_list RPAR """
        p[0] = [p[1], p[3]]
        # check p[3] are all variables
        # use a permissive parsing rule then check elements are all variables
        # a slightly questionable way of eliding the reduce/reduce conflict
        # arising from the original version of this rule and the fluent rule
        self.check_variables(p[3], p[0])

    def isVar(self, t):
        return t[0] != t[0].lower()

    def check_variables(self, p3, p0):
        for v in p3:
            if self.isVar(v):
                continue
            raise InstalParserError(
                "% ERROR: variable expected. Found {x} in {y}"
                .format(x=v, y=p0))

    def p_term_list1(self, p):
        """ term_list : term_list COMMA term """
        p[0] = p[1] + [p[3]]  # general case

    def p_term_list2(self, p):
        """ term_list : term """
        p[0] = [p[1]]  # unary case

    def p_fluent(self, p):
        """
                fluent : NAME
                fluent : NAME LPAR term_list RPAR
                fluent : POW LPAR fluent RPAR
                fluent : PERM LPAR fluent RPAR
                fluent : VIOL LPAR fluent RPAR
        fluent : OBL LPAR fluent COMMA fluent COMMA fluent RPAR
                """
        if len(p) == 2:
            p[0] = [p[1], []]
        elif len(p) == 5:
            p[0] = [p[1], p[3]]
        else:  # must be an obligation
            p[0] = [p[1], [p[3], p[5], p[7]]]
            # TL: 20121115
            # if the obligation is not declared, but only occurs in rules
            # then it needs to be added to the list obligation_fluents explicitly
            # NOTE: the variable names may not be the standard ones, e.g. Agent1, Agent2
            # so standardize them (e.g. Agent1 -> Agent) by calling getVars()
            # before added to obligation_fluents
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
                self.obligation_fluents = self.obligation_fluents + \
                    [[p[3], p[5], p[7]]]

    def p_fluent_cross(self, p):
        """fluent : GPOW LPAR NAME COMMA fluent COMMA NAME RPAR
                fluent : IPOW LPAR NAME COMMA fluent COMMA NAME RPAR
                fluent : TPOW LPAR NAME COMMA fluent COMMA NAME RPAR"""

        p[0] = [p[1], [p[3], p[5], p[7]]]

    def p_term(self, p):
        """
                term : NAME
                term : TYPE_NAME
                term : NUMBER
                """
        p[0] = p[1]

    def p_fluent_list(self, p):
        """
                fluent_list : fluent_list COMMA fluent
                fluent_list : fluent
                fluent_list :
                """
        if len(p) == 2:
            p[0] = [p[1]]  # unary case
        else:
            p[0] = p[1] + [p[3]]  # other three

    def p_error(self, p):
        if p:
            raise InstalParserSyntaxError("Syntax error at '%s'" % p.value)
        else:
            raise InstalParserSyntaxError("Syntax error at EOF")

    def term2string(self, p):
        args = p[1]
        r = ''
        if len(args) == 0:
            r = p[0]
        elif len(args) == 1:
            r = p[0] + '(' + args[0] + ')'
        elif p[0] in ['==', '!=', '<', '>', '<=', '>=']:
            # assumes arguments are literals :(
            r = p[1][0] + p[0] + p[1][1]
        elif p[0] == 'and':
            r = self.term2string(p[1]) + ' ' + p[0] + \
                ' ' + self.term2string(p[2])
        else:
            r = '(' + args[0]
            for x in args[1:]:
                r = r + ',' + x
            r = p[0] + r + ')'
        return r

    def extendedterm2string(self, p):
        if p[0] in ['perm', 'viol', 'pow']:
            r = p[0] + '(' + self.term2string(p[1]) + ')'
        elif p[0] == 'obl':
            r = p[0] + '(' + self.term2string(p[1][0]) + ',' + self.term2string(p[1][1]) + ',' + self.term2string(
                p[1][2]) + ')'
        else:
            r = self.term2string(p)
        return r

    # Global state variable used by typecheck and args2string

    saved_enumerator = 0

    def typecheck(self, p, cont=False):
        # used in processing event declarations and fluents when clearing the
        # institutional state
        # parameters must be unique so that the type predicates do
        # not over-constrain parameters, ie. multiple occurrences of the same
        # formal parameter do not lead to them being grounded to the same value
        # this depends on the same enumeration occurring in args2string
        # Sometimes, uniqueness is required across more than one term, so save
        # the counter and start from there if cont is True
        # if cont: print "typecheck: ",p,cont,saved_enumerator
        if not p:
            return 'true'
        if not cont:
            self.saved_enumerator = 0
        i = self.saved_enumerator
        r = self.types[p[0]] + '(' + p[0] + str(i) + ')'
        for j, t in enumerate(p[1:]):
            r = r + ',' + self.types[t] + '(' + t + str(i + j + 1) + ')'
        self.saved_enumerator = i + len(p)
        return r

    def args2string(self, p, cont=False):
        # variables are enumerated to ensure uniqueness and is consistent with
        # that applied in typecheck.  Sometimes, uniqueness is required across
        # more than one term, so save the counter and start from there if cont
        # is True
        # if cont: print "args2string: ",p,cont,saved_enumerator
        if not p:
            return ''
        if not cont:
            self.saved_enumerator = 0
        i = self.saved_enumerator
        r = '(' + p[0] + str(i)
        for j, x in enumerate(p[1:]):
            r = r + ',' + x + str(i + j + 1)
        r += ')'
        self.saved_enumerator = i + len(p)
        return r

    def collectVars(self, t, d):
        if not t:
            return
        if t[0] == 'and':
            self.collectVars(t[1], d)
            self.collectVars(t[2], d)
        elif t[0] == 'not':
            self.collectVars(t[1], d)
        elif t[0] == 'obl':
            for x in t[1]:
                self.collectVars(x, d)
        else:
            if t[0] in ['perm', 'pow', 'viol']:
                t = t[1]
            op = t[0]
            args = t[1]
            # not considering exogenous or creation events or violation fluents
            for evd in [self.exevents, self.inevents, self.vievents,
                        self.fluents, self.noninertial_fluents,
                        self.obligation_fluents]:
                if op in evd:
                    for (t1, t2) in zip(evd[op], args):
                        if t2 in d:
                            if t1 != d[t2]:
                                raise InstalParserTypeError(
                                    "% ERROR: {v} has type {t1} and type {t2} in {t}".format(v=t2, t1=t1, t2=d[t2],
                                                                                             t=t))
                        # only remember t2 if it is a variable (not a literal)
                        if self.isVar(t2):
                            d[t2] = t1
                    return  # assume that once found can stop searching
            # reaching here means the term was not in any of the tables
            self.instal_warn("% WARNING: {t} not found in collectVars"
                             .format(t=t))

    # TL: 20121115
    # returns the standard variable names given the event/fluent name h
    def getVars(self, h):
        if h in self.inevents:
            varH = self.inevents[h]
        elif h in self.exevents:
            varH = self.exevents[h]
        elif h in self.vievents:
            varH = self.vievents[h]
        elif h in self.fluents:
            varH = self.fluents[h]
        else:
            # TL: 20121121 instal_error only takes one argument
            raise InstalParserTypeError(
                "ERROR: Unknown Type of {h}".format(h=h))
        return varH

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
