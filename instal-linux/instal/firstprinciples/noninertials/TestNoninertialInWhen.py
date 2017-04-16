from instal.firstprinciples.TestEngine import InstalSingleShotTestRunner, InstalTestCase


class NoninertialInWhen(InstalTestCase):

    def test_noninertial_in_when_bothfalse_one(self):
        runner = InstalSingleShotTestRunner(input_files=["noninertials/noninertial_when.ial"], bridge_file=None,
                                            domain_files=["noninertials/domain.idc"], fact_files=[])

        bothfalse = [
            {"notholdsat": ["holdsat(n_flu1,complex)", "holdsat(n_flu2,complex)"]}]

        self.assertEqual(runner.run_test(query_file="noninertials/null.iaq",
                                         fact_files=[],
                                         verbose=self.verbose,
                                         conditions=bothfalse), 0, "Noninertial when: false (no facts)")

    def test_noninertial_in_when_bothfalse_two(self):
        runner = InstalSingleShotTestRunner(input_files=["noninertials/noninertial_when.ial"], bridge_file=None,
                                            domain_files=["noninertials/domain.idc"], fact_files=[])

        bothfalse = [
            {"notholdsat": ["holdsat(n_flu1,complex)", "holdsat(n_flu2,complex)"]}]

        self.assertEqual(runner.run_test(query_file="noninertials/null.iaq",
                                         fact_files=[
                                             "noninertials/complex-facts/flu2.iaf"],
                                         verbose=self.verbose,
                                         conditions=bothfalse), 0, "Noninertial when: false (flu2)")

    def test_noninertial_in_when_onetrue(self):
        runner = InstalSingleShotTestRunner(input_files=["noninertials/noninertial_when.ial"], bridge_file=None,
                                            domain_files=["noninertials/domain.idc"], fact_files=[])

        onetrue = [{"holdsat": ["holdsat(n_flu1,complex)"], "notholdsat": [
            "holdsat(n_flu2,complex)"]}]

        self.assertEqual(runner.run_test(query_file="noninertials/null.iaq",
                                         fact_files=[
                                             "noninertials/complex-facts/flu1.iaf"],
                                         verbose=self.verbose,
                                         conditions=onetrue), 0, "Noninertial when: one true (flu1)")

    def test_noninertial_in_when_bothtrue(self):
        runner = InstalSingleShotTestRunner(input_files=["noninertials/noninertial_when.ial"], bridge_file=None,
                                            domain_files=["noninertials/domain.idc"], fact_files=[])

        bothtrue = [
            {"holdsat": ["holdsat(n_flu1,complex)", "holdsat(n_flu2,complex)"]}]

        self.assertEqual(runner.run_test(query_file="noninertials/null.iaq",
                                         fact_files=["noninertials/complex-facts/flu1.iaf",
                                                     "noninertials/complex-facts/flu2.iaf"],
                                         verbose=self.verbose,
                                         conditions=bothtrue), 0, "Noninertial when: both true (flu1+2)")
