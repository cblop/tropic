from instal.firstprinciples.TestEngine import InstalSingleShotTestRunnerFromText, InstalTestCase
from instal.instalexceptions import InstalBridgeTypeError, \
    InstalParserError


class TestBasicBridgeSyntax(InstalTestCase):
    inst1 = """
    institution inst1;
    exogenous event sourceExEvent;
    inst event sourceInstEvent;

    sourceExEvent generates sourceInstEvent;

    initially perm(sourceInstEvent), pow(sourceInstEvent), perm(sourceExEvent);
    """

    inst2 = """
    institution inst2;

    fluent sinkFluent;
    inst event sinkInstEvent;

    initially perm(sinkInstEvent);
    """

    def test_basic_declaration(self):
        bridge = """
        bridge bridgeName;
        source inst1;
        sink inst2;
        """
        runner = InstalSingleShotTestRunnerFromText(input_files=[self.inst1, self.inst2], bridge_file=[bridge],
                                                    domain_files=["newbridgetest/basic.idc"], fact_files=[])

        runner.run_test(query_file="newbridgetest/blank.iaq", verbose=self.verbose,
                        conditions=[])

    def test_no_inst(self):
        bridge = """
        bridge bridgeName;
        source inst1;
        sink inst2;
        institution bridgeName;
        """
        runner = InstalSingleShotTestRunnerFromText(input_files=[self.inst1, self.inst2], bridge_file=[bridge],
                                                    domain_files=["newbridgetest/basic.idc"], fact_files=[])
        with self.assertRaises(InstalParserError):
            # in parser, inst is in p_start --> this is parser error not type
            # error as the others are.
            runner.run_test(query_file="newbridgetest/blank.iaq", verbose=self.verbose,
                            conditions=[])

    def test_no_inst_events(self):
        bridge = """
        bridge bridgeName;
        source inst1;
        sink inst2;
        inst event in_e;
        """
        runner = InstalSingleShotTestRunnerFromText(input_files=[self.inst1, self.inst2], bridge_file=[bridge],
                                                    domain_files=["newbridgetest/basic.idc"], fact_files=[])
        with self.assertRaises(InstalBridgeTypeError):
            runner.run_test(query_file="newbridgetest/blank.iaq", verbose=self.verbose,
                            conditions=[])

    def test_no_exog_events(self):
        bridge = """
        bridge bridgeName;
        source inst1;
        sink inst2;
        exogenous event ex_e;
        """
        runner = InstalSingleShotTestRunnerFromText(input_files=[self.inst1, self.inst2], bridge_file=[bridge],
                                                    domain_files=["newbridgetest/basic.idc"], fact_files=[])
        with self.assertRaises(InstalBridgeTypeError):
            runner.run_test(query_file="newbridgetest/blank.iaq", verbose=self.verbose,
                            conditions=[])

    def test_no_viol_events(self):
        bridge = """
        bridge bridgeName;
        source inst1;
        sink inst2;
        violation event ex_e;
        """
        runner = InstalSingleShotTestRunnerFromText(input_files=[self.inst1, self.inst2], bridge_file=[bridge],
                                                    domain_files=["newbridgetest/basic.idc"], fact_files=[])
        with self.assertRaises(InstalBridgeTypeError):
            runner.run_test(query_file="newbridgetest/blank.iaq", verbose=self.verbose,
                            conditions=[])

    def test_no_fluents(self):
        bridge = """
        bridge bridgeName;
        source inst1;
        sink inst2;
        fluent flu;
        """
        runner = InstalSingleShotTestRunnerFromText(input_files=[self.inst1, self.inst2], bridge_file=[bridge],
                                                    domain_files=["newbridgetest/basic.idc"], fact_files=[])
        with self.assertRaises(InstalBridgeTypeError):
            runner.run_test(query_file="newbridgetest/blank.iaq", verbose=self.verbose,
                            conditions=[])

    def test_no_obligations(self):
        bridge = """
        bridge bridgeName;
        source inst1;
        sink inst2;
        obligation fluent obl(in_a, in_b, in_c);
        """
        runner = InstalSingleShotTestRunnerFromText(input_files=[self.inst1, self.inst2], bridge_file=[bridge],
                                                    domain_files=["newbridgetest/basic.idc"], fact_files=[])
        with self.assertRaises(InstalBridgeTypeError):
            runner.run_test(query_file="newbridgetest/blank.iaq", verbose=self.verbose,
                            conditions=[])

    def test_no_noninertial(self):
        bridge = """
        bridge bridgeName;
        source inst1;
        sink inst2;
        noninertial fluent ni_in;
        """
        runner = InstalSingleShotTestRunnerFromText(input_files=[self.inst1, self.inst2], bridge_file=[bridge],
                                                    domain_files=["newbridgetest/basic.idc"], fact_files=[])
        with self.assertRaises(InstalBridgeTypeError):
            runner.run_test(query_file="newbridgetest/blank.iaq", verbose=self.verbose,
                            conditions=[])

    def test_no_generates(self):
        bridge = """
        bridge bridgeName;
        source inst1;
        sink inst2;
        in_a generates in_b;
        """
        runner = InstalSingleShotTestRunnerFromText(input_files=[self.inst1, self.inst2], bridge_file=[bridge],
                                                    domain_files=["newbridgetest/basic.idc"], fact_files=[])
        with self.assertRaises(InstalBridgeTypeError):
            runner.run_test(query_file="newbridgetest/blank.iaq", verbose=self.verbose,
                            conditions=[])

    def test_no_initiates(self):
        bridge = """
        bridge bridgeName;
        source inst1;
        sink inst2;
        in_a initiates flu_a;
        """
        runner = InstalSingleShotTestRunnerFromText(input_files=[self.inst1, self.inst2], bridge_file=[bridge],
                                                    domain_files=["newbridgetest/basic.idc"], fact_files=[])
        with self.assertRaises(InstalBridgeTypeError):
            runner.run_test(query_file="newbridgetest/blank.iaq", verbose=self.verbose,
                            conditions=[])

    def test_no_terminates(self):
        bridge = """
        bridge bridgeName;
        source inst1;
        sink inst2;
        in_a terminates flu_a;
        """
        runner = InstalSingleShotTestRunnerFromText(input_files=[self.inst1, self.inst2], bridge_file=[bridge],
                                                    domain_files=["newbridgetest/basic.idc"], fact_files=[])
        with self.assertRaises(InstalBridgeTypeError):
            runner.run_test(query_file="newbridgetest/blank.iaq", verbose=self.verbose,
                            conditions=[])

    def test_no_when(self):
        bridge = """
        bridge bridgeName;
        source inst1;
        sink inst2;
        ni_a when flu_a;
        """
        runner = InstalSingleShotTestRunnerFromText(input_files=[self.inst1, self.inst2], bridge_file=[bridge],
                                                    domain_files=["newbridgetest/basic.idc"], fact_files=[])
        with self.assertRaises(InstalBridgeTypeError):
            runner.run_test(query_file="newbridgetest/blank.iaq", verbose=self.verbose,
                            conditions=[])
