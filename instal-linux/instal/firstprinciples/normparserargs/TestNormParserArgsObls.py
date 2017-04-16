from instal.firstprinciples.TestEngine import InstalSingleShotTestRunnerFromText, InstalTestCase
from instal.instalexceptions import InstalParserArgumentError, InstalParserError


class TestNormParserArgsObls(InstalTestCase):
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

    inst event deadline_2(Alpha, Beta);
    inst event viol_2(Alpha, Beta);

    obligation fluent obl(in_two(Alpha, Beta), deadline_2(Alpha, Beta), viol_2(Alpha, Beta));
    """

    def test_initiates_obls_okay(self):
        ial = self.IAL_PRELUDE + \
            "in_three(A, B, C) initiates obl(in_two(A, C), deadline_2(A, C), viol_2(B, C));"
        runner = InstalSingleShotTestRunnerFromText(input_files=[ial], bridge_file=None,
                                                    domain_files=["normparserargs/domain.idc"], fact_files=[])

        runner.run_test(query_file="normparserargs/blank.iaq", verbose=self.verbose,
                        conditions=[])

    def test_initiates_wrongnumber_args_lhs(self):
        ial = self.IAL_PRELUDE + \
            "in_three(A, B) initiates obl(in_two(A, C), deadline_2(A, D), viol_2(D, C));"
        runner = InstalSingleShotTestRunnerFromText(input_files=[ial], bridge_file=None,
                                                    domain_files=["normparserargs/domain.idc"], fact_files=[])

        with self.assertRaises(InstalParserArgumentError):
            runner.run_test(query_file="normparserargs/blank.iaq", verbose=self.verbose,
                            conditions=[])

    def test_initiates_wrongnumber_obls_rhs_1(self):
        ial = self.IAL_PRELUDE + \
            "in_three(A, B) initiates obl(in_two(A, C), deadline_2(A, D));"
        runner = InstalSingleShotTestRunnerFromText(input_files=[ial], bridge_file=None,
                                                    domain_files=["normparserargs/domain.idc"], fact_files=[])

        with self.assertRaises(InstalParserError):
            runner.run_test(query_file="normparserargs/blank.iaq", verbose=self.verbose,
                            conditions=[])

    def test_initiates_wrongnumber_obl_rhs_internal_1(self):
        ial = self.IAL_PRELUDE + \
            "in_three(A, B, C) initiates obl(in_two(A), deadline_2(A, D), viol_2(D, C));"
        runner = InstalSingleShotTestRunnerFromText(input_files=[ial], bridge_file=None,
                                                    domain_files=["normparserargs/domain.idc"], fact_files=[])

        with self.assertRaises(InstalParserArgumentError):
            runner.run_test(query_file="normparserargs/blank.iaq", verbose=self.verbose,
                            conditions=[])

    def test_initiates_wrongnumber_obl_rhs_internal_2(self):
        ial = self.IAL_PRELUDE + \
            "in_three(A, B, C) initiates obl(in_two(A, B), deadline_2(A), viol_2(D, C));"
        runner = InstalSingleShotTestRunnerFromText(input_files=[ial], bridge_file=None,
                                                    domain_files=["normparserargs/domain.idc"], fact_files=[])

        with self.assertRaises(InstalParserArgumentError):
            runner.run_test(query_file="normparserargs/blank.iaq", verbose=self.verbose,
                            conditions=[])

    def test_initiates_wrongnumber_obl_rhs_internal_3(self):
        ial = self.IAL_PRELUDE + \
            "in_three(A, B, C) initiates obl(in_two(A, B), deadline_2(A, D), viol_2(D));"
        runner = InstalSingleShotTestRunnerFromText(input_files=[ial], bridge_file=None,
                                                    domain_files=["normparserargs/domain.idc"], fact_files=[])

        with self.assertRaises(InstalParserArgumentError):
            runner.run_test(query_file="normparserargs/blank.iaq", verbose=self.verbose,
                            conditions=[])

    def test_initiates_obls_internal_collision(self):
        ial = self.IAL_PRELUDE + \
            "in_three(A, B, C) initiates obl(in_two(A, C), deadline_2(A, D), viol_2(D, C));"
        runner = InstalSingleShotTestRunnerFromText(input_files=[ial], bridge_file=None,
                                                    domain_files=["normparserargs/domain.idc"], fact_files=[])

        with self.assertRaises(InstalParserArgumentError):
            runner.run_test(query_file="normparserargs/blank.iaq", verbose=self.verbose,
                            conditions=[])

    def test_initiates_obls_across_collision(self):
        ial = self.IAL_PRELUDE + \
            "in_three(A, B, C) initiates obl(in_two(A, D), deadline_2(C, A), viol_2(D, B));"
        runner = InstalSingleShotTestRunnerFromText(input_files=[ial], bridge_file=None,
                                                    domain_files=["normparserargs/domain.idc"], fact_files=[])

        with self.assertRaises(InstalParserArgumentError):
            runner.run_test(query_file="normparserargs/blank.iaq", verbose=self.verbose,
                            conditions=[])

    def test_initiates_obls_across_lhs_collision(self):
        ial = self.IAL_PRELUDE + \
            "in_three(A, B, C) initiates obl(in_two(A, C), deadline_2(A, C), viol_2(D, C)), obl(in_two(A, C), deadline_2(A, C), viol_2(D, B));"
        runner = InstalSingleShotTestRunnerFromText(input_files=[ial], bridge_file=None,
                                                    domain_files=["normparserargs/domain.idc"], fact_files=[])

        with self.assertRaises(InstalParserArgumentError):
            runner.run_test(query_file="normparserargs/blank.iaq", verbose=self.verbose,
                            conditions=[])

    def test_terminates_obls_okay(self):
        ial = self.IAL_PRELUDE + \
            "in_three(A, B, C) terminates obl(in_two(A, C), deadline_2(A, C), viol_2(B, C));"
        runner = InstalSingleShotTestRunnerFromText(input_files=[ial], bridge_file=None,
                                                    domain_files=["normparserargs/domain.idc"], fact_files=[])

        runner.run_test(query_file="normparserargs/blank.iaq", verbose=self.verbose,
                        conditions=[])

    def test_terminates_obls_internal_collision(self):
        ial = self.IAL_PRELUDE + \
            "in_three(A, B, C) terminates obl(in_two(A, C), deadline_2(A, D), viol_2(D, C));"
        runner = InstalSingleShotTestRunnerFromText(input_files=[ial], bridge_file=None,
                                                    domain_files=["normparserargs/domain.idc"], fact_files=[])

        with self.assertRaises(InstalParserArgumentError):
            runner.run_test(query_file="normparserargs/blank.iaq", verbose=self.verbose,
                            conditions=[])

    def test_terminates_obls_across_collision(self):
        ial = self.IAL_PRELUDE + \
            "in_three(A, B, C) terminates obl(in_two(A, D), deadline_2(C, A), viol_2(D, B));"
        runner = InstalSingleShotTestRunnerFromText(input_files=[ial], bridge_file=None,
                                                    domain_files=["normparserargs/domain.idc"], fact_files=[])

        with self.assertRaises(InstalParserArgumentError):
            runner.run_test(query_file="normparserargs/blank.iaq", verbose=self.verbose,
                            conditions=[])

    def test_terminates_obls_across_lhs_collision(self):
        ial = self.IAL_PRELUDE + \
            "in_three(A, B, C) terminates obl(in_two(A, C), deadline_2(A, C), viol_2(D, C)), obl(in_two(A, C), deadline_2(A, C), viol_2(D, B));"
        runner = InstalSingleShotTestRunnerFromText(input_files=[ial], bridge_file=None,
                                                    domain_files=["normparserargs/domain.idc"], fact_files=[])

        with self.assertRaises(InstalParserArgumentError):
            runner.run_test(query_file="normparserargs/blank.iaq", verbose=self.verbose,
                            conditions=[])

    def test_when_obls_okay(self):
        ial = self.IAL_PRELUDE + \
            "ni_three(A, B, C) when obl(in_two(A, C), deadline_2(A, C), viol_2(B, C));"
        runner = InstalSingleShotTestRunnerFromText(input_files=[ial], bridge_file=None,
                                                    domain_files=["normparserargs/domain.idc"], fact_files=[])

        runner.run_test(query_file="normparserargs/blank.iaq", verbose=self.verbose,
                        conditions=[])

    def test_when_obls_internal_collision(self):
        ial = self.IAL_PRELUDE + \
            "ni_three(A, B, C) when obl(in_two(A, C), deadline_2(A, D), viol_2(D, C));"
        runner = InstalSingleShotTestRunnerFromText(input_files=[ial], bridge_file=None,
                                                    domain_files=["normparserargs/domain.idc"], fact_files=[])

        with self.assertRaises(InstalParserArgumentError):
            runner.run_test(query_file="normparserargs/blank.iaq", verbose=self.verbose,
                            conditions=[])

    def test_when_obls_across_collision(self):
        ial = self.IAL_PRELUDE + \
            "ni_three(A, B, C) when obl(in_two(A, D), deadline_2(C, A), viol_2(D, B));"
        runner = InstalSingleShotTestRunnerFromText(input_files=[ial], bridge_file=None,
                                                    domain_files=["normparserargs/domain.idc"], fact_files=[])

        with self.assertRaises(InstalParserArgumentError):
            runner.run_test(query_file="normparserargs/blank.iaq", verbose=self.verbose,
                            conditions=[])

    def test_when_obls_across_lhs_collision(self):
        ial = self.IAL_PRELUDE + \
            "ni_three(A, B, C) when obl(in_two(A, C), deadline_2(A, C), viol_2(D, C)), obl(in_two(A, C), deadline_2(A, C), viol_2(D, B));"
        runner = InstalSingleShotTestRunnerFromText(input_files=[ial], bridge_file=None,
                                                    domain_files=["normparserargs/domain.idc"], fact_files=[])

        with self.assertRaises(InstalParserArgumentError):
            runner.run_test(query_file="normparserargs/blank.iaq", verbose=self.verbose,
                            conditions=[])
