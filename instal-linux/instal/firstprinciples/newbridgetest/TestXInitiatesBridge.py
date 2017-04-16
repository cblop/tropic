from instal.firstprinciples.TestEngine import InstalSingleShotTestRunnerFromText, InstalTestCase
from instal.instalexceptions import InstalTestNotImplemented, InstalBridgeCompileError, InstalParserError


class TestXInitiatesBridge(InstalTestCase):
    inst1 = """
    institution inst1;
    exogenous event sourceExEvent;
    inst event sourceInstEvent;

    sourceExEvent generates sourceInstEvent;

    initially perm(sourceInstEvent), pow(sourceInstEvent), perm(sourceExEvent);
    """

    inst2 = """
    institution inst2;

    type Alpha;
    fluent sinkFluent;

    exogenous event sinkExEvent;
    inst event sinkInstEvent;
    noninertial fluent sinkNoninertial;

    fluent sinkFluentWithArg(Alpha);

    initially perm(sinkInstEvent);
    """

    def test_xinitiate_basic(self):
        bridge = """bridge bridgeName;
        source inst1;
        sink inst2;

        sourceInstEvent xinitiates sinkFluent;

        cross fluent ipow(inst1, sinkFluent, inst2);
        initially ipow(inst1, sinkFluent, inst2);
        """
        runner = InstalSingleShotTestRunnerFromText(input_files=[self.inst1, self.inst2], bridge_file=[bridge],
                                                    domain_files=["newbridgetest/basic.idc"], fact_files=[])

        conditions = [{"holdsat": ["holdsat(sinkFluent, inst2)"]}]
        runner.run_test(query_file="newbridgetest/sourceEx.iaq", verbose=self.verbose,
                        conditions=conditions)

    def test_xinitiate_noipow(self):
        bridge = """bridge bridgeName;
        source inst1;
        sink inst2;

        sourceInstEvent xinitiates sinkFluent;

        cross fluent ipow(inst1, sinkFluent, inst2);
        """
        runner = InstalSingleShotTestRunnerFromText(input_files=[self.inst1, self.inst2], bridge_file=[bridge],
                                                    domain_files=["newbridgetest/basic.idc"], fact_files=[])

        conditions = [{"notholdsat": ["holdsat(sinkFluent, inst2)"]}]
        runner.run_test(query_file="newbridgetest/sourceEx.iaq", verbose=self.verbose,
                        conditions=conditions)

    def test_xinitiate_exevent(self):
        bridge = """bridge bridgeName;
        source inst1;
        sink inst2;

        sourceInstEvent xinitiates sinkExEvent;

        cross fluent ipow(inst1, sinkFluent, inst2);
        initially ipow(inst1, sinkFluent, inst2);
        """
        runner = InstalSingleShotTestRunnerFromText(input_files=[self.inst1, self.inst2], bridge_file=[bridge],
                                                    domain_files=["newbridgetest/basic.idc"], fact_files=[])

        with self.assertRaises(InstalParserError):
            runner.run_test(query_file="newbridgetest/sourceEx.iaq", verbose=self.verbose)

    def test_xinitiate_inevent(self):
        bridge = """bridge bridgeName;
        source inst1;
        sink inst2;

        sourceInstEvent xinitiates sinkInEvent;

        cross fluent ipow(inst1, sinkFluent, inst2);
        initially ipow(inst1, sinkFluent, inst2);
        """
        runner = InstalSingleShotTestRunnerFromText(input_files=[self.inst1, self.inst2], bridge_file=[bridge],
                                                    domain_files=["newbridgetest/basic.idc"], fact_files=[])

        with self.assertRaises(InstalParserError):
            runner.run_test(query_file="newbridgetest/sourceEx.iaq", verbose=self.verbose)

    def test_xinitiate_noninertial(self):
        bridge = """bridge bridgeName;
        source inst1;
        sink inst2;

        sourceInstEvent xinitiates sinkNonInertial;

        cross fluent ipow(inst1, sinkFluent, inst2);
        initially ipow(inst1, sinkFluent, inst2);
        """
        runner = InstalSingleShotTestRunnerFromText(input_files=[self.inst1, self.inst2], bridge_file=[bridge],
                                                    domain_files=["newbridgetest/basic.idc"], fact_files=[])

        with self.assertRaises(InstalParserError):
            runner.run_test(query_file="newbridgetest/sourceEx.iaq", verbose=self.verbose)

    def test_xinitiate_withargs(self):
        bridge = """bridge bridgeName;
        source inst1;
        sink inst2;

        sourceInstEvent xinitiates sinkFluentWithArg(a);

        cross fluent ipow(inst1, sinkFluent, inst2);
        cross fluent ipow(inst1, sinkFluentWithArg(Alpha), inst2);
        initially ipow(inst1, sinkFluent, inst2);
        initially ipow(inst1, sinkFluentWithArg(Alpha), inst2);
        """
        runner = InstalSingleShotTestRunnerFromText(input_files=[self.inst1, self.inst2], bridge_file=[bridge],
                                                    domain_files=["newbridgetest/basic.idc"], fact_files=[])
        conditions = [{"holdsat": ["holdsat(sinkFluentWithArg(a), inst2)"]}]

        runner.run_test(query_file="newbridgetest/sourceEx.iaq", verbose=self.verbose,conditions=conditions)