from instal.firstprinciples.TestEngine import InstalMultiShotTestRunner, InstalTestCase, InstalCompareQuerySolve
from instal.instalutility import temporary_text_file
from instal import instalquery, instaltrace, instalsolve


class MultiShotEngine(InstalTestCase):

    def test_onelength_onetype(self):
        """Taken from querytest/TestBasicQuery"""
        runner = InstalMultiShotTestRunner(input_files=["querytest/basicquery.ial"],
                                           domain_files=["querytest/foo-a.idc"])

        runner.run_test(
            verbose=self.verbose, expected_answersets=2)

    def test_onelength_onetype_fail(self):
        """Modified from from querytest/TestBasicQuery"""
        runner = InstalMultiShotTestRunner(input_files=["querytest/basicquery.ial"],
                                           domain_files=["querytest/foo-a.idc"])

        with self.assertRaises(AssertionError):
            runner.run_test(
                verbose=self.verbose, expected_answersets=3)
