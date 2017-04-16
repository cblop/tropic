from instal.firstprinciples.TestEngine import InstalSingleShotTestRunner, InstalTestCase
from instal.instalexceptions import InstalParserError


class TerminateNormsNoninertial(InstalTestCase):

    def test_terminate_noninertial(self):
        runner = InstalSingleShotTestRunner(input_files=["fluentchange/noninertialterminates.ial"], bridge_file=None,
                                            domain_files=[
                                                "fluentchange/fluentchange.idc"],
                                            fact_files=["fluentchange/fluentinitiates_permissions.iaf",
                                                        "fluentchange/fluentterminates_facts.iaf"])

        with self.assertRaises(InstalParserError):
            runner.run_test(
                query_file="fluentchange/one_in_no.iaq", verbose=self.verbose)

    def test_terminate_multiple_all_noninertial(self):
        runner = InstalSingleShotTestRunner(input_files=["fluentchange/noninertialterminates_multipleall.ial"],
                                            bridge_file=None, domain_files=["fluentchange/fluentchange.idc"],
                                            fact_files=["fluentchange/fluentinitiates_permissions.iaf",
                                                        "fluentchange/fluentterminates_facts.iaf"])

        with self.assertRaises(InstalParserError):
            runner.run_test(
                query_file="fluentchange/one_in_no.iaq", verbose=self.verbose)

    def test_terminate_multiple_one_noninertial(self):
        runner = InstalSingleShotTestRunner(input_files=["fluentchange/noninertialterminates_multipleone.ial"],
                                            bridge_file=None, domain_files=["fluentchange/fluentchange.idc"],
                                            fact_files=["fluentchange/fluentinitiates_permissions.iaf",
                                                        "fluentchange/fluentterminates_facts.iaf"])

        with self.assertRaises(InstalParserError):
            runner.run_test(
                query_file="fluentchange/one_in_no.iaq", verbose=self.verbose)

    def test_terminate_noninertial_condition(self):
        runner = InstalSingleShotTestRunner(input_files=["fluentchange/noninertialterminates_condition.ial"],
                                            bridge_file=None, domain_files=["fluentchange/fluentchange.idc"],
                                            fact_files=["fluentchange/fluentinitiates_permissions.iaf",
                                                        "fluentchange/fluentterminates_facts.iaf"])

        with self.assertRaises(InstalParserError):
            runner.run_test(
                query_file="fluentchange/one_in_no.iaq", verbose=self.verbose)
