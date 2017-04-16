from instal.firstprinciples.TestEngine import InstalSingleShotTestRunnerFromText, InstalTestCase
from instal.instalexceptions import InstalBridgeParserError, InstalParserError


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
    exogenous event sinkExEvent;
    inst event sinkInstEvent;

    initially perm(sinkExEvent);
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

    def test_basic_declaration_noname(self):
        bridge = """
        source inst1;
        sink inst2;
        """
        runner = InstalSingleShotTestRunnerFromText(input_files=[self.inst1, self.inst2], bridge_file=[bridge],
                                                    domain_files=["newbridgetest/basic.idc"], fact_files=[])

        with self.assertRaises(InstalParserError):
            runner.run_test(query_file="newbridgetest/blank.iaq", verbose=self.verbose,
                            conditions=[])

    def test_basic_declaration_nosource(self):
        bridge = """ bridge bridgeName;
        sink inst2;
        """
        runner = InstalSingleShotTestRunnerFromText(input_files=[self.inst1, self.inst2], bridge_file=[bridge],
                                                    domain_files=["newbridgetest/basic.idc"], fact_files=[])

        with self.assertRaises(InstalBridgeParserError):
            runner.run_test(query_file="newbridgetest/blank.iaq", verbose=self.verbose,
                            conditions=[])

    def test_basic_declaration_nosink(self):
        bridge = """ bridge bridgeName;
        source inst1;
        """
        runner = InstalSingleShotTestRunnerFromText(input_files=[self.inst1, self.inst2], bridge_file=[bridge],
                                                    domain_files=["newbridgetest/basic.idc"], fact_files=[])

        with self.assertRaises(InstalBridgeParserError):
            runner.run_test(query_file="newbridgetest/blank.iaq", verbose=self.verbose,
                            conditions=[])

    def test_basic_declaration_same_sink_and_source(self):
        bridge = """ bridge bridgeName;
        source inst1;
        sink inst1;
        """
        runner = InstalSingleShotTestRunnerFromText(input_files=[self.inst1, self.inst2], bridge_file=[bridge],
                                                    domain_files=["newbridgetest/basic.idc"], fact_files=[])

        with self.assertRaises(InstalBridgeParserError):
            runner.run_test(query_file="newbridgetest/blank.iaq", verbose=self.verbose,
                            conditions=[])

    def test_basic_declaration_live(self):
        bridge = """bridge bridgeName;
        source inst1;
        sink inst2;
        """
        runner = InstalSingleShotTestRunnerFromText(input_files=[self.inst1, self.inst2], bridge_file=[bridge],
                                                    domain_files=["newbridgetest/basic.idc"], fact_files=[])

        conditions = [{"holdsat": ["holdsat(live(inst1), inst1)", "holdsat(live(inst2), inst2)",
                                   "holdsat(live(bridgeName), bridgeName)"]}]
        runner.run_test(query_file="newbridgetest/blank.iaq", verbose=self.verbose,
                        conditions=conditions)

    def test_basic_declare_crossfluent(self):
        bridge = """bridge bridgeName;
        source inst1;
        sink inst2;

        cross fluent ipow(inst1, sinkFluent, inst2);
        cross fluent tpow(inst1, sinkFluent, inst2);
        cross fluent gpow(inst1, sinkExEvent, inst2);
        """
        runner = InstalSingleShotTestRunnerFromText(input_files=[self.inst1, self.inst2], bridge_file=[bridge],
                                                    domain_files=["newbridgetest/basic.idc"], fact_files=[])

        runner.run_test(query_file="newbridgetest/blank.iaq", verbose=self.verbose,
                        conditions=[])

    def test_basic_declare_xinitiates(self):
        bridge = """bridge bridgeName;
        source inst1;
        sink inst2;

        sourceInstEvent xinitiates sinkFluent;
        """
        runner = InstalSingleShotTestRunnerFromText(input_files=[self.inst1, self.inst2], bridge_file=[bridge],
                                                    domain_files=["newbridgetest/basic.idc"], fact_files=[])

        runner.run_test(query_file="newbridgetest/blank.iaq", verbose=self.verbose,
                        conditions=[])

    def test_basic_declare_xinitiates_exogenous(self):
        bridge = """bridge bridgeName;
        source inst1;
        sink inst2;

        sourceExEvent xinitiates sinkFluent;
        """
        runner = InstalSingleShotTestRunnerFromText(input_files=[self.inst1, self.inst2], bridge_file=[bridge],
                                                    domain_files=["newbridgetest/basic.idc"], fact_files=[])

        with self.assertRaises(InstalParserError):
            runner.run_test(query_file="newbridgetest/blank.iaq", verbose=self.verbose,
                            conditions=[])

    def test_basic_declare_xterminates(self):
        bridge = """bridge bridgeName;
        source inst1;
        sink inst2;

        sourceInstEvent xterminates sinkFluent;
        """
        runner = InstalSingleShotTestRunnerFromText(input_files=[self.inst1, self.inst2], bridge_file=[bridge],
                                                    domain_files=["newbridgetest/basic.idc"], fact_files=[])

        runner.run_test(query_file="newbridgetest/blank.iaq", verbose=self.verbose,
                        conditions=[])

    def test_basic_declare_xterminates_exogenous(self):
        bridge = """bridge bridgeName;
        source inst1;
        sink inst2;

        sourceExEvent xterminates sinkFluent;
        """
        runner = InstalSingleShotTestRunnerFromText(input_files=[self.inst1, self.inst2], bridge_file=[bridge],
                                                    domain_files=["newbridgetest/basic.idc"], fact_files=[])

        with self.assertRaises(InstalParserError):
            runner.run_test(query_file="newbridgetest/blank.iaq", verbose=self.verbose,
                            conditions=[])

    def test_basic_declare_xgenerates(self):
        bridge = """bridge testBridge;
        source inst1;
        sink inst2;

        sourceInstEvent xgenerates sinkExEvent;
        """
        runner = InstalSingleShotTestRunnerFromText(input_files=[self.inst1, self.inst2], bridge_file=[bridge],
                                                    domain_files=["newbridgetest/basic.idc"], fact_files=[])

        runner.run_test(query_file="newbridgetest/blank.iaq", verbose=self.verbose,
                        conditions=[])

    def test_basic_declare_xgenerates_exogenous(self):
        bridge = """bridge bridgeName;
        source inst1;
        sink inst2;

        sourceExEvent xgenerates sinkExEvent;
        """
        runner = InstalSingleShotTestRunnerFromText(input_files=[self.inst1, self.inst2], bridge_file=[bridge],
                                                    domain_files=["newbridgetest/basic.idc"], fact_files=[])

        with self.assertRaises(InstalParserError):
            runner.run_test(query_file="newbridgetest/blank.iaq", verbose=self.verbose,
                            conditions=[])
