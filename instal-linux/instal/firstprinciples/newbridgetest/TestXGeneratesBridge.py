from instal.firstprinciples.TestEngine import InstalSingleShotTestRunnerFromText, InstalTestCase
from instal.instalexceptions import InstalTestNotImplemented, InstalBridgeCompileError, InstalParserError


class TestXGeneratesBridge(InstalTestCase):
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
    exogenous event sinkExWithArg(Alpha);
    inst event sinkInstEvent;
    violation event sinkViolEvent;
    noninertial fluent sinkNoninertial;
    

    initially perm(sinkExEvent);
    initially perm(sinkExWithArg(Alpha));
    """

    def test_xgenerates_basic(self):
        bridge = """bridge bridgeName;
        source inst1;
        sink inst2;

        sourceInstEvent xgenerates sinkExEvent;

        cross fluent gpow(inst1, sinkExEvent, inst2);
        initially gpow(inst1, sinkExEvent, inst2);
        """
        runner = InstalSingleShotTestRunnerFromText(input_files=[self.inst1, self.inst2], bridge_file=[bridge],
                                                    domain_files=["newbridgetest/basic.idc"], fact_files=[])

        conditions = [{"occurred": ["occurred(sinkExEvent, inst2)"]}]
        runner.run_test(query_file="newbridgetest/sourceEx.iaq", verbose=self.verbose,
                        conditions=conditions)

    def test_xgenerates_nogpow(self):
        bridge = """bridge bridgeName;
        source inst1;
        sink inst2;

        sourceInstEvent xgenerates sinkExEvent;

        cross fluent gpow(inst1, sinkExEvent, inst2);
        """
        runner = InstalSingleShotTestRunnerFromText(input_files=[self.inst1, self.inst2], bridge_file=[bridge],
                                                    domain_files=["newbridgetest/basic.idc"], fact_files=[])

        conditions = [{"notoccurred": ["occurred(sinkExEvent, inst2)"]}]
        runner.run_test(query_file="newbridgetest/sourceEx.iaq", verbose=self.verbose,
                        conditions=conditions)

    def test_xgenerates_inst(self):
        bridge = """bridge bridgeName;
        source inst1;
        sink inst2;

        sourceInstEvent xgenerates sinkInstEvent;

        cross fluent gpow(inst1, sinkExEvent, inst2);
        """
        runner = InstalSingleShotTestRunnerFromText(input_files=[self.inst1, self.inst2], bridge_file=[bridge],
                                                    domain_files=["newbridgetest/basic.idc"], fact_files=[])

        with self.assertRaises(InstalParserError):
            runner.run_test(query_file="newbridgetest/sourceEx.iaq", verbose=self.verbose)


    def test_xgenerates_viol(self):
        bridge = """bridge bridgeName;
        source inst1;
        sink inst2;

        sourceInstEvent xgenerates sinkViolEvent;

        cross fluent gpow(inst1, sinkExEvent, inst2);
        """
        runner = InstalSingleShotTestRunnerFromText(input_files=[self.inst1, self.inst2], bridge_file=[bridge],
                                                    domain_files=["newbridgetest/basic.idc"], fact_files=[])

        with self.assertRaises(InstalParserError):
            runner.run_test(query_file="newbridgetest/sourceEx.iaq", verbose=self.verbose)


    def test_xgenerates_fluent(self):
        bridge = """bridge bridgeName;
        source inst1;
        sink inst2;

        sourceInstEvent xgenerates sinkFluent;

        cross fluent gpow(inst1, sinkExEvent, inst2);
        """
        runner = InstalSingleShotTestRunnerFromText(input_files=[self.inst1, self.inst2], bridge_file=[bridge],
                                                    domain_files=["newbridgetest/basic.idc"], fact_files=[])

        with self.assertRaises(InstalParserError):
            runner.run_test(query_file="newbridgetest/sourceEx.iaq", verbose=self.verbose)

    def test_xgenerates_withargs(self):
        bridge = """bridge bridgeName;
        source inst1;
        sink inst2;

        sourceInstEvent xgenerates sinkExWithArg(a);

        cross fluent gpow(inst1, sinkExEvent, inst2);
        initially gpow(inst1, sinkExEvent, inst2);
        initially gpow(inst1, sinkExWithArg(Alpha), inst2);
        """
        runner = InstalSingleShotTestRunnerFromText(input_files=[self.inst1, self.inst2], bridge_file=[bridge],
                                                    domain_files=["newbridgetest/basic.idc"], fact_files=[])

        conditions = [{"occurred": ["occurred(sinkExWithArg(a), inst2)"]}]
        runner.run_test(query_file="newbridgetest/sourceEx.iaq", verbose=self.verbose,
                        conditions=conditions)