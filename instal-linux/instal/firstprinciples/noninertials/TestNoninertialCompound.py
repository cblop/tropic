from instal.firstprinciples.TestEngine import InstalSingleShotTestRunner, InstalTestCase


class NoninertialCompound(InstalTestCase):

    def test_noninertial_compound_false_nofacts(self):
        runner = InstalSingleShotTestRunner(input_files=["noninertials/compound.ial"], bridge_file=None,
                                            domain_files=["noninertials/domain.idc"], fact_files=[])

        ni_fluent_false = [{"notholdsat": ["holdsat(n_flu,complex)"]}]

        self.assertEqual(runner.run_test(query_file="noninertials/null.iaq",
                                         fact_files=[],
                                         verbose=self.verbose,
                                         conditions=ni_fluent_false), 0, "Noninertial compound: false (no facts)")

    def test_noninertial_compound_false_flu1(self):
        runner = InstalSingleShotTestRunner(input_files=["noninertials/compound.ial"], bridge_file=None,
                                            domain_files=["noninertials/domain.idc"], fact_files=[])

        ni_fluent_false = [{"notholdsat": ["holdsat(n_flu,complex)"]}]

        self.assertEqual(runner.run_test(query_file="noninertials/null.iaq",
                                         fact_files=[
                                             "noninertials/complex-facts/flu1.iaf"],
                                         verbose=self.verbose,
                                         conditions=ni_fluent_false), 0, "Noninertial compound: false (flu1)")

    def test_noninertial_compound_false_flu2(self):
        runner = InstalSingleShotTestRunner(input_files=["noninertials/compound.ial"], bridge_file=None,
                                            domain_files=["noninertials/domain.idc"], fact_files=[])

        ni_fluent_false = [{"notholdsat": ["holdsat(n_flu,complex)"]}]

        self.assertEqual(runner.run_test(query_file="noninertials/null.iaq",
                                         fact_files=[
                                             "noninertials/complex-facts/flu2.iaf"],
                                         verbose=self.verbose,
                                         conditions=ni_fluent_false), 0, "Noninertial compound: false (flu2)")

    def test_noninertial_compound_false_flu3(self):
        runner = InstalSingleShotTestRunner(input_files=["noninertials/compound.ial"], bridge_file=None,
                                            domain_files=["noninertials/domain.idc"], fact_files=[])

        ni_fluent_false = [{"notholdsat": ["holdsat(n_flu,complex)"]}]

        self.assertEqual(runner.run_test(query_file="noninertials/null.iaq",
                                         fact_files=[
                                             "noninertials/complex-facts/flu3.iaf"],
                                         verbose=self.verbose,
                                         conditions=ni_fluent_false), 0, "Noninertial compound: false (flu3)")

    def test_noninertial_compound_false_flu13(self):
        runner = InstalSingleShotTestRunner(input_files=["noninertials/compound.ial"], bridge_file=None,
                                            domain_files=["noninertials/domain.idc"], fact_files=[])

        ni_fluent_false = [{"notholdsat": ["holdsat(n_flu,complex)"]}]

        self.assertEqual(runner.run_test(query_file="noninertials/null.iaq",
                                         fact_files=["noninertials/complex-facts/flu1.iaf",
                                                     "noninertials/complex-facts/flu3.iaf"],
                                         verbose=self.verbose,
                                         conditions=ni_fluent_false), 0, "Noninertial compound: false (flu1+3)")

    def test_noninertial_compound_true_flu12(self):
        runner = InstalSingleShotTestRunner(input_files=["noninertials/compound.ial"], bridge_file=None,
                                            domain_files=["noninertials/domain.idc"], fact_files=[])

        ni_fluent_true = [{"holdsat": ["holdsat(n_flu,complex)"]}]

        self.assertEqual(runner.run_test(query_file="noninertials/null.iaq",
                                         fact_files=["noninertials/complex-facts/flu1.iaf",
                                                     "noninertials/complex-facts/flu2.iaf"],
                                         verbose=self.verbose,
                                         conditions=ni_fluent_true), 0, "Noninertial compound: true (flu1+2)")

    def test_noninertial_compound_true_flu23(self):
        runner = InstalSingleShotTestRunner(input_files=["noninertials/compound.ial"], bridge_file=None,
                                            domain_files=["noninertials/domain.idc"], fact_files=[])

        ni_fluent_true = [{"holdsat": ["holdsat(n_flu,complex)"]}]

        self.assertEqual(runner.run_test(query_file="noninertials/null.iaq",
                                         fact_files=["noninertials/complex-facts/flu2.iaf",
                                                     "noninertials/complex-facts/flu3.iaf"],
                                         verbose=self.verbose,
                                         conditions=ni_fluent_true), 0, "Noninertial compound: true (flu2+3)")

    def test_noninertial_compound_true_flu123(self):
        runner = InstalSingleShotTestRunner(input_files=["noninertials/compound.ial"], bridge_file=None,
                                            domain_files=["noninertials/domain.idc"], fact_files=[])

        ni_fluent_true = [{"holdsat": ["holdsat(n_flu,complex)"]}]

        self.assertEqual(runner.run_test(query_file="noninertials/null.iaq",
                                         fact_files=["noninertials/complex-facts/flu2.iaf",
                                                     "noninertials/complex-facts/flu2.iaf",
                                                     "noninertials/complex-facts/flu3.iaf"],
                                         verbose=self.verbose,
                                         conditions=ni_fluent_true), 0, "Noninertial compound: true (flu1+2+3)")
