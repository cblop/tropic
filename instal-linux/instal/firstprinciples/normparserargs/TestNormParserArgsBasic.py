from instal.firstprinciples.TestEngine import InstalSingleShotTestRunnerFromText, InstalTestCase
from instal.instalexceptions import InstalParserArgumentError


class TestNormParserArgsBasic(InstalTestCase):
    IAL_PRELUDE = """
    institution inst_name;
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
    """

    def test_basic_two_conditions(self):
        ial = self.IAL_PRELUDE + "in_one(A) generates in_one(A), in_one(A);"
        runner = InstalSingleShotTestRunnerFromText(input_files=[ial], bridge_file=None,
                                                    domain_files=["normparserargs/domain.idc"], fact_files=[])

        runner.run_test(query_file="normparserargs/blank.iaq", verbose=self.verbose,
                        conditions=[])

    def test_wrong_number_of_args_lhs(self):
        ial = self.IAL_PRELUDE + "in_one(A, B) generates in_one(A), in_one(A);"
        runner = InstalSingleShotTestRunnerFromText(input_files=[ial], bridge_file=None,
                                                    domain_files=["normparserargs/domain.idc"], fact_files=[])

        with self.assertRaises(InstalParserArgumentError):
            runner.run_test(query_file="normparserargs/blank.iaq", verbose=self.verbose,
                            conditions=[])

    def test_wrong_number_of_args_rhs_1(self):
        ial = self.IAL_PRELUDE + "in_one(A) generates in_one(A, B), in_one(A);"
        runner = InstalSingleShotTestRunnerFromText(input_files=[ial], bridge_file=None,
                                                    domain_files=["normparserargs/domain.idc"], fact_files=[])

        with self.assertRaises(InstalParserArgumentError):
            runner.run_test(query_file="normparserargs/blank.iaq", verbose=self.verbose,
                            conditions=[])

    def test_wrong_number_of_args_rhs_2(self):
        ial = self.IAL_PRELUDE + "in_one(A) generates in_one(A), in_one(A, B);"
        runner = InstalSingleShotTestRunnerFromText(input_files=[ial], bridge_file=None,
                                                    domain_files=["normparserargs/domain.idc"], fact_files=[])

        with self.assertRaises(InstalParserArgumentError):
            runner.run_test(query_file="normparserargs/blank.iaq", verbose=self.verbose,
                            conditions=[])

    def test_overlapping_args_oneterm_lhs(self):
        ial = self.IAL_PRELUDE + "in_two(A, A) generates in_one(A), in_one(A);"
        runner = InstalSingleShotTestRunnerFromText(input_files=[ial], bridge_file=None,
                                                    domain_files=["normparserargs/domain.idc"], fact_files=[])

        with self.assertRaises(InstalParserArgumentError):
            runner.run_test(query_file="normparserargs/blank.iaq", verbose=self.verbose,
                            conditions=[])

    def test_overlapping_args_oneterm_rhs_1(self):
        ial = self.IAL_PRELUDE + \
            "in_two(A, B) generates in_two(A, A), in_one(A);"
        runner = InstalSingleShotTestRunnerFromText(input_files=[ial], bridge_file=None,
                                                    domain_files=["normparserargs/domain.idc"], fact_files=[])

        with self.assertRaises(InstalParserArgumentError):
            runner.run_test(query_file="normparserargs/blank.iaq", verbose=self.verbose,
                            conditions=[])

    def test_overlapping_args_oneterm_rhs_2(self):
        ial = self.IAL_PRELUDE + \
            "in_two(A, B) generates in_two(A, B), in_two(A,A);"
        runner = InstalSingleShotTestRunnerFromText(input_files=[ial], bridge_file=None,
                                                    domain_files=["normparserargs/domain.idc"], fact_files=[])

        with self.assertRaises(InstalParserArgumentError):
            runner.run_test(query_file="normparserargs/blank.iaq", verbose=self.verbose,
                            conditions=[])

    def test_overlapping_args_twoterms(self):
        ial = self.IAL_PRELUDE + "in_two(B, A) generates in_two(A, B);"
        runner = InstalSingleShotTestRunnerFromText(input_files=[ial], bridge_file=None,
                                                    domain_files=["normparserargs/domain.idc"], fact_files=[])

        with self.assertRaises(InstalParserArgumentError):
            runner.run_test(query_file="normparserargs/blank.iaq", verbose=self.verbose,
                            conditions=[])

    def test_overlapping_args_threeterms(self):
        ial = self.IAL_PRELUDE + \
            "in_three(A, B, C) generates in_two(D, E), in_two(B, A);"
        runner = InstalSingleShotTestRunnerFromText(input_files=[ial], bridge_file=None,
                                                    domain_files=["normparserargs/domain.idc"], fact_files=[])

        with self.assertRaises(InstalParserArgumentError):
            runner.run_test(query_file="normparserargs/blank.iaq", verbose=self.verbose,
                            conditions=[])

    def test_overlapping_args_threeterms_collision(self):
        ial = self.IAL_PRELUDE + \
            "in_three(A, B, C) generates in_two(B, A), in_two(C, A);"
        runner = InstalSingleShotTestRunnerFromText(input_files=[ial], bridge_file=None,
                                                    domain_files=["normparserargs/domain.idc"], fact_files=[])

        with self.assertRaises(InstalParserArgumentError):
            runner.run_test(query_file="normparserargs/blank.iaq", verbose=self.verbose,
                            conditions=[])

    def test_initiates_okay(self):
        ial = self.IAL_PRELUDE + \
            "in_three(A, B, C) initiates flu_two(A, C), flu_two(A, C);"
        runner = InstalSingleShotTestRunnerFromText(input_files=[ial], bridge_file=None,
                                                    domain_files=["normparserargs/domain.idc"], fact_files=[])

        runner.run_test(query_file="normparserargs/blank.iaq", verbose=self.verbose,
                        conditions=[])

    def test_initiates_lhs_collide(self):
        ial = self.IAL_PRELUDE + \
            "in_three(A, B, C) initiates flu_two(A, B), flu_two(A, B);"
        runner = InstalSingleShotTestRunnerFromText(input_files=[ial], bridge_file=None,
                                                    domain_files=["normparserargs/domain.idc"], fact_files=[])

        with self.assertRaises(InstalParserArgumentError):
            runner.run_test(query_file="normparserargs/blank.iaq", verbose=self.verbose,
                            conditions=[])

    def test_initiates_collision_oneterm_lhs(self):
        ial = self.IAL_PRELUDE + \
            "in_three(A, A, A) initiates flu_two(C, D), flu_two(E, B);"
        runner = InstalSingleShotTestRunnerFromText(input_files=[ial], bridge_file=None,
                                                    domain_files=["normparserargs/domain.idc"], fact_files=[])

        with self.assertRaises(InstalParserArgumentError):
            runner.run_test(query_file="normparserargs/blank.iaq", verbose=self.verbose,
                            conditions=[])

    def test_initiates_collision_oneterm_rhs(self):
        ial = self.IAL_PRELUDE + \
            "in_three(A, B, C) initiates flu_two(A, A), flu_two(E, B);"
        runner = InstalSingleShotTestRunnerFromText(input_files=[ial], bridge_file=None,
                                                    domain_files=["normparserargs/domain.idc"], fact_files=[])

        with self.assertRaises(InstalParserArgumentError):
            runner.run_test(query_file="normparserargs/blank.iaq", verbose=self.verbose,
                            conditions=[])

    def test_initiates_collision_twoterms(self):
        ial = self.IAL_PRELUDE + \
            "in_three(A, B, C) initiates flu_two(A, B), flu_two(B, A);"
        runner = InstalSingleShotTestRunnerFromText(input_files=[ial], bridge_file=None,
                                                    domain_files=["normparserargs/domain.idc"], fact_files=[])

        with self.assertRaises(InstalParserArgumentError):
            runner.run_test(query_file="normparserargs/blank.iaq", verbose=self.verbose,
                            conditions=[])

    def test_initiates_collision_threeterms(self):
        ial = self.IAL_PRELUDE + \
            "in_three(A, B, C) initiates flu_two(C, A), flu_two(B, A);"
        runner = InstalSingleShotTestRunnerFromText(input_files=[ial], bridge_file=None,
                                                    domain_files=["normparserargs/domain.idc"], fact_files=[])

        with self.assertRaises(InstalParserArgumentError):
            runner.run_test(query_file="normparserargs/blank.iaq", verbose=self.verbose,
                            conditions=[])

    def test_terminates_okay(self):
        ial = self.IAL_PRELUDE + \
            "in_three(A, B, C) terminates flu_two(A, C), flu_two(A, C);"
        runner = InstalSingleShotTestRunnerFromText(input_files=[ial], bridge_file=None,
                                                    domain_files=["normparserargs/domain.idc"], fact_files=[])

        runner.run_test(query_file="normparserargs/blank.iaq", verbose=self.verbose,
                        conditions=[])

    def test_terminates_lhs_collide(self):
        ial = self.IAL_PRELUDE + \
            "in_three(A, B, C) terminates flu_two(A, B), flu_two(A, B);"
        runner = InstalSingleShotTestRunnerFromText(input_files=[ial], bridge_file=None,
                                                    domain_files=["normparserargs/domain.idc"], fact_files=[])

        with self.assertRaises(InstalParserArgumentError):
            runner.run_test(query_file="normparserargs/blank.iaq", verbose=self.verbose,
                            conditions=[])

    def test_terminates_collision_oneterm_lhs(self):
        ial = self.IAL_PRELUDE + \
            "in_three(A, A, A) terminates flu_two(C, D), flu_two(E, B);"
        runner = InstalSingleShotTestRunnerFromText(input_files=[ial], bridge_file=None,
                                                    domain_files=["normparserargs/domain.idc"], fact_files=[])

        with self.assertRaises(InstalParserArgumentError):
            runner.run_test(query_file="normparserargs/blank.iaq", verbose=self.verbose,
                            conditions=[])

    def test_terminates_collision_oneterm_rhs(self):
        ial = self.IAL_PRELUDE + \
            "in_three(A, B, C) initiates flu_two(A, A), flu_two(E, B);"
        runner = InstalSingleShotTestRunnerFromText(input_files=[ial], bridge_file=None,
                                                    domain_files=["normparserargs/domain.idc"], fact_files=[])

        with self.assertRaises(InstalParserArgumentError):
            runner.run_test(query_file="normparserargs/blank.iaq", verbose=self.verbose,
                            conditions=[])

    def test_terminates_collision_twoterms(self):
        ial = self.IAL_PRELUDE + \
            "in_three(A, B, C) initiates flu_two(A, B), flu_two(B, A);"
        runner = InstalSingleShotTestRunnerFromText(input_files=[ial], bridge_file=None,
                                                    domain_files=["normparserargs/domain.idc"], fact_files=[])

        with self.assertRaises(InstalParserArgumentError):
            runner.run_test(query_file="normparserargs/blank.iaq", verbose=self.verbose,
                            conditions=[])

    def test_terminates_collision_threeterms(self):
        ial = self.IAL_PRELUDE + \
            "in_three(A, B, C) initiates flu_two(C, A), flu_two(B, A);"
        runner = InstalSingleShotTestRunnerFromText(input_files=[ial], bridge_file=None,
                                                    domain_files=["normparserargs/domain.idc"], fact_files=[])

        with self.assertRaises(InstalParserArgumentError):
            runner.run_test(query_file="normparserargs/blank.iaq", verbose=self.verbose,
                            conditions=[])

    def test_when_okay(self):
        ial = self.IAL_PRELUDE + \
            "ni_three(A, B, C) when flu_two(A, C), flu_two(A, C);"
        runner = InstalSingleShotTestRunnerFromText(input_files=[ial], bridge_file=None,
                                                    domain_files=["normparserargs/domain.idc"], fact_files=[])

        runner.run_test(query_file="normparserargs/blank.iaq", verbose=self.verbose,
                        conditions=[])

    def test_when_lhs_collide(self):
        ial = self.IAL_PRELUDE + \
            "ni_three(A, B, C) when flu_two(A, B), flu_two(A, B);"
        runner = InstalSingleShotTestRunnerFromText(input_files=[ial], bridge_file=None,
                                                    domain_files=["normparserargs/domain.idc"], fact_files=[])

        with self.assertRaises(InstalParserArgumentError):
            runner.run_test(query_file="normparserargs/blank.iaq", verbose=self.verbose,
                            conditions=[])

    def test_when_collision_oneterm_lhs(self):
        ial = self.IAL_PRELUDE + \
            "ni_three(A, A, A) when flu_two(C, D), flu_two(E, B);"
        runner = InstalSingleShotTestRunnerFromText(input_files=[ial], bridge_file=None,
                                                    domain_files=["normparserargs/domain.idc"], fact_files=[])

        with self.assertRaises(InstalParserArgumentError):
            runner.run_test(query_file="normparserargs/blank.iaq", verbose=self.verbose,
                            conditions=[])

    def test_when_collision_oneterm_rhs(self):
        ial = self.IAL_PRELUDE + \
            "ni_three(A, B, C) when flu_two(A, A), flu_two(E, B);"
        runner = InstalSingleShotTestRunnerFromText(input_files=[ial], bridge_file=None,
                                                    domain_files=["normparserargs/domain.idc"], fact_files=[])

        with self.assertRaises(InstalParserArgumentError):
            runner.run_test(query_file="normparserargs/blank.iaq", verbose=self.verbose,
                            conditions=[])

    def test_when_collision_twoterms(self):
        ial = self.IAL_PRELUDE + \
            "ni_three(A, B, C) when flu_two(A, B), flu_two(B, A);"
        runner = InstalSingleShotTestRunnerFromText(input_files=[ial], bridge_file=None,
                                                    domain_files=["normparserargs/domain.idc"], fact_files=[])

        with self.assertRaises(InstalParserArgumentError):
            runner.run_test(query_file="normparserargs/blank.iaq", verbose=self.verbose,
                            conditions=[])

    def test_when_collision_threeterms(self):
        ial = self.IAL_PRELUDE + \
            "ni_three(A, B, C) when flu_two(C, A), flu_two(B, A);"
        runner = InstalSingleShotTestRunnerFromText(input_files=[ial], bridge_file=None,
                                                    domain_files=["normparserargs/domain.idc"], fact_files=[])

        with self.assertRaises(InstalParserArgumentError):
            runner.run_test(query_file="normparserargs/blank.iaq", verbose=self.verbose,
                            conditions=[])
