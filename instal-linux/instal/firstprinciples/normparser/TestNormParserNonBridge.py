from instal.firstprinciples.TestEngine import InstalSingleShotTestRunnerFromText, InstalTestCase
from instal.instalexceptions import InstalParserTypeError, \
    InstalParserError


class TestNormParserNonBridge(InstalTestCase):
    inst1 = """
        institution inst_name;
        type Alpha;
        type Beta;
        exogenous event ex_a;
        exogenous event ex_b;
        exogenous event ex_no;
        inst event in_a;
        inst event in_b;
        inst event in_no;
        inst event in_no2;
        violation event vi_a;
        violation event vi_b;
        fluent flu_a;
        fluent flu_b;
        noninertial fluent nif_a;
        noninertial fluent nif_b;
        obligation fluent obl(in_a, in_b, in_no);
        obligation fluent obl(in_a, in_b, in_no2);
        """

    def test_basic_declaration(self):
        inst = self.inst1
        runner = InstalSingleShotTestRunnerFromText(input_files=[inst], bridge_file=[],
                                                    domain_files=["normparser/blank.idc"], fact_files=[])

        runner.run_test(query_file="normparser/blank.iaq", verbose=self.verbose,
                        conditions=[])

    def test_no_ipow(self):
        inst = self.inst1
        inst += "cross fluent ipow(inst_name, in_a, inst_name_2);"
        runner = InstalSingleShotTestRunnerFromText(input_files=[inst], bridge_file=[],
                                                    domain_files=["normparser/blank.idc"], fact_files=[])

        with self.assertRaises(InstalParserTypeError):
            runner.run_test(query_file="normparser/blank.iaq", verbose=self.verbose,
                            conditions=[])

    def test_no_tpow(self):
        inst = self.inst1
        inst += "cross fluent tpow(inst_name, in_a, inst_name_2);"
        runner = InstalSingleShotTestRunnerFromText(input_files=[inst], bridge_file=[],
                                                    domain_files=["normparser/blank.idc"], fact_files=[])

        with self.assertRaises(InstalParserTypeError):
            runner.run_test(query_file="normparser/blank.iaq", verbose=self.verbose,
                            conditions=[])

    def test_no_gpow(self):
        inst = self.inst1
        inst += "cross fluent gpow(inst_name, in_a, inst_name_2);"
        runner = InstalSingleShotTestRunnerFromText(input_files=[inst], bridge_file=[],
                                                    domain_files=["normparser/blank.idc"], fact_files=[])

        with self.assertRaises(InstalParserTypeError):
            runner.run_test(query_file="normparser/blank.iaq", verbose=self.verbose,
                            conditions=[])

    def test_no_xgenerates(self):
        inst = self.inst1
        inst += "in_a xgenerates in_b;"
        runner = InstalSingleShotTestRunnerFromText(input_files=[inst], bridge_file=[],
                                                    domain_files=["normparser/blank.idc"], fact_files=[])

        with self.assertRaises(InstalParserTypeError):
            runner.run_test(query_file="normparser/blank.iaq", verbose=self.verbose,
                            conditions=[])

    def test_no_xinitiates(self):
        inst = self.inst1
        inst += "in_a xinitiates flu_a;"
        runner = InstalSingleShotTestRunnerFromText(input_files=[inst], bridge_file=[],
                                                    domain_files=["normparser/blank.idc"], fact_files=[])

        with self.assertRaises(InstalParserTypeError):
            runner.run_test(query_file="normparser/blank.iaq", verbose=self.verbose,
                            conditions=[])

    def test_no_xterminates(self):
        inst = self.inst1
        inst += "in_a xterminates flu_a;"
        runner = InstalSingleShotTestRunnerFromText(input_files=[inst], bridge_file=[],
                                                    domain_files=["normparser/blank.idc"], fact_files=[])

        with self.assertRaises(InstalParserTypeError):
            runner.run_test(query_file="normparser/blank.iaq", verbose=self.verbose,
                            conditions=[])

    def test_no_source(self):
        inst = self.inst1
        inst += "source inst1;"
        runner = InstalSingleShotTestRunnerFromText(input_files=[inst], bridge_file=[],
                                                    domain_files=["normparser/blank.idc"], fact_files=[])

        with self.assertRaises(InstalParserTypeError):
            runner.run_test(query_file="normparser/blank.iaq", verbose=self.verbose,
                            conditions=[])

    def test_no_sink(self):
        inst = self.inst1
        inst += "sink inst2;"
        runner = InstalSingleShotTestRunnerFromText(input_files=[inst], bridge_file=[],
                                                    domain_files=["normparser/blank.idc"], fact_files=[])

        with self.assertRaises(InstalParserTypeError):
            runner.run_test(query_file="normparser/blank.iaq", verbose=self.verbose,
                            conditions=[])

    def test_no_bridge(self):
        inst = self.inst1
        inst += "bridge inst_name;"
        runner = InstalSingleShotTestRunnerFromText(input_files=[inst], bridge_file=[],
                                                    domain_files=["normparser/blank.idc"], fact_files=[])

        with self.assertRaises(InstalParserError):
            # Because inst/bridge is part of p_start, this is an
            # InstalParserError not a type error
            runner.run_test(query_file="normparser/blank.iaq", verbose=self.verbose,
                            conditions=[])
