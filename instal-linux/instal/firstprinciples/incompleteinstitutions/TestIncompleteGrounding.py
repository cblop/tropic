from instal.firstprinciples.TestEngine import InstalSingleShotTestRunner, InstalMultiShotTestRunner, InstalTestCase
from instal.instalexceptions import InstalRuntimeError


class IncompleteGrounding(InstalTestCase):

    def test_complete_grounding_solve(self):
        runner = InstalSingleShotTestRunner(input_files=["incompleteinstitutions/incomplete.ial"], bridge_file=None,
                                            domain_files=["incompleteinstitutions/fullgrounding.idc"], fact_files=[])

        runner.run_test(query_file="incompleteinstitutions/blank.iaq")

    def test_no_grounding_solve(self):
        runner = InstalSingleShotTestRunner(input_files=["incompleteinstitutions/incomplete.ial"], bridge_file=None,
                                            domain_files=["incompleteinstitutions/nogrounding.idc"], fact_files=[])

        with self.assertRaises(InstalRuntimeError):
            runner.run_test(query_file="incompleteinstitutions/blank.iaq")

    def test_partial_grounding_solve(self):
        runner = InstalSingleShotTestRunner(input_files=["incompleteinstitutions/incomplete.ial"], bridge_file=None,
                                            domain_files=["incompleteinstitutions/partialgrounding.idc"], fact_files=[])

        with self.assertRaises(InstalRuntimeError):
            runner.run_test(query_file="incompleteinstitutions/blank.iaq")

    def test_complete_grounding_query(self):
        runner = InstalMultiShotTestRunner(input_files=["incompleteinstitutions/incomplete.ial"], bridge_file=None,
                                           domain_files=["incompleteinstitutions/fullgrounding.idc"], fact_files=[])

        runner.run_test(
            query_file="incompleteinstitutions/blank.iaq", expected_answersets=1)

    def test_no_grounding_query(self):
        runner = InstalMultiShotTestRunner(input_files=["incompleteinstitutions/incomplete.ial"], bridge_file=None,
                                           domain_files=["incompleteinstitutions/nogrounding.idc"], fact_files=[])

        with self.assertRaises(InstalRuntimeError):
            runner.run_test(query_file="incompleteinstitutions/blank.iaq")

    def test_partial_grounding_query(self):
        runner = InstalMultiShotTestRunner(input_files=["incompleteinstitutions/incomplete.ial"], bridge_file=None,
                                           domain_files=["incompleteinstitutions/partialgrounding.idc"], fact_files=[])

        with self.assertRaises(InstalRuntimeError):
            runner.run_test(query_file="incompleteinstitutions/blank.iaq")
