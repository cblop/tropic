from instal.firstprinciples.TestEngine import InstalSingleShotTestRunner, InstalTestCase


class GenerateNormsPerms(InstalTestCase):

    def test_generate_with_nonpermitted_event(self):
        runner = InstalSingleShotTestRunner(input_files=["generates/generate_institutional.ial"], bridge_file=None,
                                            domain_files=[
                                                "generates/blank.idc"],
                                            fact_files=["generates/perm-inrhs.iaf", "generates/pow-inrhs.iaf"])

        condition = [
            {"occurred": ["occurred(ex_lhs, generate)", "occurred(viol(ex_lhs), generate)"],
             "notoccurred": ["occurred(in_rhs,generate)", "occurred(viol(in_rhs,generate))"]}
        ]

        self.assertEqual(runner.run_test(query_file="generates/generates-exlhs.iaq",
                                         verbose=self.verbose,
                                         conditions=condition), 0,
                         "Exogenous events causing violations can't generate")
