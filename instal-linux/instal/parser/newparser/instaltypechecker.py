from collections import defaultdict

from instal.instalexceptions import InstalParserNotDeclaredError, InstalParserArgumentError, InstalParserTypeError, InstalParserError
from .typechecker import TypeChecker


class InstalTypeChecker(TypeChecker):

    def __init__(self, ir_dict):
        super(InstalTypeChecker, self).__init__(ir_dict)
        self.declaration_keys = ["inevents", "exevents", "vievents", "fluents",
                                 "noninertial_fluents", "obligation_fluents", "powers", "permissions"]

    def check_types(self):

        self.check_names()

        self.check_declarations()

        self.check_initiates(self.IR_dict["initiates"])
        self.check_terminates(self.IR_dict["terminates"])
        self.check_generates(self.IR_dict["generates"])
        self.check_whens(self.IR_dict["whens"])

        self.check_bridge()

    declr_keys = ["inevents", "exevents",
                  "vievents", "fluents", "noninertial_fluents"]

    def check_declarations(self):
        self.check_declaration_types()
        self.check_declaration_name_duplicates()

    def check_declaration_name_duplicates(self):
        names = []
        for k in self.declr_keys:
            for d in self.IR_dict[k].items():
                if d[0] in names:
                    raise InstalParserError(
                        "Duplicate name: {} in {}".format(d, k))
                names.append(d[0])

    def check_declaration_types(self):
        for k in self.declr_keys:
            for d in self.IR_dict[k].items():
                self.check_declaration_type(d)

    def check_declaration_type(self, d):
        for t in d[1]:
            if t not in self.IR_dict["types"]:
                raise InstalParserError(
                    "Type not declared: {} in {}".format(t, d))

    def check_bridge(self):
        if self.IR_dict["cross_initiation_fluents"]:
            raise InstalParserTypeError(
                "Unexpected ipow in regular institution.")

        if self.IR_dict["cross_termination_fluents"]:
            raise InstalParserTypeError(
                "Unexpected tpow in regular institution.")

        if self.IR_dict["cross_generation_fluents"]:
            raise InstalParserTypeError(
                "Unexpected gpow in regular institution.")

        if self.IR_dict["xgenerates"]:
            raise InstalParserTypeError(
                "Unexpected xgenerates in regular institution.")

        if self.IR_dict["xterminates"]:
            raise InstalParserTypeError(
                "Unexpected xterminates in regular institution.")

        if self.IR_dict["xinitiates"]:
            raise InstalParserTypeError(
                "Unexpected xinitiates in regular institution.")

    def check_names(self):
        names = self.IR_dict.get("names")
        if not names:
            raise InstalParserTypeError("No names provided")

        bridge = names.get("bridge")
        inst = names.get("institution")
        source = names.get("source")
        sink = names.get("sink")

        if not inst:
            raise InstalParserTypeError("No institution name provided.")

        if source or sink or bridge:
            raise InstalParserTypeError(
                "Found erroneous bridge/sink/source declaration: are you trying to parse a .iab as a .ial?")

    def check_initiates(self, initiates):
        for i in initiates:
            self.check_initiate(i)

    def check_initiate(self, initiate):
        self.can_initiate(initiate[0])
        self.is_list_initiatable(initiate[1])
        self.is_valid_condition(initiate[2])

        self.check_norm_arguments(lhs=initiate[0], rhs=initiate[
                                  1], condition=initiate[2])

    def check_terminates(self, terminates):
        for t in terminates:
            self.check_terminate(t)

    def check_terminate(self, terminate):
        self.can_terminate(terminate[0])
        self.is_list_terminatable(terminate[1])
        self.is_valid_condition(terminate[2])

        self.check_norm_arguments(lhs=terminate[0], rhs=terminate[
                                  1], condition=terminate[2])

    def check_generates(self, generates):
        for g in generates:
            self.check_generate(g)

    def check_generate(self, generate):
        self.can_generate(generate[0])
        self.is_list_generatable(generate[1])
        self.is_valid_condition(generate[2])

        self.check_norm_arguments(lhs=generate[0], rhs=generate[
                                  1], condition=generate[2])

    def check_whens(self, whens):
        for w in whens:
            self.check_when(w)

    def check_when(self, when):
        self.can_when(when[0])
        self.is_valid_condition(when[1])

        self.check_norm_arguments(lhs=when[0], condition=when[1])

    def can_initiate(self, term):
        # any institutional or violation event
        self.check_term_declared(["inevents", "vievents"], term)

    def can_terminate(self, term):
        # any institutional or violation event
        self.check_term_declared(["inevents", "vievents"], term)

    def can_generate(self, term):
        # any event (exogenous, institutional, violation)
        self.check_term_declared(["inevents", "vievents", "exevents"], term)

    def can_when(self, term):
        # any noninertial fluent
        self.check_term_declared(["noninertial_fluents"], term)

    def is_list_initiatable(self, term_list):
        # a list of inertial fluents, powers, permissions, obligations
        for term in term_list:
            self.check_term_declared(
                ["fluents", "powers", "permissions", "obligation_fluents"], term)

    def is_list_terminatable(self, term_list):
        # a list of inertial fluents, powers, permissions, obligations
        for term in term_list:
            self.check_term_declared(
                ["fluents", "powers", "permissions", "obligation_fluents"], term)

    def is_list_generatable(self, term_list):
        # a list of institutional or violation events
        for term in term_list:
            self.check_term_declared(["inevents", "vievents"], term)

    SPECIAL_KEYS = ["permissions", "powers", "obligation_fluents"]

    def is_valid_condition(self, cond):
        if len(cond) == 0:
            return
        if cond[0] == "and":
            self.is_valid_condition(cond[1])
            self.is_valid_condition(cond[2])
        elif cond[0] == "not":
            self.is_valid_condition(cond[1])
        elif cond[0] in self.EXPR_SYMBOLS:
            return
        else:
            self.check_term_declared(["fluents", "powers", "permissions", "noninertial_fluents", "obligation_fluents"],
                                     cond)

    def check_norm_arguments(self, lhs=None, rhs=None, condition=None):
        # Takes a norm.
        # Check whether each of its terms has the correct number of arguments as was declared
        # Also checks to see whether there's any type conflicts in its variables
        # ...and whether there are any unsafe variables
        if not lhs:
            lhs = []
        if not rhs:
            rhs = []
        if not condition:
            condition = []
        lhs_type_dict = self.lhs_norm_arguments(lhs)
        rhs_type_dict = self.rhs_norm_arguments(rhs)
        condition_type_dict = self.condition_norm_arguments(condition)
        final_types = self.get_types_dict(
            lhs_type_dict, rhs_type_dict, condition_type_dict)
        self.check_overloaded_arguments(final_types)

        self.check_conditional_expr(final_types, condition)

    def get_typedict_term(self, term):
        term_types = defaultdict(set)
        term_declared = self.get_term_declared(self.declaration_keys, term)
        if term[0] == "obl":
            e, d, v = term[1][0], term[1][1], term[1][2]
            term_types = self.combine_defaultdicts(
                self.get_typedict_term(e), self.get_typedict_term(d))
            term_types = self.combine_defaultdicts(
                term_types, self.get_typedict_term(v))
            return term_types
        elif term[0] == "perm":
            return self.get_typedict_term(term[1])
        elif term[0] == "pow":
            return self.get_typedict_term(term[1])
        used_args = term[1]
        declared_args = term_declared[1]
        if len(used_args) != len(declared_args):
            raise InstalParserArgumentError(
                "Mismatch in arguments between used ({}) and declared ({}).".format(term, term_declared))
        for argindex in range(0, len(used_args)):
            term_types[used_args[argindex]].add(declared_args[argindex])

        return term_types

    def lhs_norm_arguments(self, lhs):
        return self.get_typedict_term(lhs)

    def rhs_norm_arguments(self, rhs):
        type_dict = defaultdict(set)
        for r in rhs:
            type_dict = self.combine_defaultdicts(
                type_dict, self.get_typedict_term(r))

        return type_dict

    def condition_norm_arguments(self, cond):
        type_dict = defaultdict(set)
        if len(cond) == 0:
            return type_dict
        if cond[0] == "and":
            type_dict = self.combine_defaultdicts(self.condition_norm_arguments(cond[1]),
                                                  self.condition_norm_arguments(cond[2]))
        elif cond[0] in self.EXPR_SYMBOLS:
            pass
        elif cond[0] == "not":
            type_dict = self.condition_norm_arguments(cond[1])
        else:
            type_dict = self.get_typedict_term(cond)
        return type_dict

    def get_term_declared(self, keys_to_check, term):
        if len(term) == 0:
            return None
        if term[0] == "perm":
            if "permissions" in keys_to_check:
                declared_term = self.get_term_declared(
                    ["inevents", "exevents"], term[1])
                if declared_term:
                    return ["perm", declared_term]
        elif term[0] == "pow":
            if "powers" in keys_to_check:
                declared_term = self.get_term_declared(["inevents"], term[1])
                if declared_term:
                    return ["pow", declared_term]
        elif term[0] == "obl":
            if "obligation_fluents" in keys_to_check:
                e, d, v = term[1][0], term[1][1], term[1][2]
                e_declared = self.get_term_declared(
                    ["inevents", "vievents"], e)
                d_declared = self.get_term_declared(
                    ["inevents", "vievents"], d)
                v_declared = self.get_term_declared(
                    ["inevents", "vievents"], v)
                if e_declared and d_declared and v_declared:
                    return ["obl", [e_declared, d_declared, v_declared]]

        elif term[0] == "viol":
            raise NotImplementedError("I'm not sure if you can do this?")
        else:
            keys_to_check = [
                k for k in keys_to_check if k not in self.SPECIAL_KEYS]
            for key in keys_to_check:
                declared_term = self.IR_dict[key].get(term[0], None)
                if declared_term is None:
                    continue
                declared_term = [term[0], declared_term]
                if declared_term:
                    return declared_term
        return None

    def check_term_declared(self, keys_to_check, term):
        if self.get_term_declared(keys_to_check, term):
            return True
        raise InstalParserNotDeclaredError(
            "% Term {} not declared in the institution (checked {})".format(term, keys_to_check))
