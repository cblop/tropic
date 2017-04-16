from instal.firstprinciples.TestEngine import InstalSingleShotTestRunner, InstalTestCase
from instal.instalexceptions import InstalParserError


class TerminateNormsFluents(InstalTestCase):

    def test_terminate_fluents_institutional_onearg(self):
        runner = InstalSingleShotTestRunner(input_files=["fluentchange/fluentterminates.ial"], bridge_file=None,
                                            domain_files=[
                                                "fluentchange/fluentchange.idc"],
                                            fact_files=["fluentchange/fluentinitiates_permissions.iaf",
                                                        "fluentchange/fluentterminates_facts.iaf"])

        in_a_true_condition = [
            {"notholdsat": ["holdsat(flu_onearg(foo),fluentchange)"]}]

        self.assertEqual(runner.run_test(query_file="fluentchange/one_in_a.iaq", verbose=self.verbose,
                                         conditions=in_a_true_condition), 0,
                         "A fluent with one arg terminated by an inst event.")

    def test_terminate_fluents_institutional_twoargs(self):
        runner = InstalSingleShotTestRunner(input_files=["fluentchange/fluentterminates.ial"], bridge_file=None,
                                            domain_files=[
                                                "fluentchange/fluentchange.idc"],
                                            fact_files=["fluentchange/fluentinitiates_permissions.iaf",
                                                        "fluentchange/fluentterminates_facts.iaf"])

        in_b_true_condition = [
            {"notholdsat": ["holdsat(flu_twoargs(foo, foo),fluentchange)"]}]

        self.assertEqual(runner.run_test(query_file="fluentchange/one_in_b.iaq", verbose=self.verbose,
                                         conditions=in_b_true_condition), 0,
                         "A fluent with two args terminated by an inst event.")

    def test_terminate_fluents_institutional_noargs(self):
        runner = InstalSingleShotTestRunner(input_files=["fluentchange/fluentterminates.ial"], bridge_file=None,
                                            domain_files=[
                                                "fluentchange/fluentchange.idc"],
                                            fact_files=["fluentchange/fluentinitiates_permissions.iaf",
                                                        "fluentchange/fluentterminates_facts.iaf"])

        in_no_true_condition = [
            {"notholdsat": ["holdsat(flu_no, fluentchange)"]}]

        self.assertEqual(runner.run_test(query_file="fluentchange/one_in_no.iaq", verbose=self.verbose,
                                         conditions=in_no_true_condition), 0,
                         "A fluent with no args terminated by an inst event.")

    def test_terminate_fluents_exogenous(self):
        runner = InstalSingleShotTestRunner(input_files=["fluentchange/fluentterminates_exogenous.ial"],
                                            bridge_file=None, domain_files=["fluentchange/fluentchange.idc"],
                                            fact_files=["fluentchange/fluentinitiates_permissions.iaf",
                                                        "fluentchange/fluentterminates_facts.iaf"])

        with self.assertRaises(InstalParserError):
            runner.run_test(query_file="fluentchange/one_in_a.iaq",
                            verbose=self.verbose, conditions=[])

    def test_terminate_multiple_fluent(self):
        runner = InstalSingleShotTestRunner(input_files=["fluentchange/fluentterminates.ial"],
                                            bridge_file=None, domain_files=["fluentchange/fluentchange.idc"],
                                            fact_files=["fluentchange/multiple-permissions.iaf",
                                                        "fluentchange/terminates-multiple.iaf"])

        condition = [{"holdsat": ["holdsat(flu_multiple1, fluentchange)", "holdsat(flu_multiple2, fluentchange)"]},
                     {"notholdsat": ["holdsat(flu_multiple1, fluentchange)", "holdsat(flu_multiple2, fluentchange)"]}]

        self.assertEqual(runner.run_test(query_file="fluentchange/ex_multiple.iaq", verbose=self.verbose,
                                         conditions=condition), 0, "Multiple fluents terminated from one event.")

    def test_terminate_fluent_condition_true(self):
        runner = InstalSingleShotTestRunner(input_files=["fluentchange/fluentterminates.ial"],
                                            bridge_file=None, domain_files=["fluentchange/fluentchange.idc"],
                                            fact_files=["fluentchange/conditional-permissions.iaf",
                                                        "fluentchange/condition-conditional.iaf",
                                                        "fluentchange/condition-condition.iaf"])

        condition = [{"holdsat": ["holdsat(flu_conditional, fluentchange)", "holdsat(flu_condition, fluentchange)"]},
                     {"notholdsat": ["holdsat(flu_conditional, fluentchange)"],
                      "holdsat": ["holdsat(flu_condition, fluentchange)"]}]

        self.assertEqual(runner.run_test(query_file="fluentchange/ex_conditional.iaq", verbose=self.verbose,
                                         conditions=condition), 0, "Multiple fluents terminated from one event.")

    def test_terminate_fluent_condition_false(self):
        runner = InstalSingleShotTestRunner(input_files=["fluentchange/fluentterminates.ial"],
                                            bridge_file=None, domain_files=["fluentchange/fluentchange.idc"],
                                            fact_files=["fluentchange/conditional-permissions.iaf",
                                                        "fluentchange/condition-condition.iaf"])

        condition = [{"holdsat": ["holdsat(flu_conditional, fluentchange)"],
                      "notholdsat": ["holdsat(flu_condition, fluentchange)"]},
                     {"holdsat": ["holdsat(flu_conditional, fluentchange)"],
                      "notholdsat": ["holdsat(flu_condition, fluentchange)"]}]

        self.assertEqual(runner.run_test(query_file="fluentchange/ex_conditional.iaq", verbose=self.verbose,
                                         conditions=condition), 0, "Multiple fluents terminated from one event.")

    def test_terminate_fluents_institutional_violation(self):
        runner = InstalSingleShotTestRunner(input_files=["fluentchange/fluentterminates.ial"], bridge_file=None,
                                            domain_files=[
                                                "fluentchange/fluentchange.idc"],
                                            fact_files=["fluentchange/fluentinitiates_permissions_violation.iaf",
                                                        "fluentchange/fluentterminates_facts.iaf"])

        in_a_true_condition = [
            {"holdsat": ["holdsat(flu_onearg(foo),fluentchange)"]}]

        self.assertEqual(runner.run_test(query_file="fluentchange/one_in_a.iaq", verbose=self.verbose,
                                         conditions=in_a_true_condition), 0,
                         "A fluent with one arg terminated by an inst event.")
