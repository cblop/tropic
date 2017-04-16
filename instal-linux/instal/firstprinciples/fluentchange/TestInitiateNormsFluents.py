from instal.firstprinciples.TestEngine import InstalSingleShotTestRunner, InstalTestCase
from instal.instalexceptions import InstalParserError


class InitiateNormsFluents(InstalTestCase):

    def test_initiate_fluent_institutional_onearg(self):
        runner = InstalSingleShotTestRunner(input_files=["fluentchange/fluentinitiates.ial"], bridge_file=None,
                                            domain_files=[
                                                "fluentchange/fluentchange.idc"],
                                            fact_files=["fluentchange/fluentinitiates_permissions.iaf"])

        in_a_true_condition = [
            {"holdsat": ["holdsat(flu_onearg(foo),fluentchange)"]}]

        self.assertEqual(runner.run_test(query_file="fluentchange/one_in_a.iaq", verbose=self.verbose,
                                         conditions=in_a_true_condition), 0,
                         "A fluent with one arg initiated by an inst event.")

    def test_initiate_fluent_institutional_twoargs(self):
        runner = InstalSingleShotTestRunner(input_files=["fluentchange/fluentinitiates.ial"], bridge_file=None,
                                            domain_files=[
                                                "fluentchange/fluentchange.idc"],
                                            fact_files=["fluentchange/fluentinitiates_permissions.iaf"])

        in_b_true_condition = [
            {"holdsat": ["holdsat(flu_twoargs(foo, foo),fluentchange)"]}]

        self.assertEqual(runner.run_test(query_file="fluentchange/one_in_b.iaq", verbose=self.verbose,
                                         conditions=in_b_true_condition), 0,
                         "A fluent with two args initiated by an inst event.")

    def test_initiate_fluent_institutional_noargs(self):
        runner = InstalSingleShotTestRunner(input_files=["fluentchange/fluentinitiates.ial"], bridge_file=None,
                                            domain_files=[
                                                "fluentchange/fluentchange.idc"],
                                            fact_files=["fluentchange/fluentinitiates_permissions.iaf"])

        in_no_true_condition = [{"holdsat": ["holdsat(flu_no, fluentchange)"]}]

        self.assertEqual(runner.run_test(query_file="fluentchange/one_in_no.iaq", verbose=self.verbose,
                                         conditions=in_no_true_condition), 0,
                         "A fluent with no args initiated by an inst event.")

    def test_initiate_fluent_exogenous_onearg(self):
        runner = InstalSingleShotTestRunner(input_files=["fluentchange/fluentinitiates_exogenous.ial"],
                                            bridge_file=None, domain_files=["fluentchange/fluentchange.idc"],
                                            fact_files=["fluentchange/fluentinitiates_permissions.iaf"])

        with self.assertRaises(InstalParserError):
            runner.run_test(query_file="fluentchange/one_in_a.iaq",
                            verbose=self.verbose, conditions=[])

    def test_initiate_multiple_fluent(self):
        runner = InstalSingleShotTestRunner(input_files=["fluentchange/fluentinitiates.ial"],
                                            bridge_file=None, domain_files=["fluentchange/fluentchange.idc"],
                                            fact_files=["fluentchange/multiple-permissions.iaf"])

        condition = [{"holdsat": [
            "holdsat(flu_multiple1, fluentchange)", "holdsat(flu_multiple2, fluentchange)"]}]

        self.assertEqual(runner.run_test(query_file="fluentchange/ex_multiple.iaq", verbose=self.verbose,
                                         conditions=condition), 0, "Multiple fluents initiated from one event.")

    def test_initiate_fluent_condition_true(self):
        runner = InstalSingleShotTestRunner(input_files=["fluentchange/fluentinitiates.ial"],
                                            bridge_file=None, domain_files=["fluentchange/fluentchange.idc"],
                                            fact_files=["fluentchange/conditional-permissions.iaf",
                                                        "fluentchange/condition-conditional.iaf"])

        condition = [{"holdsat": ["holdsat(flu_conditional, fluentchange)"]}]

        self.assertEqual(runner.run_test(query_file="fluentchange/ex_conditional.iaq", verbose=self.verbose,
                                         conditions=condition), 0,
                         "Initiates statement happens when conditional is true.")

    def test_initiate_fluent_condition_false(self):
        runner = InstalSingleShotTestRunner(input_files=["fluentchange/fluentinitiates.ial"],
                                            bridge_file=None, domain_files=["fluentchange/fluentchange.idc"],
                                            fact_files=["fluentchange/conditional-permissions.iaf"])

        condition = [
            {"notholdsat": ["holdsat(flu_conditional, fluentchange)"]}]

        self.assertEqual(runner.run_test(query_file="fluentchange/ex_conditional.iaq", verbose=self.verbose,
                                         conditions=condition), 0,
                         "Initiates statement doesn't happen when conditional is false")

    def test_initiate_fluent_institutional_violation(self):
        runner = InstalSingleShotTestRunner(input_files=["fluentchange/fluentinitiates.ial"], bridge_file=None,
                                            domain_files=[
                                                "fluentchange/fluentchange.idc"],
                                            fact_files=["fluentchange/fluentinitiates_permissions_violation.iaf"])

        in_a_true_condition = [
            {"notholdsat": ["holdsat(flu_onearg(foo),fluentchange)"]}]

        self.assertEqual(runner.run_test(query_file="fluentchange/one_in_a.iaq", verbose=self.verbose,
                                         conditions=in_a_true_condition), 0,
                         "A fluent with one arg not initiated by an inst with violation.")
