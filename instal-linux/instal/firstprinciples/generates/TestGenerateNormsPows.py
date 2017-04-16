from instal.firstprinciples.TestEngine import InstalSingleShotTestRunner, InstalTestCase


class GenerateNormsPows(InstalTestCase):

    def test_generate_without_power(self):
        runner = InstalSingleShotTestRunner(input_files=["generates/generate_institutional.ial"], bridge_file=None,
                                            domain_files=[
                                                "generates/blank.idc"],
                                            fact_files=["generates/perm-inrhs.iaf", "generates/perm-exlhs.iaf"])

        condition = [
            {"occurred": ["occurred(ex_lhs, generate)"],
             "notoccurred": ["occurred(viol(ex_lhs),generate)", "occurred(in_rhs,generate)",
                             "occurred(viol(in_rhs,generate))"]}
        ]

        self.assertEqual(runner.run_test(query_file="generates/generates-exlhs.iaq",
                                         verbose=self.verbose,
                                         conditions=condition), 0, "No event generated if no power (institutional)")
