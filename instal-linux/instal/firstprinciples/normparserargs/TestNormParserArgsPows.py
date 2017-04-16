from instal.firstprinciples.TestEngine import InstalSingleShotTestRunnerFromText, InstalTestCase
from instal.instalexceptions import InstalParserArgumentError


class TestNormParserArgsPows(InstalTestCase):
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

    def test_initiates_pows_okay(self):
        ial = self.IAL_PRELUDE + \
            "in_three(A, B, C) initiates pow(in_two(A, C)), pow(in_two(A, C));"
        runner = InstalSingleShotTestRunnerFromText(input_files=[ial], bridge_file=None,
                                                    domain_files=["normparserargs/domain.idc"], fact_files=[])

        runner.run_test(query_file="normparserargs/blank.iaq", verbose=self.verbose,
                        conditions=[])

    def test_initiates_pows_wrongnumber_args_lhs(self):
        ial = self.IAL_PRELUDE + \
            "in_three(A, C) initiates pow(in_two(A, C)), pow(in_two(A, C));"
        runner = InstalSingleShotTestRunnerFromText(input_files=[ial], bridge_file=None,
                                                    domain_files=["normparserargs/domain.idc"], fact_files=[])

        with self.assertRaises(InstalParserArgumentError):
            runner.run_test(query_file="normparserargs/blank.iaq", verbose=self.verbose,
                            conditions=[])

    def test_initiates_pows_wrongnumber_args_rhs_1(self):
        ial = self.IAL_PRELUDE + \
            "in_three(A, B, C) initiates pow(in_two(A)), pow(in_two(A, C));"
        runner = InstalSingleShotTestRunnerFromText(input_files=[ial], bridge_file=None,
                                                    domain_files=["normparserargs/domain.idc"], fact_files=[])

        with self.assertRaises(InstalParserArgumentError):
            runner.run_test(query_file="normparserargs/blank.iaq", verbose=self.verbose,
                            conditions=[])

    def test_initiates_pows_wrongnumber_args_rhs_2(self):
        ial = self.IAL_PRELUDE + \
            "in_three(A, B, C) initiates pow(in_two(A, C)), pow(in_two(A));"
        runner = InstalSingleShotTestRunnerFromText(input_files=[ial], bridge_file=None,
                                                    domain_files=["normparserargs/domain.idc"], fact_files=[])

        with self.assertRaises(InstalParserArgumentError):
            runner.run_test(query_file="normparserargs/blank.iaq", verbose=self.verbose,
                            conditions=[])

    def test_initiates_pows_lhs_collide(self):
        ial = self.IAL_PRELUDE + \
            "in_three(A, B, C) initiates pow(in_two(A, B)), pow(in_two(A, B));"
        runner = InstalSingleShotTestRunnerFromText(input_files=[ial], bridge_file=None,
                                                    domain_files=["normparserargs/domain.idc"], fact_files=[])

        with self.assertRaises(InstalParserArgumentError):
            runner.run_test(query_file="normparserargs/blank.iaq", verbose=self.verbose,
                            conditions=[])

    def test_initiates_pows_collision_oneterm_lhs(self):
        ial = self.IAL_PRELUDE + \
            "in_three(A, A, A) initiates pow(in_two(C, D)), pow(in_two(E, B));"
        runner = InstalSingleShotTestRunnerFromText(input_files=[ial], bridge_file=None,
                                                    domain_files=["normparserargs/domain.idc"], fact_files=[])

        with self.assertRaises(InstalParserArgumentError):
            runner.run_test(query_file="normparserargs/blank.iaq", verbose=self.verbose,
                            conditions=[])

    def test_initiates_pows_collision_oneterm_rhs(self):
        ial = self.IAL_PRELUDE + \
            "in_three(A, B, C) initiates pow(in_two(A, A)), pow(in_two(E, B));"
        runner = InstalSingleShotTestRunnerFromText(input_files=[ial], bridge_file=None,
                                                    domain_files=["normparserargs/domain.idc"], fact_files=[])

        with self.assertRaises(InstalParserArgumentError):
            runner.run_test(query_file="normparserargs/blank.iaq", verbose=self.verbose,
                            conditions=[])

    def test_initiates_pows_collision_twoterms(self):
        ial = self.IAL_PRELUDE + \
            "in_three(A, B, C) initiates pow(in_two(A, B)), pow(in_two(B, A));"
        runner = InstalSingleShotTestRunnerFromText(input_files=[ial], bridge_file=None,
                                                    domain_files=["normparserargs/domain.idc"], fact_files=[])

        with self.assertRaises(InstalParserArgumentError):
            runner.run_test(query_file="normparserargs/blank.iaq", verbose=self.verbose,
                            conditions=[])

    def test_initiates_pows_collision_threeterms(self):
        ial = self.IAL_PRELUDE + \
            "in_three(A, B, C) initiates pow(in_two(C, A)), pow(in_two(B, A));"
        runner = InstalSingleShotTestRunnerFromText(input_files=[ial], bridge_file=None,
                                                    domain_files=["normparserargs/domain.idc"], fact_files=[])

        with self.assertRaises(InstalParserArgumentError):
            runner.run_test(query_file="normparserargs/blank.iaq", verbose=self.verbose,
                            conditions=[])

    def test_terminates_pows_okay(self):
        ial = self.IAL_PRELUDE + \
            "in_three(A, B, C) terminates pow(in_two(A, C)), pow(in_two(A, C));"
        runner = InstalSingleShotTestRunnerFromText(input_files=[ial], bridge_file=None,
                                                    domain_files=["normparserargs/domain.idc"], fact_files=[])

        runner.run_test(query_file="normparserargs/blank.iaq", verbose=self.verbose,
                        conditions=[])

    def test_terminates_pows_lhs_collide(self):
        ial = self.IAL_PRELUDE + \
            "in_three(A, B, C) terminates pow(in_two(A, B)), pow(in_two(A, B));"
        runner = InstalSingleShotTestRunnerFromText(input_files=[ial], bridge_file=None,
                                                    domain_files=["normparserargs/domain.idc"], fact_files=[])

        with self.assertRaises(InstalParserArgumentError):
            runner.run_test(query_file="normparserargs/blank.iaq", verbose=self.verbose,
                            conditions=[])

    def test_terminates_pows_collision_oneterm_lhs(self):
        ial = self.IAL_PRELUDE + \
            "in_three(A, A, A) terminates pow(in_two(C, D)), pow(in_two(E, B));"
        runner = InstalSingleShotTestRunnerFromText(input_files=[ial], bridge_file=None,
                                                    domain_files=["normparserargs/domain.idc"], fact_files=[])

        with self.assertRaises(InstalParserArgumentError):
            runner.run_test(query_file="normparserargs/blank.iaq", verbose=self.verbose,
                            conditions=[])

    def test_terminates_pows_collision_oneterm_rhs(self):
        ial = self.IAL_PRELUDE + \
            "in_three(A, B, C) initiates pow(in_two(A, A)), pow(in_two(E, B));"
        runner = InstalSingleShotTestRunnerFromText(input_files=[ial], bridge_file=None,
                                                    domain_files=["normparserargs/domain.idc"], fact_files=[])

        with self.assertRaises(InstalParserArgumentError):
            runner.run_test(query_file="normparserargs/blank.iaq", verbose=self.verbose,
                            conditions=[])

    def test_terminates_pows_collision_twoterms(self):
        ial = self.IAL_PRELUDE + \
            "in_three(A, B, C) initiates pow(in_two(A, B)), pow(in_two(B, A));"
        runner = InstalSingleShotTestRunnerFromText(input_files=[ial], bridge_file=None,
                                                    domain_files=["normparserargs/domain.idc"], fact_files=[])

        with self.assertRaises(InstalParserArgumentError):
            runner.run_test(query_file="normparserargs/blank.iaq", verbose=self.verbose,
                            conditions=[])

    def test_terminates_pows_collision_threeterms(self):
        ial = self.IAL_PRELUDE + \
            "in_three(A, B, C) initiates pow(in_two(C, A)), pow(in_two(B, A));"
        runner = InstalSingleShotTestRunnerFromText(input_files=[ial], bridge_file=None,
                                                    domain_files=["normparserargs/domain.idc"], fact_files=[])

        with self.assertRaises(InstalParserArgumentError):
            runner.run_test(query_file="normparserargs/blank.iaq", verbose=self.verbose,
                            conditions=[])

    def test_when_pows_okay(self):
        ial = self.IAL_PRELUDE + \
            "ni_three(A, B, C) when flu_two(A, C), flu_two(A, C);"
        runner = InstalSingleShotTestRunnerFromText(input_files=[ial], bridge_file=None,
                                                    domain_files=["normparserargs/domain.idc"], fact_files=[])

        runner.run_test(query_file="normparserargs/blank.iaq", verbose=self.verbose,
                        conditions=[])

    def test_when_pows_lhs_collide(self):
        ial = self.IAL_PRELUDE + \
            "ni_three(A, B, C) when pow(in_two(A, B)), pow(in_two(A, B));"
        runner = InstalSingleShotTestRunnerFromText(input_files=[ial], bridge_file=None,
                                                    domain_files=["normparserargs/domain.idc"], fact_files=[])

        with self.assertRaises(InstalParserArgumentError):
            runner.run_test(query_file="normparserargs/blank.iaq", verbose=self.verbose,
                            conditions=[])

    def test_when_pows_collision_oneterm_lhs(self):
        ial = self.IAL_PRELUDE + \
            "ni_three(A, A, A) when pow(in_two(C, D)), pow(in_two(E, B));"
        runner = InstalSingleShotTestRunnerFromText(input_files=[ial], bridge_file=None,
                                                    domain_files=["normparserargs/domain.idc"], fact_files=[])

        with self.assertRaises(InstalParserArgumentError):
            runner.run_test(query_file="normparserargs/blank.iaq", verbose=self.verbose,
                            conditions=[])

    def test_when_pows_collision_oneterm_rhs(self):
        ial = self.IAL_PRELUDE + \
            "ni_three(A, B, C) when pow(in_two(A, A)), pow(in_two(E, B));"
        runner = InstalSingleShotTestRunnerFromText(input_files=[ial], bridge_file=None,
                                                    domain_files=["normparserargs/domain.idc"], fact_files=[])

        with self.assertRaises(InstalParserArgumentError):
            runner.run_test(query_file="normparserargs/blank.iaq", verbose=self.verbose,
                            conditions=[])

    def test_when_pows_collision_twoterms(self):
        ial = self.IAL_PRELUDE + \
            "ni_three(A, B, C) when pow(in_two(A, B)), pow(in_two(B, A));"
        runner = InstalSingleShotTestRunnerFromText(input_files=[ial], bridge_file=None,
                                                    domain_files=["normparserargs/domain.idc"], fact_files=[])

        with self.assertRaises(InstalParserArgumentError):
            runner.run_test(query_file="normparserargs/blank.iaq", verbose=self.verbose,
                            conditions=[])

    def test_when_pows_collision_threeterms(self):
        ial = self.IAL_PRELUDE + \
            "ni_three(A, B, C) when pow(in_two(C, A)), pow(in_two(B, A));"
        runner = InstalSingleShotTestRunnerFromText(input_files=[ial], bridge_file=None,
                                                    domain_files=["normparserargs/domain.idc"], fact_files=[])

        with self.assertRaises(InstalParserArgumentError):
            runner.run_test(query_file="normparserargs/blank.iaq", verbose=self.verbose,
                            conditions=[])
