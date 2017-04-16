from instal.instalexceptions import InstalCompileError


class InstalCompiler(object):
    """
        InstalCompiler
        Compiles InstAL IR to ASP.
        Call compile_ial() - requires the IR.
        A significant chunk of this code is legacy and thus fragile.
    """

    def __init__(self):
        self.ial_ir = {}
        self.names = {}
        self.types = {}
        self.exevents = {}
        self.inevents = {}
        self.vievents = {}

        self.out = ""

    def instal_print(self, to_append: str) -> None:
        #Legacy. InstAL print used to print to file: it now just adds to an out variable which is returned.
        self.out += to_append + "\n"

    def compile_ial(self, ial_ir: dict) -> str:
        """Called to compile ial_ir to ASP."""
        self.ial_ir = ial_ir
        self.names = self.ial_ir["names"]
        self.types = self.ial_ir["types"]
        self.exevents = self.ial_ir["exevents"]
        self.inevents = self.ial_ir["inevents"]
        self.vievents = self.ial_ir["vievents"]

        self.instal_print_all(self.ial_ir)
        return self.out

    def instal_print_all(self, ial_ir: dict) -> None:
        self.instal_print("%\n% "
                          "-------------------------------"
                          "PART 1"
                          "-------------------------------"
                          "\n%")
        self.instal_print_standard_prelude()
        self.instal_print_constraints()
        self.instal_print_exevents(ial_ir["exevents"])
        self.instal_print_nullevent()
        self.instal_print_inevents(ial_ir["inevents"])
        self.instal_print_vievents(ial_ir["vievents"])
        self.instal_print_crevents({})
        self.instal_print_dievents({})
        self.instal_print_dissolve({})
        self.instal_print_inertial_fluents(ial_ir["fluents"])
        self.instal_print_noninertial_fluents(ial_ir["noninertial_fluents"])
        self.instal_print_violation_fluents([])
        self.instal_print_obligation_fluents(ial_ir["obligation_fluents"])
        self.instal_print("%\n% "
                          "-------------------------------"
                          "PART 2"
                          "-------------------------------"
                          "\n%")
        self.instal_print_generates(ial_ir["generates"])
        self.instal_print_initiates(ial_ir["initiates"])
        self.instal_print_terminates(ial_ir["terminates"])
        self.instal_print_noninertials(ial_ir["whens"])
        self.instal_print("%\n% "
                          "-------------------------------"
                          "PART 3"
                          "-------------------------------"
                          "\n%")
        self.instal_print_initially(ial_ir["initials"])
        self.instal_print_types()
        self.instal_print("%\n% End of file\n%")

    def instal_print_standard_prelude(self):
        # Legacy. This used to dump the standard prelude at the top of every file.
        # It is now done in instal.models.InstalModel.
        self.instal_print("%\n% Standard prelude for {institution}\n%"
                          .format(**self.names))
        self.instal_print("% Standard prelude now dealt with in InstalModel.")

        # institution live fluents and the _preludeLoaded fluent
        self.instal_print("%\n% Rules for Institution {institution}\n%\n"
                          "  ifluent(live({institution}), {institution}).\n"
                          "  fluent(live({institution}), {institution}).\n"
                          "  inst({institution}).\n"
                          "  :- not _preludeLoaded. \n"
                          .format(**self.names))

    def instal_print_constraints(self):
        pass

    def isVar(self, t: str) -> bool:
        """
            Checks whether t is a type name by seeing if it has an uppercase first character.
        """
        return t[0] != t[0].lower()

    EXPR_SYMBOLS = ['==', '!=', '<', '>', '<=', '>=']

    def collectVars(self, t, d, compiler: 'InstalCompiler' = None):
        # A legacy function. Not removed because a lot of the type checking is tied to the functionality.
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
        elif t[0] in self.EXPR_SYMBOLS:
            pass
        else:
            if t[0] in ['perm', 'pow', 'viol']:
                t = t[1]
            op = t[0]
            args = t[1]
            for evd in [self.ial_ir["exevents"], self.ial_ir["inevents"], self.ial_ir["vievents"],
                        self.ial_ir["fluents"], self.ial_ir[
                        "noninertial_fluents"],
                        self.ial_ir["obligation_fluents"]]:
                if op in evd:
                    for (t1, t2) in zip(evd[op], args):
                        if t2 in d:
                            if t1 != d[t2]:
                                raise InstalCompileError(
                                    "% ERROR: {v} has type {t1} and type {t2} in {t}".format(v=t2, t1=t1, t2=d[t2],
                                                                                             t=t))
                        if self.isVar(t2):
                            d[t2] = t1
                    return
            raise InstalCompileError("% WARNING: {t} not found in collectVars"
                                     .format(t=t))

    def instal_print_types(self) -> None:
        # Print types. Also adds a constraint that every type must be grounded.
        self.instal_print("%\n% "
                          "-------------------------------"
                          "GROUNDING"
                          "-------------------------------"
                          "\n%")
        for t in self.types:
            self.instal_print("% {x}".format(x=t))
            self.instal_print(
                "_typeNotDeclared :- not {x}(_).".format(x=t.lower()))
            self.instal_print("#program {x}(l).".format(x=t.lower()))
            self.instal_print("{x}(l).\n".format(x=t.lower()))

    def instal_print_exevents(self, exevents: dict) -> None:
        # print exevents
        self.instal_print("%\n% Exogenous events")
        for ev, args in exevents.items():
            self.instal_print(
                "% Event: {ev} (type: ex)\n"
                "  event({ev}{args}) :- {rhs}.\n"
                "  evtype({ev}{args},{inst},ex) :- {rhs}.\n"
                "  evinst({ev}{args},{inst}) :- {rhs}.\n"
                "  ifluent(perm({ev}{args}), {inst}) :- {rhs}.\n"
                "  fluent(perm({ev}{args}), {inst}) :- {rhs}.\n"
                "  event(viol({ev}{args})) :- {rhs}.\n"
                "  evtype(viol({ev}{args}), {inst}, viol) :- {rhs}.\n"
                "  evinst(viol({ev}{args}),{inst}) :- {rhs}."
                .format(ev=ev,
                        args=self.args2string(args),
                        rhs=self.typecheck(args),
                        inst=self.names["institution"]))

    def instal_print_nullevent(self) -> None:
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

    def instal_print_inevents(self, inevents: dict) -> None:
        # print inevents
        self.instal_print("% Institutional events")
        for ev, args in inevents.items():
            self.instal_print(
                "% Event: {ev} (type: in)\n"
                "  event({ev}{args}) :- {rhs}.\n"
                "  evtype({ev}{args},{inst},inst) :- {rhs}.\n"
                "  evinst({ev}{args},{inst}) :- {rhs}.\n"
                "  ifluent(pow({ev}{args}),{inst}) :- {rhs}.\n"
                "  ifluent(perm({ev}{args}),{inst}) :- {rhs}.\n"
                "  fluent(pow({ev}{args}),{inst}) :- {rhs}.\n"
                "  fluent(perm({ev}{args}),{inst}) :- {rhs}.\n"
                "  event(viol({ev}{args})) :- {rhs}.\n"
                "  evtype(viol({ev}{args}),{inst},viol) :- {rhs}.\n"
                "  evinst(viol({ev}{args}),{inst}) :- {rhs}."
                .format(ev=ev,
                        args=self.args2string(args),
                        rhs=self.typecheck(args),
                        inst=self.names["institution"]))

    def instal_print_vievents(self, vievents: dict) -> None:
        # print vievents
        self.instal_print("%\n% Violation events\n%")
        for ev, args in vievents.items():
            self.instal_print(
                "% Event: {ev} (type: in)\n"
                "  event({ev}{args}) :- {rhs}.\n"
                "  evtype({ev}{args},{inst},viol) :- {rhs}.\n"
                "  evinst({ev}{args},{inst}) :- {rhs}."
                .format(ev=ev,
                        args=self.args2string(args),
                        rhs=self.typecheck(args),
                        inst=self.names["institution"]))

    def instal_print_crevents(self, crevents: dict) -> None:
        # print crevents
        self.instal_print("%\n% Creation events\n%")
        for ev in crevents:
            raise InstalCompileError("NOT IMPLEMENTED: Creation events.")

    def instal_print_dievents(self, dievents: dict) -> None:
        # print dievents
        self.instal_print("%\n% Dissolution events\n%")
        for ev in dievents:
            raise InstalCompileError("NOT IMPLEMENTED: Dissolution events.")

    def instal_print_inertial_fluents(self, fluents: dict) -> None:
        # inertial fluents
        self.instal_print("%\n% inertial fluents\n%")
        for inf, args in fluents.items():
            self.instal_print(
                "ifluent({name}{args},{inst}) :-\n"
                "  {preds}.\n"
                "fluent({name}{args},{inst}) :-\n"
                "  {preds}.\n"
                .format(name=inf,
                        args=self.args2string(args),
                        preds=self.typecheck(args),
                        inst=self.names["institution"]))

    def instal_print_noninertial_fluents(self, noninertial_fluents: dict) -> None:
        # noninertial fluents
        self.instal_print("%\n% noninertial fluents\n%")
        for nif, args in noninertial_fluents.items():
            self.instal_print(
                "nifluent({name}{args}, {inst}) :-\n"
                "  {preds}.\n"
                "fluent({name}{args}, {inst}) :-\n"
                "  {preds}.\n"
                .format(name=nif,
                        args=self.args2string(args),
                        preds=self.typecheck(args), inst=self.names["institution"]))

    def instal_print_violation_fluents(self, violation_fluents):
        # violation fluents
        self.instal_print("%\n% violation fluents (to be implemented)\n")
        for vif in violation_fluents:
            raise InstalCompileError("NOT IMPLEMENTED: Violation fluents.")

    saved_enumerator = 0

    def typecheck(self, p, cont: bool=False):
        # Legacy. Type checking is dealt with elsewhere, but this is necessary functionality.
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

    def instal_print_obligation_fluents(self, obligation_fluents: list) -> None:
        # obligation fluents
        self.instal_print("%\n% obligation fluents\n%")
        for of in obligation_fluents:
            e = of[0][0] + self.args2string(of[0][1])
            d = of[1][0] + self.args2string(of[1][1], cont=True)
            v = of[2][0] + self.args2string(of[2][1], cont=True)
            te = self.typecheck(of[0][1])
            td = self.typecheck(of[1][1], cont=True)
            tv = self.typecheck(of[2][1], cont=True)

            # Future versions will allow for conditions/deadlines to be states as well as events.
            # Not implemented as present though.
            e_event = True
            e_fluent = False
            d_event = True
            d_fluent = False

            self.instal_print(
                "oblfluent(obl({e},{d},{v}), {inst}) :-".format(e=e, d=d, v=v, inst=self.names["institution"]))
            if e_event:
                self.instal_print("   event({e}),".format(e=e))
            if e_fluent:
                self.instal_print("   fluent({e},{inst}),".format(
                    e=e, inst=self.names["institution"]))
            if d_event:
                self.instal_print("   event({d}),".format(d=d))
            if d_fluent:
                self.instal_print("   fluent({d},{inst}),".format(
                    d=d, inst=self.names["institution"]))
            self.instal_print("   event({v}), {te},{td},{tv},inst({inst})."
                              .format(e=e, d=d, v=v, te=te, td=td, tv=tv, inst=self.names["institution"]))

            # The 2nd obligation rule
            self.instal_print("ifluent(obl({e},{d},{v}), {inst}) :-".format(e=e, d=d, v=v, inst=self.names[
                "institution"]))
            if e_event:
                self.instal_print("   event({e}),".format(e=e))
            if e_fluent:
                self.instal_print("   fluent({e},{inst}),".format(
                    e=e, inst=self.names["institution"]))
            if d_event:
                self.instal_print("   event({d}),".format(d=d))
            if d_fluent:
                self.instal_print("   fluent({d},{inst}),".format(
                    d=d, inst=self.names["institution"]))
            self.instal_print("   event({v}), {te},{td},{tv},inst({inst})."
                              .format(e=e, d=d, v=v, te=te, td=td, tv=tv, inst=self.names["institution"]))
            self.instal_print(
                "fluent(obl({e},{d},{v}), {inst}) :-".format(e=e, d=d, v=v, inst=self.names["institution"]))
            if e_event:
                self.instal_print("   event({e}),".format(e=e))
            if e_fluent:
                self.instal_print("   fluent({e},{inst}),".format(
                    e=e, inst=self.names["institution"]))
            if d_event:
                self.instal_print("   event({d}),".format(d=d))
            if d_fluent:
                self.instal_print("   fluent({d},{inst}),".format(
                    d=d, inst=self.names["institution"]))
            self.instal_print("   event({v}), {te},{td},{tv},inst({inst})."
                              .format(e=e, d=d, v=v, te=te, td=td, tv=tv, inst=self.names["institution"]))

            # The 3rd obligation rule
            self.instal_print(
                "terminated(obl({e},{d},{v}),{inst},I) :-".format(e=e, d=d, v=v, inst=self.names["institution"]))
            if e_event:
                self.instal_print("   event({e}), occurred({e},{inst},I),".format(
                    e=e, inst=self.names["institution"]))
            if e_fluent:
                self.instal_print(
                    "   fluent({e},{inst}), holdsat({e},{inst},I),".format(e=e, inst=self.names["institution"]))
            if d_event:
                self.instal_print("   event({d}),".format(d=d))
            if d_fluent:
                self.instal_print("   fluent({d},{inst}),".format(
                    d=d, inst=self.names["institution"]))
            self.instal_print("   holdsat(obl({e},{d},{v}),{inst},I),\n"
                              "   event({v}), {te},{td},{tv},inst({inst})."
                              .format(e=e, d=d, v=v, te=te, td=td, tv=tv, inst=self.names["institution"]))

            # The fourth obligation rule
            self.instal_print(
                "terminated(obl({e},{d},{v}),{inst},I) :-".format(e=e, d=d, v=v, inst=self.names["institution"]))
            if e_event:
                self.instal_print("   event({e}), ".format(e=e))
            if e_fluent:
                self.instal_print("   fluent({e},{inst}),".format(
                    e=e, inst=self.names["institution"]))
            if d_event:
                self.instal_print("   event({d}), occurred({d},{inst},I),".format(
                    d=d, inst=self.names["institution"]))
            if d_fluent:
                self.instal_print(
                    "   fluent({d},{inst}),  holdsat({d},{inst},I),".format(d=d, inst=self.names["institution"]))
            self.instal_print("   holdsat(obl({e},{d},{v}),{inst},I),\n"
                              "   event({v}), {te},{td},{tv},inst({inst})."
                              .format(e=e, d=d, v=v, te=te, td=td, tv=tv, inst=self.names["institution"]))

            # The fifth obligation rule
            self.instal_print(
                "occurred({v},{inst},I) :-".format(v=v, inst=self.names["institution"]))
            if e_event:
                self.instal_print("   event({e}), ".format(e=e))
            if e_fluent:
                self.instal_print(
                    "   fluent({e},{inst}), not holdsat({e}, {inst}, I),".format(e=e, inst=self.names["institution"]))
            if d_event:
                self.instal_print("   event({d}), occurred({d},{inst},I),".format(
                    d=d, inst=self.names["institution"]))
            if d_fluent:
                self.instal_print(
                    "   fluent({d},{inst}),  holdsat({d},{inst},I),".format(d=d, inst=self.names["institution"]))
            self.instal_print("   holdsat(obl({e},{d},{v}),{inst},I),\n"
                              "   event({v}), {te},{td},{tv},inst({inst})."
                              .format(e=e, d=d, v=v, te=te, td=td, tv=tv, inst=self.names["institution"]))


    def instal_print_generates(self, generates: list) -> None:
        # generates
        self.instal_print("%\n% generate rules\n%")
        for rl in generates:
            [inorexev, inev, cond, ti] = rl
            vars1 = {}
            self.collectVars(inorexev, vars1)
            self.collectVars(cond, vars1)
            if not ti:
                time = ""
            else:
                time = "+" + str(ti)
                raise InstalCompileError(
                    "NOT IMPLEMENTED: Being able to generate events in n timesteps")
            for x in inev:
                vars2 = {}
                self.instal_print(
                    "%\n"
                    "% Translation of {exev} generates {inev} if {condition} in {time}\n"
                    "occurred({inev},{inst},I{time}) :- occurred({exev},{inst},I),"
                    "not occurred(viol({exev}),{inst},I),\n"
                    .format(exev=self.extendedterm2string(inorexev),
                            inev=self.extendedterm2string(x),
                            inst=self.names["institution"],
                            condition=cond, time=time))
                if not x[0] in self.vievents.keys():
                    self.instal_print(
                        "   holdsat(pow({inev}),{inst},I{time}),\n".format(
                            exev=self.extendedterm2string(inorexev),
                            inev=self.extendedterm2string(x),
                            inst=self.names["institution"],
                            condition=cond, time=time))
                self.printCondition(cond)
                for k in vars1:
                    self.instal_print(
                        "   {pred}({tvar}),"
                        .format(pred=self.types[vars1[k]], tvar=k))
                for k in vars2:
                    if k not in vars1:
                        self.instal_print(
                            "   {pred}({tvar}),"
                            .format(pred=self.types[vars2[k]], tvar=k))
                self.instal_print("   inst({inst}), instant(I).".format(
                    inst=self.names["institution"]))

    def instal_print_initiates(self, initiates: list) -> None:
        # initiates
        self.instal_print("%\n% initiate rules\n%")
        for rl in initiates:
            [inev, inits, cond] = rl
            vars1 = {}
            self.collectVars(inev, vars1)
            self.collectVars(cond, vars1)
            for x in inits:
                vars2 = {}
                self.instal_print(
                    "%\n% Translation of {inev} initiates {inits} if {condition}"
                    .format(inev=self.extendedterm2string(inev), inits=x, condition=cond))
                self.instal_print("%\ninitiated({inf},{inst},I) :-\n"
                                  "   occurred({ev},{inst},I),\n"
                                  "   not occurred(viol({ev}),{inst},I),\n"
                                  "   holdsat(live({inst}),{inst},I), inst({inst}),"
                                  .format(inf=self.extendedterm2string(x),
                                          ev=self.extendedterm2string(inev),
                                          inst=self.names["institution"]))
                self.printCondition(cond)
                for k in vars1:
                    self.instal_print(
                        "   {pred}({tvar}),"
                        .format(pred=self.types[vars1[k]], tvar=k))
                for k in vars2:
                    if k not in vars1:
                        self.instal_print(
                            "   {pred}({tvar}),"
                            .format(pred=self.types[vars2[k]], tvar=k))
                self.instal_print("   inst({inst}), instant(I).".format(
                    inst=self.names["institution"]))

    def instal_print_terminates(self, terminates: list) -> None:
        # terminates
        self.instal_print("%\n% terminate rules\n%")
        for rl in terminates:
            [inev, terms, cond] = rl
            vars1 = {}
            self.collectVars(inev, vars1)
            self.collectVars(cond, vars1)
            for x in terms:
                vars2 = {}
                self.instal_print(
                    "%\n% Translation of {inev} terminates {terms} if {condition}"
                    .format(inev=self.extendedterm2string(inev), terms=x, condition=cond))
                self.instal_print("%\nterminated({inf},{inst},I) :-\n"
                                  "   occurred({ev},{inst},I),\n"
                                  "   not occurred(viol({ev}),{inst},I),\n"
                                  "   holdsat(live({inst}),{inst},I),inst({inst}),"
                                  .format(inf=self.extendedterm2string(x),
                                          ev=self.extendedterm2string(inev),
                                          inst=self.names["institution"]))
                self.printCondition(cond)
                for k in vars1:
                    self.instal_print(
                        "   {pred}({tvar}),"
                        .format(pred=self.types[vars1[k]], tvar=k))
                for k in vars2:
                    if k not in vars1:
                        self.instal_print(
                            "   {pred}({tvar}),"
                            .format(pred=self.types[vars2[k]], tvar=k))
                self.instal_print("   inst({inst}), instant(I).".format(
                    inst=self.names["institution"]))

    def instal_print_noninertials(self, whens: list) -> None:
        # noninertials
        self.instal_print("%\n% noninertial rules\n%")
        for rl in whens:
            [nif, ante] = rl
            vars1 = {}
            self.collectVars(nif, vars1)
            self.instal_print("%\n% Translation of {nif} when {ante}\n"
                              "holdsat({nif},{inst},I) :-"
                              .format(nif=self.extendedterm2string(nif), ante=ante, inst=self.names["institution"]))
            self.printCondition(ante)
            for k in vars1:
                self.instal_print("   {pred}({tvar}),".
                                  format(pred=self.types[vars1[k]], tvar=k))
            self.instal_print("   inst({inst}), instant(I).".format(
                inst=self.names["institution"]))

    def instal_print_initially(self, initials: list) -> None:
        # initially
        self.instal_print("%\n% initially\n%")
        if True:
            self.instal_print("% no creation event")
            self.instal_print("holdsat(live({inst}),{inst},I) :- start(I), inst({inst})."
                              .format(inst=self.names["institution"]))
            self.instal_print("holdsat(perm(null),{inst},I) :- start(I), inst({inst})."
                              .format(inst=self.names["institution"]))
            for inits in initials:
                [i, cond] = inits
                fvars = {}
                self.instal_print("% initially: {x}"
                                  .format(x=self.extendedterm2string(i)))
                if not (cond == []):
                    self.instal_print(
                        "% condition: {x}"
                        .format(x=self.extendedterm2string(cond)))
                self.instal_print("holdsat({inf},{inst},I) :- not holdsat(live({inst}),{inst}),"
                                  .format(inst=self.names["institution"], inf=self.extendedterm2string(i)))
                self.collectVars(i, fvars)
                for k in fvars:
                    self.instal_print(
                        "   {pred}({tvar}),"
                        .format(pred=self.types[fvars[k]], tvar=k))
                if not (cond == []):
                    self.printCondition(cond)
                self.instal_print("   inst({inst}), start(I).".format(
                    inst=self.names["institution"]))
        else:
            pass

    def instal_print_dissolve(self, dievents: dict) -> None:
        # dissolve
        self.instal_print("%\n% dissolve events\n%")
        for d in dievents:
            raise InstalCompileError("NOT IMPLEMENTED: Dissolution events.")

    def args2string(self, p, cont: bool=False):
        # Legacy.
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

    def printCondition(self, c, institution: str=None):
        if not institution:
            institution = self.names["institution"]
        if not c:
            return
        if c[0] == 'and':
            self.printCondition(c[1])
            self.printCondition(c[2])
        elif c[0] == 'not':
            self.instal_print("   not")
            self.printCondition(c[1])
        elif c[0] == '==':
            self.instal_print("   {l}=={r},".format(l=c[1][0], r=c[1][1]))
        elif c[0] == '!=':
            self.instal_print("   {l}!={r},".format(l=c[1][0], r=c[1][1]))
        elif c[0] == '<':
            self.instal_print("   {l}<{r},".format(l=c[1][0], r=c[1][1]))
        elif c[0] == '>':
            self.instal_print("   {l}>{r},".format(l=c[1][0], r=c[1][1]))
        elif c[0] == '<=':
            self.instal_print("   {l}<={r},".format(l=c[1][0], r=c[1][1]))
        elif c[0] == '>=':
            self.instal_print("   {l}>={r},".format(l=c[1][0], r=c[1][1]))
        else:
            self.instal_print("   holdsat({fluent},{inst},I),"
                              .format(fluent=self.extendedterm2string(c), inst=institution))

    def term2string(self, p):
        # Legacy.
        args = p[1]
        r = ''
        if len(args) == 0:
            r = p[0]
        elif len(args) == 1:
            r = p[0] + '(' + args[0] + ')'
        elif p[0] in ['==', '!=', '<', '>', '<=', '>=']:
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
        # Legacy.
        if p[0] in ['perm', 'viol', 'pow']:
            r = p[0] + '(' + self.term2string(p[1]) + ')'
        elif p[0] == 'obl':
            r = p[0] + '(' + self.term2string(p[1][0]) + ',' + self.term2string(p[1][1]) + ',' + self.term2string(
                p[1][2]) + ')'
        elif p[0] in ["tpow", "ipow", "gpow"]:
            r = p[0] + '(' + p[1][0] + ',' + \
                self.term2string(p[1][1]) + ',' + p[1][2] + ')'
        else:
            r = self.term2string(p)
        return r
