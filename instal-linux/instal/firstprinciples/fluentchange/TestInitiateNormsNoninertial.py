from instal.firstprinciples.TestEngine import InstalSingleShotTestRunner, InstalTestCase
from instal.instalexceptions import InstalParserError


class InitiateNormsPerms(InstalTestCase):

    def test_initiate_noninertial(self):
        runner = InstalSingleShotTestRunner(input_files=["fluentchange/noninertialinitiates.ial"], bridge_file=None,
                                            domain_files=[
                                                "fluentchange/fluentchange.idc"],
                                            fact_files=["fluentchange/fluentinitiates_permissions.iaf"])

        with self.assertRaises(InstalParserError):
            runner.run_test(
                query_file="fluentchange/one_in_no.iaq", verbose=self.verbose)

    def test_initiate_multiple_all_noninertial(self):
        runner = InstalSingleShotTestRunner(input_files=["fluentchange/noninertialinitiates_multipleall.ial"],
                                            bridge_file=None, domain_files=["fluentchange/fluentchange.idc"],
                                            fact_files=["fluentchange/fluentinitiates_permissions.iaf"])

        with self.assertRaises(InstalParserError):
            runner.run_test(
                query_file="fluentchange/one_in_no.iaq", verbose=self.verbose)

    def test_initiate_multiple_one_noninertial(self):
        runner = InstalSingleShotTestRunner(input_files=["fluentchange/noninertialinitiates_multipleone.ial"],
                                            bridge_file=None, domain_files=["fluentchange/fluentchange.idc"],
                                            fact_files=["fluentchange/fluentinitiates_permissions.iaf"])

        with self.assertRaises(InstalParserError):
            runner.run_test(
                query_file="fluentchange/one_in_no.iaq", verbose=self.verbose)

    def test_initiate_noninertial_condition(self):
        runner = InstalSingleShotTestRunner(input_files=["fluentchange/noninertialinitiates_condition.ial"],
                                            bridge_file=None, domain_files=["fluentchange/fluentchange.idc"],
                                            fact_files=["fluentchange/fluentinitiates_permissions.iaf",
                                                        "fluentchange/fluentterminates_facts.iaf"])

        with self.assertRaises(InstalParserError):
            runner.run_test(
                query_file="fluentchange/one_in_no.iaq", verbose=self.verbose)
