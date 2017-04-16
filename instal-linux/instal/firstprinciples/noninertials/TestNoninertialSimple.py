from instal.firstprinciples.TestEngine import InstalSingleShotTestRunner, InstalTestCase


class NoninertialSimple(InstalTestCase):

    def test_noninertial_simple_iaf_true(self):
        runner = InstalSingleShotTestRunner(input_files=["noninertials/simple.ial"], bridge_file=None,
                                            domain_files=["noninertials/domain.idc"], fact_files=[])

        in_a_true_condition = [{"holdsat": ["holdsat(n_flu,simple)"]}]

        self.assertEqual(runner.run_test(query_file="noninertials/null.iaq",
                                         fact_files=[
                                             "noninertials/fluent_active.iaf"],
                                         verbose=self.verbose,
                                         conditions=in_a_true_condition), 0, "Noninertial true from loaded fact file")

    def test_noninertial_simple_initiated_true(self):
        runner = InstalSingleShotTestRunner(input_files=["noninertials/simple.ial"], bridge_file=None,
                                            domain_files=["noninertials/domain.idc"], fact_files=[])

        in_a_true_condition = [{"holdsat": ["holdsat(n_flu,simple)"]}]

        self.assertEqual(runner.run_test(query_file="noninertials/simple-ina.iaq",
                                         fact_files=[],
                                         verbose=self.verbose,
                                         conditions=in_a_true_condition), 0, "Noninertial true from initiated fluent")

    def test_noninertial_simple_iaf_false(self):
        runner = InstalSingleShotTestRunner(input_files=["noninertials/simple.ial"], bridge_file=None,
                                            domain_files=["noninertials/domain.idc"], fact_files=[])

        in_a_true_condition = [{"notholdsat": ["holdsat(n_flu,simple)"]}]

        self.assertEqual(runner.run_test(query_file="noninertials/null.iaq",
                                         fact_files=[],
                                         verbose=self.verbose,
                                         conditions=in_a_true_condition), 0, "Noninertial false because not loaded.")

    def test_noninertial_simple_terminated_false(self):
        runner = InstalSingleShotTestRunner(input_files=["noninertials/simple.ial"], bridge_file=None,
                                            domain_files=["noninertials/domain.idc"], fact_files=[])

        in_a_true_condition = [{"notholdsat": ["holdsat(n_flu,simple)"]}]

        self.assertEqual(runner.run_test(query_file="noninertials/simple-inb.iaq",
                                         fact_files=[
                                             "noninertials/fluent_active.iaf"],
                                         verbose=self.verbose,
                                         conditions=in_a_true_condition), 0,
                         "Noninertial true from loaded fact file with termination")

    def test_noninertial_simple_on_and_off(self):
        runner = InstalSingleShotTestRunner(input_files=["noninertials/simple.ial"], bridge_file=None,
                                            domain_files=["noninertials/domain.idc"], fact_files=[])

        in_a_true_condition = [{"holdsat": ["holdsat(n_flu,simple)"]}] + [{"notholdsat": ["holdsat(n_flu,simple)"]}] + [
            {"holdsat": ["holdsat(n_flu,simple)"]}] + [{"notholdsat": ["holdsat(n_flu,simple)"]}]

        self.assertEqual(runner.run_test(query_file="noninertials/simple-on-off-on-off.iaq",
                                         verbose=self.verbose,
                                         conditions=in_a_true_condition), 0, "Noninertial on and off")
