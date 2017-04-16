from instal.firstprinciples.TestEngine import InstalSingleShotTestRunner, InstalTestCase
from instal.instalexceptions import InstalParserError


class SingleShotEngine(InstalTestCase):

    def test_generate_institutional(self):
        """Taken from generates/TestGenerateNormsEvents.py"""
        runner = InstalSingleShotTestRunner(input_files=["generates/generate_institutional.ial"], bridge_file=None,
                                            domain_files=[
                                                "generates/blank.idc"],
                                            fact_files=["generates/perm-exlhs.iaf", "generates/perm-inrhs.iaf",
                                                        "generates/pow-inrhs.iaf"])

        condition = [
            {"occurred": ["occurred(ex_lhs, generate)", "occurred(in_rhs, generate)"],
             "notoccurred": ["occurred(viol(ex_lhs),generate)", "occurred(viol(in_rhs),generate)"]}
        ]

        runner.run_test(query_file="generates/generates-exlhs.iaq",
                        verbose=self.verbose,
                        conditions=condition)

    def test_generate_institutional_fail(self):
        """Modified from from generates/TestGenerateNormsEvents.py"""
        runner = InstalSingleShotTestRunner(input_files=["generates/generate_institutional.ial"], bridge_file=None,
                                            domain_files=[
                                                "generates/blank.idc"],
                                            fact_files=["generates/perm-exlhs.iaf", "generates/perm-inrhs.iaf",
                                                        "generates/pow-inrhs.iaf"])

        condition = [
            {"notoccurred": ["occurred(ex_lhs, generate)", "occurred(in_rhs, generate)"],
             "occurred": ["occurred(viol(ex_lhs),generate)", "occurred(viol(in_rhs),generate)"]}
        ]
        with self.assertRaises(AssertionError):
            runner.run_test(query_file="generates/generates-exlhs.iaq",
                            verbose=self.verbose,
                            conditions=condition)
