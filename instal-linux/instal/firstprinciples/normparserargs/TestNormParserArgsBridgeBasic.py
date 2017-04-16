from instal.firstprinciples.TestEngine import InstalSingleShotTestRunnerFromText, InstalTestCase
from instal.instalexceptions import InstalParserArgumentError


class TestNormParserArgsObls(InstalTestCase):
    inst1 = """
    institution inst1;
    type Alpha; % Ground with {a, b}
    type Beta; % Ground with {c}
    inst event in_zero;
    inst event in_one(Alpha);
    inst event in_two(Alpha, Beta);
    inst event in_three(Alpha, Alpha, Beta);
    fluent flu_zero;
    fluent flu_one(Alpha);
    fluent flu_two(Alpha, Beta);
    fluent flu_three(Alpha, Alpha, Beta);
    noninertial fluent ni_zero;
    noninertial fluent ni_one(Alpha);
    noninertial fluent ni_two(Alpha, Beta);
    noninertial fluent ni_three(Alpha, Alpha, Beta);

    inst event deadline_2(Alpha, Beta);
    inst event viol_2(Alpha, Beta);

    obligation fluent obl(in_two(Alpha, Beta), deadline_2(Alpha, Beta), viol_2(Alpha, Beta));
    """

    inst2 = """
    institution inst2;
    type Alpha; % Ground with {a, b}
    type Beta; % Ground with {c}
    exogenous event in_zero;
    exogenous event in_one(Alpha);
    exogenous event in_two(Alpha, Beta);
    exogenous event in_three(Alpha, Alpha, Beta);
    fluent flu_zero;
    fluent flu_one(Alpha);
    fluent flu_two(Alpha, Beta);
    fluent flu_three(Alpha, Alpha, Beta);
    noninertial fluent ni_zero;
    noninertial fluent ni_one(Alpha);
    noninertial fluent ni_two(Alpha, Beta);
    noninertial fluent ni_three(Alpha, Alpha, Beta);

    inst event deadline_2(Alpha, Beta);
    inst event viol_2(Alpha, Beta);
    inst event obl_a(Alpha, Beta);

    obligation fluent obl(obl_a(Alpha, Beta), deadline_2(Alpha, Beta), viol_2(Alpha, Beta));
    """

    BRIDGE_PRELUDE = """
    bridge bridgeName;
    source inst1;
    sink inst2;
    """

    def test_basic_two_conditions(self):
        bridge = self.BRIDGE_PRELUDE + \
            "in_one(A) xgenerates in_one(A), in_one(A);"
        runner = InstalSingleShotTestRunnerFromText(input_files=[self.inst1, self.inst2], bridge_file=[bridge],
                                                    domain_files=["normparserargs/domain.idc"], fact_files=[])

        runner.run_test(query_file="normparserargs/blank.iaq", verbose=self.verbose,
                        conditions=[])

    def test_wrong_number_of_args_lhs(self):
        bridge = self.BRIDGE_PRELUDE + \
            "in_one(A, B) xgenerates in_one(A), in_one(A);"
        runner = InstalSingleShotTestRunnerFromText(input_files=[self.inst1, self.inst2], bridge_file=[bridge],
                                                    domain_files=["normparserargs/domain.idc"], fact_files=[])

        with self.assertRaises(InstalParserArgumentError):
            runner.run_test(query_file="normparserargs/blank.iaq", verbose=self.verbose,
                            conditions=[])

    def test_wrong_number_of_args_rhs_1(self):
        bridge = self.BRIDGE_PRELUDE + \
            "in_one(A) xgenerates in_one(A, B), in_one(A);"
        runner = InstalSingleShotTestRunnerFromText(input_files=[self.inst1, self.inst2], bridge_file=[bridge],
                                                    domain_files=["normparserargs/domain.idc"], fact_files=[])

        with self.assertRaises(InstalParserArgumentError):
            runner.run_test(query_file="normparserargs/blank.iaq", verbose=self.verbose,
                            conditions=[])

    def test_wrong_number_of_args_rhs_2(self):
        bridge = self.BRIDGE_PRELUDE + \
            "in_one(A) xgenerates in_one(A), in_one(A, B);"
        runner = InstalSingleShotTestRunnerFromText(input_files=[self.inst1, self.inst2], bridge_file=[bridge],
                                                    domain_files=["normparserargs/domain.idc"], fact_files=[])

        with self.assertRaises(InstalParserArgumentError):
            runner.run_test(query_file="normparserargs/blank.iaq", verbose=self.verbose,
                            conditions=[])

    def test_overlapping_args_oneterm_lhs(self):
        bridge = self.BRIDGE_PRELUDE + \
            "in_two(A, A) xgenerates in_one(A), in_one(A);"
        runner = InstalSingleShotTestRunnerFromText(input_files=[self.inst1, self.inst2], bridge_file=[bridge],
                                                    domain_files=["normparserargs/domain.idc"], fact_files=[])

        with self.assertRaises(InstalParserArgumentError):
            runner.run_test(query_file="normparserargs/blank.iaq", verbose=self.verbose,
                            conditions=[])

    def test_overlapping_args_oneterm_rhs_1(self):
        bridge = self.BRIDGE_PRELUDE + \
            "in_two(A, B) xgenerates in_two(A, A), in_one(A);"
        runner = InstalSingleShotTestRunnerFromText(input_files=[self.inst1, self.inst2], bridge_file=[bridge],
                                                    domain_files=["normparserargs/domain.idc"], fact_files=[])

        with self.assertRaises(InstalParserArgumentError):
            runner.run_test(query_file="normparserargs/blank.iaq", verbose=self.verbose,
                            conditions=[])

    def test_overlapping_args_oneterm_rhs_2(self):
        bridge = self.BRIDGE_PRELUDE + \
            "in_two(A, B) xgenerates in_two(A, B), in_two(A,A);"
        runner = InstalSingleShotTestRunnerFromText(input_files=[self.inst1, self.inst2], bridge_file=[bridge],
                                                    domain_files=["normparserargs/domain.idc"], fact_files=[])

        with self.assertRaises(InstalParserArgumentError):
            runner.run_test(query_file="normparserargs/blank.iaq", verbose=self.verbose,
                            conditions=[])

    def test_overlapping_args_twoterms(self):
        bridge = self.BRIDGE_PRELUDE + "in_two(B, A) xgenerates in_two(A, B);"
        runner = InstalSingleShotTestRunnerFromText(input_files=[self.inst1, self.inst2], bridge_file=[bridge],
                                                    domain_files=["normparserargs/domain.idc"], fact_files=[])

        with self.assertRaises(InstalParserArgumentError):
            runner.run_test(query_file="normparserargs/blank.iaq", verbose=self.verbose,
                            conditions=[])

    def test_overlapping_args_threeterms(self):
        bridge = self.BRIDGE_PRELUDE + \
            "in_three(A, B, C) xgenerates in_two(D, E), in_two(B, A);"
        runner = InstalSingleShotTestRunnerFromText(input_files=[self.inst1, self.inst2], bridge_file=[bridge],
                                                    domain_files=["normparserargs/domain.idc"], fact_files=[])

        with self.assertRaises(InstalParserArgumentError):
            runner.run_test(query_file="normparserargs/blank.iaq", verbose=self.verbose,
                            conditions=[])

    def test_overlapping_args_threeterms_collision(self):
        bridge = self.BRIDGE_PRELUDE + \
            "in_three(A, B, C) xgenerates in_two(B, A), in_two(C, A);"
        runner = InstalSingleShotTestRunnerFromText(input_files=[self.inst1, self.inst2], bridge_file=[bridge],
                                                    domain_files=["normparserargs/domain.idc"], fact_files=[])

        with self.assertRaises(InstalParserArgumentError):
            runner.run_test(query_file="normparserargs/blank.iaq", verbose=self.verbose,
                            conditions=[])

    def test_xinitiates_okay(self):
        bridge = self.BRIDGE_PRELUDE + \
            "in_three(A, B, C) xinitiates flu_two(A, C), flu_two(A, C);"
        runner = InstalSingleShotTestRunnerFromText(input_files=[self.inst1, self.inst2], bridge_file=[bridge],
                                                    domain_files=["normparserargs/domain.idc"], fact_files=[])

        runner.run_test(query_file="normparserargs/blank.iaq", verbose=self.verbose,
                        conditions=[])

    def test_xinitiates_lhs_collide(self):
        bridge = self.BRIDGE_PRELUDE + \
            "in_three(A, B, C) xinitiates flu_two(A, B), flu_two(A, B);"
        runner = InstalSingleShotTestRunnerFromText(input_files=[self.inst1, self.inst2], bridge_file=[bridge],
                                                    domain_files=["normparserargs/domain.idc"], fact_files=[])

        with self.assertRaises(InstalParserArgumentError):
            runner.run_test(query_file="normparserargs/blank.iaq", verbose=self.verbose,
                            conditions=[])

    def test_xinitiates_collision_oneterm_lhs(self):
        bridge = self.BRIDGE_PRELUDE + \
            "in_three(A, A, A) xinitiates flu_two(C, D), flu_two(E, B);"
        runner = InstalSingleShotTestRunnerFromText(input_files=[self.inst1, self.inst2], bridge_file=[bridge],
                                                    domain_files=["normparserargs/domain.idc"], fact_files=[])

        with self.assertRaises(InstalParserArgumentError):
            runner.run_test(query_file="normparserargs/blank.iaq", verbose=self.verbose,
                            conditions=[])

    def test_xinitiates_collision_oneterm_rhs(self):
        bridge = self.BRIDGE_PRELUDE + \
            "in_three(A, B, C) xinitiates flu_two(A, A), flu_two(E, B);"
        runner = InstalSingleShotTestRunnerFromText(input_files=[self.inst1, self.inst2], bridge_file=[bridge],
                                                    domain_files=["normparserargs/domain.idc"], fact_files=[])

        with self.assertRaises(InstalParserArgumentError):
            runner.run_test(query_file="normparserargs/blank.iaq", verbose=self.verbose,
                            conditions=[])

    def test_xinitiates_collision_twoterms(self):
        bridge = self.BRIDGE_PRELUDE + \
            "in_three(A, B, C) xinitiates flu_two(A, B), flu_two(B, A);"
        runner = InstalSingleShotTestRunnerFromText(input_files=[self.inst1, self.inst2], bridge_file=[bridge],
                                                    domain_files=["normparserargs/domain.idc"], fact_files=[])

        with self.assertRaises(InstalParserArgumentError):
            runner.run_test(query_file="normparserargs/blank.iaq", verbose=self.verbose,
                            conditions=[])

    def test_xinitiates_collision_threeterms(self):
        bridge = self.BRIDGE_PRELUDE + \
            "in_three(A, B, C) xinitiates flu_two(C, A), flu_two(B, A);"
        runner = InstalSingleShotTestRunnerFromText(input_files=[self.inst1, self.inst2], bridge_file=[bridge],
                                                    domain_files=["normparserargs/domain.idc"], fact_files=[])

        with self.assertRaises(InstalParserArgumentError):
            runner.run_test(query_file="normparserargs/blank.iaq", verbose=self.verbose,
                            conditions=[])

    def test_xterminates_okay(self):
        bridge = self.BRIDGE_PRELUDE + \
            "in_three(A, B, C) xterminates flu_two(A, C), flu_two(A, C);"
        runner = InstalSingleShotTestRunnerFromText(input_files=[self.inst1, self.inst2], bridge_file=[bridge],
                                                    domain_files=["normparserargs/domain.idc"], fact_files=[])

        runner.run_test(query_file="normparserargs/blank.iaq", verbose=self.verbose,
                        conditions=[])

    def test_xterminates_lhs_collide(self):
        bridge = self.BRIDGE_PRELUDE + \
            "in_three(A, B, C) xterminates flu_two(A, B), flu_two(A, B);"
        runner = InstalSingleShotTestRunnerFromText(input_files=[self.inst1, self.inst2], bridge_file=[bridge],
                                                    domain_files=["normparserargs/domain.idc"], fact_files=[])

        with self.assertRaises(InstalParserArgumentError):
            runner.run_test(query_file="normparserargs/blank.iaq", verbose=self.verbose,
                            conditions=[])

    def test_xterminates_collision_oneterm_lhs(self):
        bridge = self.BRIDGE_PRELUDE + \
            "in_three(A, A, A) xterminates flu_two(C, D), flu_two(E, B);"
        runner = InstalSingleShotTestRunnerFromText(input_files=[self.inst1, self.inst2], bridge_file=[bridge],
                                                    domain_files=["normparserargs/domain.idc"], fact_files=[])

        with self.assertRaises(InstalParserArgumentError):
            runner.run_test(query_file="normparserargs/blank.iaq", verbose=self.verbose,
                            conditions=[])

    def test_xterminates_collision_oneterm_rhs(self):
        bridge = self.BRIDGE_PRELUDE + \
            "in_three(A, B, C) xinitiates flu_two(A, A), flu_two(E, B);"
        runner = InstalSingleShotTestRunnerFromText(input_files=[self.inst1, self.inst2], bridge_file=[bridge],
                                                    domain_files=["normparserargs/domain.idc"], fact_files=[])

        with self.assertRaises(InstalParserArgumentError):
            runner.run_test(query_file="normparserargs/blank.iaq", verbose=self.verbose,
                            conditions=[])

    def test_xterminates_collision_twoterms(self):
        bridge = self.BRIDGE_PRELUDE + \
            "in_three(A, B, C) xinitiates flu_two(A, B), flu_two(B, A);"
        runner = InstalSingleShotTestRunnerFromText(input_files=[self.inst1, self.inst2], bridge_file=[bridge],
                                                    domain_files=["normparserargs/domain.idc"], fact_files=[])

        with self.assertRaises(InstalParserArgumentError):
            runner.run_test(query_file="normparserargs/blank.iaq", verbose=self.verbose,
                            conditions=[])

    def test_xterminates_collision_threeterms(self):
        bridge = self.BRIDGE_PRELUDE + \
            "in_three(A, B, C) xinitiates flu_two(C, A), flu_two(B, A);"
        runner = InstalSingleShotTestRunnerFromText(input_files=[self.inst1, self.inst2], bridge_file=[bridge],
                                                    domain_files=["normparserargs/domain.idc"], fact_files=[])

        with self.assertRaises(InstalParserArgumentError):
            runner.run_test(query_file="normparserargs/blank.iaq", verbose=self.verbose,
                            conditions=[])
