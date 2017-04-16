from instal.instalexceptions import InstalBridgeTypeError
from .typechecker import TypeChecker
from .instaltypechecker import InstalTypeChecker


class BridgeTypeChecker(TypeChecker):

    def __init__(self, ir_dict):
        self.source_typechecker = None
        self.sink_typechecker = None
        super(BridgeTypeChecker, self).__init__(ir_dict)

    def check_types(self, other_institutions=None):
        self.check_names()
        # TODO: Check there's nothing there shouldn't be (regular norms, fluent
        # declarations, etc.).

        self.source_typechecker = self.get_source_typechecker(
            self.IR_dict["names"]["source"], other_institutions)
        self.sink_typechecker = self.get_sink_typechecker(
            self.IR_dict["names"]["sink"], other_institutions)

        self.check_ipows(self.IR_dict["cross_initiation_fluents"])
        self.check_tpows(self.IR_dict["cross_termination_fluents"])
        self.check_gpows(self.IR_dict["cross_generation_fluents"])

        self.check_xgenerates(self.IR_dict["xgenerates"])
        self.check_xterminates(self.IR_dict["xterminates"])
        self.check_xinitiates(self.IR_dict["xinitiates"])

        self.check_non_bridge()

    def check_non_bridge(self):
        if self.IR_dict["initiates"]:
            raise InstalBridgeTypeError(
                "Unexpected initiates in bridge institution.")
        if self.IR_dict["terminates"]:
            raise InstalBridgeTypeError(
                "Unexpected terminates in bridge institution.")
        if self.IR_dict["generates"]:
            raise InstalBridgeTypeError(
                "Unexpected generates in bridge institution.")
        if self.IR_dict["whens"]:
            raise InstalBridgeTypeError(
                "Unexpected when in bridge institution.")

        if self.IR_dict["exevents"]:
            raise InstalBridgeTypeError(
                "Unexpected exogenous event in bridge institution.")
        if self.IR_dict["inevents"]:
            raise InstalBridgeTypeError(
                "Unexpected institutional event in bridge institution.")
        if self.IR_dict["vievents"]:
            raise InstalBridgeTypeError(
                "Unexpected violation event in bridge institution.")

        if self.IR_dict["fluents"]:
            raise InstalBridgeTypeError(
                "Unexpected fluent in bridge institution.")
        if self.IR_dict["noninertial_fluents"]:
            raise InstalBridgeTypeError(
                "Unexpected noninertial fluent in bridge institution.")
        if self.IR_dict["obligation_fluents"]:
            raise InstalBridgeTypeError(
                "Unexpected obligation fluent in bridge institution.")

    def get_source_typechecker(self, source, other_institutions):
        for i in other_institutions:
            if source == i["contents"]["names"]["institution"]:
                return InstalTypeChecker(i["contents"])
        raise InstalBridgeTypeError("No source institution {}".format(source))

    def get_sink_typechecker(self, sink, other_institutions):
        for i in other_institutions:
            if sink == i["contents"]["names"]["institution"]:
                return InstalTypeChecker(i["contents"])
        raise InstalBridgeTypeError("No sink institution {}".format(sink))

    def is_source(self, instName):
        return instName == self.IR_dict["names"]["source"]

    def check_is_source(self, instName):
        if not self.is_source(instName):
            raise InstalBridgeTypeError(
                "Institution {} is not the source in bridge {}".format(instName, self.IR_dict["names"]["bridge"]))

    def is_sink(self, instName):
        return instName == self.IR_dict["names"]["sink"]

    def check_is_sink(self, instName):
        if not self.is_sink(instName):
            raise InstalBridgeTypeError(
                "Institution {} is not the sink in bridge {}".format(instName, self.IR_dict["names"]["bridge"]))

    def check_ipows(self, ipows):
        for i in ipows:
            self.check_ipow(i)

    def check_ipow(self, ipow):
        self.check_is_source(ipow[0])
        self.sink_typechecker.is_list_initiatable([ipow[1]])
        self.check_is_sink(ipow[2])

    def check_tpows(self, tpows):
        for t in tpows:
            self.check_tpow(t)

    def check_tpow(self, tpow):
        self.check_is_source(tpow[0])
        self.sink_typechecker.is_list_terminatable([tpow[1]])
        self.check_is_sink(tpow[2])

    def check_gpows(self, gpows):
        for g in gpows:
            self.check_gpow(g)

    def check_gpow(self, gpow):
        self.check_is_source(gpow[0])
        self.check_sink_exogenous(gpow[1])
        self.check_is_sink(gpow[2])

    def check_sink_exogenous(self, term):
        self.sink_typechecker.check_term_declared(["exevents"], term)

    def check_sink_exogenous_list(self, terms):
        for t in terms:
            self.check_sink_exogenous(t)

    def check_xgenerates(self, xgenerates):
        for g in xgenerates:
            self.check_xgenerate(g)

    def check_xgenerate(self, xgenerate):
        self.source_typechecker.check_term_declared(
            ["inevents", "vievents"], (xgenerate[0]))
        self.check_sink_exogenous_list(xgenerate[1])
        self.source_typechecker.is_valid_condition(xgenerate[2])

        self.check_norm_arguments(lhs=xgenerate[0], rhs=xgenerate[
                                  1], condition=xgenerate[2])

    def check_xinitiates(self, xinitiates):
        for i in xinitiates:
            self.check_xinitiate(i)

    def check_xinitiate(self, xinitiate):
        self.source_typechecker.check_term_declared(
            ["inevents", "vievents"], (xinitiate[0]))
        self.sink_typechecker.is_list_initiatable(xinitiate[1])
        self.source_typechecker.is_valid_condition(xinitiate[2])

        self.check_norm_arguments(lhs=xinitiate[0], rhs=xinitiate[
                                  1], condition=xinitiate[2])

    def check_xterminates(self, xterminates):
        for t in xterminates:
            self.check_xterminate(t)

    def check_xterminate(self, xterminate):
        self.source_typechecker.check_term_declared(
            ["inevents", "vievents"], (xterminate[0]))
        self.sink_typechecker.is_list_terminatable(xterminate[1])
        self.source_typechecker.is_valid_condition(xterminate[2])

        self.check_norm_arguments(lhs=xterminate[0], rhs=xterminate[
                                  1], condition=xterminate[2])

    def check_norm_arguments(self, lhs=None, rhs=None, condition=None):
        # Overridee=d from TypeChecker
        if not lhs:
            lhs = []
        if not rhs:
            rhs = []
        if not condition:
            condition = []
        lhs_type_dict = self.source_typechecker.lhs_norm_arguments(lhs)
        rhs_type_dict = self.sink_typechecker.rhs_norm_arguments(rhs)
        condition_type_dict = self.source_typechecker.condition_norm_arguments(
            condition)
        final_types = self.get_types_dict(
            lhs_type_dict, rhs_type_dict, condition_type_dict)
        self.check_overloaded_arguments(final_types)

    def check_names(self):
        names = self.IR_dict.get("names")
        if not names:
            raise InstalBridgeTypeError("No names provided")

        bridge = names.get("bridge")
        inst = names.get("institution")
        source = names.get("source")
        sink = names.get("sink")

        if not bridge:
            raise InstalBridgeTypeError("No bridge name specified")

        if inst:
            raise InstalBridgeTypeError(
                "Institution name has been specified - are you trying to compile a .ial as a bridge?")

        if not source:
            raise InstalBridgeTypeError("Source institution not specified")

        if not sink:
            raise InstalBridgeTypeError("Sink institution not specified")

        if sink == source:
            raise InstalBridgeTypeError(
                "Source institution is the same as sink institution.")
