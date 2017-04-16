from instal.firstprinciples.TestEngine import InstalSingleShotTestRunner, InstalTestCase
from instal.instalexceptions import InstalParserError


class TerminateNormsPows(InstalTestCase):

    def test_terminate_pows_institutional(self):
        runner = InstalSingleShotTestRunner(input_files=["fluentchange/powterminates.ial"], bridge_file=None,
                                            domain_files=[
                                                "fluentchange/fluentchange.idc"],
                                            fact_files=["fluentchange/fluentinitiates_permissions.iaf",
                                                        "fluentchange/fluentterminates_facts.iaf"])

        in_a_true_condition = [
            {"notholdsat": ["holdsat(pow(in_no),fluentchange)"]}]

        self.assertEqual(runner.run_test(query_file="fluentchange/one_in_no.iaq", verbose=self.verbose,
                                         conditions=in_a_true_condition), 0, "A power terminated by an inst event.")

    def test_terminate_pows_exogenous(self):
        runner = InstalSingleShotTestRunner(input_files=["fluentchange/powterminates_exogenous.ial"], bridge_file=None,
                                            domain_files=[
                                                "fluentchange/fluentchange.idc"],
                                            fact_files=["fluentchange/fluentinitiates_permissions.iaf",
                                                        "fluentchange/fluentterminates_facts.iaf"])

        with self.assertRaises(InstalParserError):
            runner.run_test(query_file="fluentchange/one_in_a.iaq",
                            verbose=self.verbose, conditions=[])
