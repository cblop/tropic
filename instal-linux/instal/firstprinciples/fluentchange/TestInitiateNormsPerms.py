from instal.firstprinciples.TestEngine import InstalSingleShotTestRunner, InstalTestCase
from instal.instalexceptions import InstalParserError


class InitiateNormsPerms(InstalTestCase):

    def test_initiate_perms_institutional(self):
        runner = InstalSingleShotTestRunner(input_files=["fluentchange/perminitiates.ial"], bridge_file=None,
                                            domain_files=[
                                                "fluentchange/fluentchange.idc"],
                                            fact_files=["fluentchange/fluentinitiates_permissions.iaf"])

        in_a_true_condition = [
            {"holdsat": ["holdsat(perm(ex_a(foo)),fluentchange)"]}]

        self.assertEqual(runner.run_test(query_file="fluentchange/one_in_a.iaq", verbose=self.verbose,
                                         conditions=in_a_true_condition), 0,
                         "A permission initiated by an institutional event")

    def test_initiate_perms_exogenous(self):
        runner = InstalSingleShotTestRunner(input_files=["fluentchange/perminitiates_exogenous.ial"], bridge_file=None,
                                            domain_files=[
                                                "fluentchange/fluentchange.idc"],
                                            fact_files=["fluentchange/fluentinitiates_permissions.iaf"])

        with self.assertRaises(InstalParserError):
            runner.run_test(query_file="fluentchange/one_in_a.iaq",
                            verbose=self.verbose, conditions=[])
