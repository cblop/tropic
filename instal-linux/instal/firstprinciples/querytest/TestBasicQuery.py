from instal.firstprinciples.TestEngine import InstalMultiShotTestRunner, InstalTestCase, InstalCompareQuerySolve
from instal.instalutility import temporary_text_file
from instal import instalquery, instaltrace, instalsolve


class BasicQuery(InstalTestCase):
    verbose = 2

    def test_onelength_onetype(self):
        runner = InstalMultiShotTestRunner(input_files=["querytest/basicquery.ial"],
                                           domain_files=["querytest/foo-a.idc"])

        self.assertEqual(runner.run_test(
            verbose=self.verbose, expected_answersets=2), 0, "Basic query test: expecting 2 events.")

    def test_onelength_twotype(self):
        runner = InstalMultiShotTestRunner(input_files=["querytest/basicquery.ial"],
                                           domain_files=["querytest/foo-a.idc",
                                                         "querytest/foo-b.idc"])

        self.assertEqual(runner.run_test(
            verbose=self.verbose, expected_answersets=3), 0, "Basic query test: expecting 3 events.")

    def test_twolength_onetype(self):
        runner = InstalMultiShotTestRunner(input_files=["querytest/basicquery.ial"],
                                           domain_files=["querytest/foo-a.idc"])

        self.assertEqual(runner.run_test(
            verbose=self.verbose, expected_answersets=4, length=2), 0, "Basic query test: expecting 4 events.")

    def test_twolength_twotype(self):
        runner = InstalMultiShotTestRunner(input_files=["querytest/basicquery.ial"],
                                           domain_files=["querytest/foo-a.idc",
                                                         "querytest/foo-b.idc"])

        self.assertEqual(runner.run_test(
            verbose=self.verbose, expected_answersets=9, length=2), 0, "Basic query test: expecting 9 events.")

    def test_onelength_query(self):
        runner = InstalMultiShotTestRunner(input_files=["querytest/basicquery.ial"],
                                           domain_files=["querytest/foo-a.idc"])

        self.assertEqual(runner.run_test(
            verbose=self.verbose, query_file="querytest/ex_a_1.iaq", expected_answersets=1, length=1), 0,
            "Query test with query file: 1 event.")

    def test_twolength_query(self):
        runner = InstalMultiShotTestRunner(input_files=["querytest/basicquery.ial"],
                                           domain_files=["querytest/foo-a.idc", "querytest/foo-b.idc"])

        self.assertEqual(runner.run_test(
            verbose=self.verbose, query_file="querytest/ex_a_b_2.iaq", expected_answersets=1, length=2), 0,
            "Query test with query file: 2 events.")

    def test_twolength_onequery(self):
        runner = InstalMultiShotTestRunner(input_files=["querytest/basicquery.ial"],
                                           domain_files=["querytest/foo-a.idc", "querytest/foo-b.idc"])

        self.assertEqual(runner.run_test(
            verbose=self.verbose, query_file="querytest/ex_a_1.iaq", expected_answersets=3, length=2), 0,
            "Query test with query file: 2 events.")

    def test_threelength_twoquery(self):
        runner = InstalMultiShotTestRunner(input_files=["querytest/basicquery.ial"],
                                           domain_files=["querytest/foo-a.idc", "querytest/foo-b.idc"])

        self.assertEqual(runner.run_test(
            verbose=self.verbose, query_file="querytest/ex_a_b_2.iaq", expected_answersets=3, length=3), 0,
            "Query test with query file: 2 events.")

    def test_fivelength_twoquery(self):
        runner = InstalMultiShotTestRunner(input_files=["querytest/basicquery.ial"],
                                           domain_files=["querytest/foo-a.idc", "querytest/foo-b.idc"])

        self.assertEqual(runner.run_test(
            verbose=self.verbose, query_file="querytest/ex_a_b_2.iaq", expected_answersets=27, length=5), 0,
            "Query test with query file: 2 events.")

    def test_one_with_constraint_onelength(self):
        runner = InstalMultiShotTestRunner(input_files=["querytest/basicquery.ial", "querytest/no-viols.lp"],
                                           domain_files=["querytest/foo-a.idc"])

        self.assertEqual(runner.run_test(
            verbose=self.verbose, expected_answersets=1, length=1), 0, "")

    def test_one_with_constraint_fivelength(self):
        runner = InstalMultiShotTestRunner(input_files=["querytest/basicquery.ial", "querytest/no-viols.lp"],
                                           domain_files=["querytest/foo-a.idc"])

        self.assertEqual(runner.run_test(
            verbose=self.verbose, expected_answersets=1, length=5), 0, "")

    def test_one_with_constraint_and_fact_onelength(self):
        runner = InstalMultiShotTestRunner(input_files=["querytest/basicquery.ial", "querytest/no-viols.lp"],
                                           domain_files=["querytest/foo-a.idc"])

        self.assertEqual(runner.run_test(fact_files=["querytest/ex_a_permission.iaf"],
                                         verbose=self.verbose, expected_answersets=2, length=1), 0, "")

    def test_one_with_constraint_and_fact_fivelength(self):
        runner = InstalMultiShotTestRunner(input_files=["querytest/basicquery.ial", "querytest/no-viols.lp"],
                                           domain_files=["querytest/foo-a.idc"])

        self.assertEqual(runner.run_test(fact_files=["querytest/ex_a_permission.iaf"],
                                         verbose=self.verbose, expected_answersets=32, length=5), 0, "")

    def test_solve_query_same(self):
        test_runner = InstalCompareQuerySolve(input_files=["querytest/basicquery.ial"],
                                              bridge_file=None,
                                              domain_files=["querytest/foo-a.idc"], fact_files=[],
                                              query="querytest/ex_a_1.iaq", length=1)
        solve_text, query_text = test_runner.run_test()
        self.assertTrue(query_text == solve_text)
