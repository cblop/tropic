from instal.firstprinciples.TestEngine import InstalSingleShotTestRunner, InstalMultiShotTestRunner, InstalTestCase


class UnrecognisedEvents(InstalTestCase):

    def test_recognised_query(self):
        runner = InstalMultiShotTestRunner(input_files=["unrecognisedevents/unrecogevent.ial"], bridge_file=None,
                                           domain_files=["unrecognisedevents/domain.idc"], fact_files=[])

        self.assertEqual(runner.run_test(
            verbose=self.verbose, query_file="unrecognisedevents/recognised.iaq", expected_answersets=1), 0, "")

    def test_unrecognised_eventname_query(self):
        runner = InstalMultiShotTestRunner(input_files=["unrecognisedevents/unrecogevent.ial"], bridge_file=None,
                                           domain_files=["unrecognisedevents/domain.idc"], fact_files=[])

        self.assertEqual(runner.run_test(
            verbose=self.verbose, query_file="unrecognisedevents/unrecognised.iaq", expected_answersets=1), 0, "")

    def test_unrecognised_argnum1_query(self):
        runner = InstalMultiShotTestRunner(input_files=["unrecognisedevents/unrecogevent.ial"], bridge_file=None,
                                           domain_files=["unrecognisedevents/domain.idc"], fact_files=[])

        self.assertEqual(runner.run_test(
            verbose=self.verbose, query_file="unrecognisedevents/unrecognised_argnum1.iaq", expected_answersets=1), 0,
            "")

    def test_unrecognised_argnum2_query(self):
        runner = InstalMultiShotTestRunner(input_files=["unrecognisedevents/unrecogevent.ial"], bridge_file=None,
                                           domain_files=["unrecognisedevents/domain.idc"], fact_files=[])

        self.assertEqual(runner.run_test(
            verbose=self.verbose, query_file="unrecognisedevents/unrecognised_argnum2.iaq", expected_answersets=1), 0,
            "")

    def test_unrecognised_argnum3_query(self):
        runner = InstalMultiShotTestRunner(input_files=["unrecognisedevents/unrecogevent.ial"], bridge_file=None,
                                           domain_files=["unrecognisedevents/domain.idc"], fact_files=[])

        self.assertEqual(runner.run_test(
            verbose=self.verbose, query_file="unrecognisedevents/unrecognised_argnum3.iaq", expected_answersets=1), 0,
            "")

    def test_unrecognised_type1_query(self):
        runner = InstalMultiShotTestRunner(input_files=["unrecognisedevents/unrecogevent.ial"], bridge_file=None,
                                           domain_files=["unrecognisedevents/domain.idc"], fact_files=[])

        self.assertEqual(runner.run_test(
            verbose=self.verbose, query_file="unrecognisedevents/unrecognised_type1.iaq", expected_answersets=1), 0, "")

    def test_unrecognised_type2_query(self):
        runner = InstalMultiShotTestRunner(input_files=["unrecognisedevents/unrecogevent.ial"], bridge_file=None,
                                           domain_files=["unrecognisedevents/domain.idc"], fact_files=[])

        self.assertEqual(runner.run_test(
            verbose=self.verbose, query_file="unrecognisedevents/unrecognised_type2.iaq", expected_answersets=1), 0, "")

    def test_unrecognised_type3_query(self):
        runner = InstalMultiShotTestRunner(input_files=["unrecognisedevents/unrecogevent.ial"], bridge_file=None,
                                           domain_files=["unrecognisedevents/domain.idc"], fact_files=[])

        self.assertEqual(runner.run_test(
            verbose=self.verbose, query_file="unrecognisedevents/unrecognised_type3.iaq", expected_answersets=1), 0, "")

    def test_recognised_solve(self):
        runner = InstalSingleShotTestRunner(input_files=["unrecognisedevents/unrecogevent.ial"], bridge_file=None,
                                            domain_files=["unrecognisedevents/domain.idc"], fact_files=[])
        conditions = [{"occurred": ["occurred(recognised, unrecog)"]}]
        self.assertEqual(runner.run_test(
            verbose=self.verbose, query_file="unrecognisedevents/recognised.iaq", conditions=conditions), 0, "")

    def test_unrecognised_eventname_solve(self):
        runner = InstalSingleShotTestRunner(input_files=["unrecognisedevents/unrecogevent.ial"], bridge_file=None,
                                            domain_files=["unrecognisedevents/domain.idc"], fact_files=[])

        conditions = [{"occurred": ["occurred(null, unrecog)"]}]
        self.assertEqual(runner.run_test(
            verbose=self.verbose, query_file="unrecognisedevents/unrecognised.iaq", conditions=conditions), 0, "")

    def test_unrecognised_argnum1_solve(self):
        runner = InstalSingleShotTestRunner(input_files=["unrecognisedevents/unrecogevent.ial"], bridge_file=None,
                                            domain_files=["unrecognisedevents/domain.idc"], fact_files=[])

        conditions = [{"occurred": ["occurred(null, unrecog)"]}]
        self.assertEqual(runner.run_test(
            verbose=self.verbose, query_file="unrecognisedevents/unrecognised_argnum1.iaq", conditions=conditions), 0,
            "")

    def test_unrecognised_argnum2_solve(self):
        runner = InstalSingleShotTestRunner(input_files=["unrecognisedevents/unrecogevent.ial"], bridge_file=None,
                                            domain_files=["unrecognisedevents/domain.idc"], fact_files=[])

        conditions = [{"occurred": ["occurred(null, unrecog)"]}]
        self.assertEqual(runner.run_test(
            verbose=self.verbose, query_file="unrecognisedevents/unrecognised_argnum2.iaq", conditions=conditions), 0,
            "")

    def test_unrecognised_argnum3_solve(self):
        runner = InstalSingleShotTestRunner(input_files=["unrecognisedevents/unrecogevent.ial"], bridge_file=None,
                                            domain_files=["unrecognisedevents/domain.idc"], fact_files=[])

        conditions = [{"occurred": ["occurred(null, unrecog)"]}]
        self.assertEqual(runner.run_test(
            verbose=self.verbose, query_file="unrecognisedevents/unrecognised_argnum3.iaq", conditions=conditions), 0,
            "")

    def test_unrecognised_type1_solve(self):
        runner = InstalSingleShotTestRunner(input_files=["unrecognisedevents/unrecogevent.ial"], bridge_file=None,
                                            domain_files=["unrecognisedevents/domain.idc"], fact_files=[])

        conditions = [{"occurred": ["occurred(null, unrecog)"]}]
        self.assertEqual(runner.run_test(
            verbose=self.verbose, query_file="unrecognisedevents/unrecognised_type1.iaq", conditions=conditions), 0, "")

    def test_unrecognised_type2_solve(self):
        runner = InstalSingleShotTestRunner(input_files=["unrecognisedevents/unrecogevent.ial"], bridge_file=None,
                                            domain_files=["unrecognisedevents/domain.idc"], fact_files=[])

        conditions = [{"occurred": ["occurred(null, unrecog)"]}]
        self.assertEqual(runner.run_test(
            verbose=self.verbose, query_file="unrecognisedevents/unrecognised_type2.iaq", conditions=conditions), 0, "")

    def test_unrecognised_type3_solve(self):
        runner = InstalSingleShotTestRunner(input_files=["unrecognisedevents/unrecogevent.ial"], bridge_file=None,
                                            domain_files=["unrecognisedevents/domain.idc"], fact_files=[])

        conditions = [{"occurred": ["occurred(null, unrecog)"]}]
        self.assertEqual(runner.run_test(
            verbose=self.verbose, query_file="unrecognisedevents/unrecognised_type3.iaq", conditions=conditions), 0, "")
