from instal.firstprinciples.TestEngine import InstalSingleShotTestRunner, InstalTestCase


class NoninertialSimple(InstalTestCase):

    def test_complex_noninertial_true_all_on(self):
        runner = InstalSingleShotTestRunner(input_files=["noninertials/complex.ial"], bridge_file=None,
                                            domain_files=["noninertials/domain.idc"], fact_files=[])

        all_on_condition = [{"holdsat": ["holdsat(n_all_in,complex)",
                                         "holdsat(n_2flu_pow,complex)",
                                         "holdsat(n_2flu_perm,complex)",
                                         "holdsat(n_2flu_obl,complex)",
                                         "holdsat(n_1flu_perm_pow,complex)",
                                         "holdsat(n_perm_pow_obl,complex)"]}]

        self.assertEqual(runner.run_test(query_file="noninertials/null.iaq",
                                         fact_files=["noninertials/complex-facts/flu1.iaf",
                                                     "noninertials/complex-facts/flu2.iaf",
                                                     "noninertials/complex-facts/flu3.iaf",
                                                     "noninertials/complex-facts/pow.iaf",
                                                     "noninertials/complex-facts/perm.iaf",
                                                     "noninertials/complex-facts/obl.iaf"],
                                         verbose=self.verbose,
                                         conditions=all_on_condition), 0, "Noninertial complex: all on")

    def test_complex_noninertial_true_n_all_in(self):
        runner = InstalSingleShotTestRunner(input_files=["noninertials/complex.ial"], bridge_file=None,
                                            domain_files=["noninertials/domain.idc"], fact_files=[])

        only_n_all_in = [{"holdsat": ["holdsat(n_all_in,complex)"],
                          "notholdsat": ["holdsat(n_2flu_pow,complex)",
                                         "holdsat(n_2flu_perm,complex)",
                                         "holdsat(n_2flu_obl,complex)",
                                         "holdsat(n_1flu_perm_pow,complex)",
                                         "holdsat(n_perm_pow_obl,complex)"]}]

        self.assertEqual(runner.run_test(query_file="noninertials/null.iaq",
                                         fact_files=["noninertials/complex-facts/flu1.iaf",
                                                     "noninertials/complex-facts/flu2.iaf",
                                                     "noninertials/complex-facts/flu3.iaf"],
                                         verbose=self.verbose,
                                         conditions=only_n_all_in), 0, "Noninertial complex: only n_all_in on")

    def test_complex_noninertial_2flu_pow(self):
        runner = InstalSingleShotTestRunner(input_files=["noninertials/complex.ial"], bridge_file=None,
                                            domain_files=["noninertials/domain.idc"], fact_files=[])

        only_2flu_pow_on = [{"holdsat": ["holdsat(n_2flu_pow,complex)", ],
                             "notholdsat": ["holdsat(n_all_in,complex)",
                                            "holdsat(n_2flu_perm,complex)",
                                            "holdsat(n_2flu_obl,complex)",
                                            "holdsat(n_1flu_perm_pow,complex)",
                                            "holdsat(n_perm_pow_obl,complex)"]}]

        self.assertEqual(runner.run_test(query_file="noninertials/null.iaq",
                                         fact_files=["noninertials/complex-facts/flu1.iaf",
                                                     "noninertials/complex-facts/flu2.iaf",
                                                     "noninertials/complex-facts/pow.iaf"],
                                         verbose=self.verbose,
                                         conditions=only_2flu_pow_on), 0, "Noninertial complex: only  2flu_pow_on on")

    def test_complex_noninertial_2flu_perm(self):
        runner = InstalSingleShotTestRunner(input_files=["noninertials/complex.ial"], bridge_file=None,
                                            domain_files=["noninertials/domain.idc"], fact_files=[])

        only_2flu_perm_on = [{"holdsat": ["holdsat(n_2flu_perm,complex)", ],
                              "notholdsat": ["holdsat(n_all_in,complex)",
                                             "holdsat(n_2flu_pow,complex)",
                                             "holdsat(n_2flu_obl,complex)",
                                             "holdsat(n_1flu_perm_pow,complex)",
                                             "holdsat(n_perm_pow_obl,complex)"]}]

        self.assertEqual(runner.run_test(query_file="noninertials/null.iaq",
                                         fact_files=["noninertials/complex-facts/flu1.iaf",
                                                     "noninertials/complex-facts/flu2.iaf",
                                                     "noninertials/complex-facts/perm.iaf"],
                                         verbose=self.verbose,
                                         conditions=only_2flu_perm_on), 0,
                         "Noninertial complex: only  2flu_perm_on  on")

    def test_complex_noninertial_2flu_obl(self):
        runner = InstalSingleShotTestRunner(input_files=["noninertials/complex.ial"], bridge_file=None,
                                            domain_files=["noninertials/domain.idc"], fact_files=[])

        only_2flu_obl_on = [{"holdsat": ["holdsat(n_2flu_obl,complex)", ],
                             "notholdsat": ["holdsat(n_all_in,complex)",
                                            "holdsat(n_2flu_pow,complex)",
                                            "holdsat(n_2flu_perm,complex)",
                                            "holdsat(n_1flu_perm_pow,complex)",
                                            "holdsat(n_perm_pow_obl,complex)"]}]

        self.assertEqual(runner.run_test(query_file="noninertials/null.iaq",
                                         fact_files=["noninertials/complex-facts/flu1.iaf",
                                                     "noninertials/complex-facts/flu2.iaf",
                                                     "noninertials/complex-facts/obl.iaf"],
                                         verbose=self.verbose,
                                         conditions=only_2flu_obl_on), 0, "Noninertial complex: only  2flu_obl_on  on")

    def test_complex_noninertial_1flu_perm_pow(self):
        runner = InstalSingleShotTestRunner(input_files=["noninertials/complex.ial"], bridge_file=None,
                                            domain_files=["noninertials/domain.idc"], fact_files=[])

        only_1flu_perm_pow_on = [{"holdsat": ["holdsat(n_1flu_perm_pow,complex)", ],
                                  "notholdsat": ["holdsat(n_all_in,complex)",
                                                 "holdsat(n_2flu_obl,complex)",
                                                 "holdsat(n_2flu_perm,complex)",
                                                 "holdsat(n_2flu_pow,complex)",
                                                 "holdsat(n_perm_pow_obl,complex)"]}]

        self.assertEqual(runner.run_test(query_file="noninertials/null.iaq",
                                         fact_files=["noninertials/complex-facts/flu1.iaf",
                                                     "noninertials/complex-facts/perm.iaf",
                                                     "noninertials/complex-facts/pow.iaf"],
                                         verbose=self.verbose,
                                         conditions=only_1flu_perm_pow_on), 0,
                         "Noninertial complex: only 1flu_perm_pow on")

    def test_complex_noninertial_perm_pow_obl(self):
        runner = InstalSingleShotTestRunner(input_files=["noninertials/complex.ial"], bridge_file=None,
                                            domain_files=["noninertials/domain.idc"], fact_files=[])

        only_perm_pow_obl_on = [{"holdsat": ["holdsat(n_perm_pow_obl,complex)", ],
                                 "notholdsat": ["holdsat(n_all_in,complex)",
                                                "holdsat(n_2flu_obl,complex)",
                                                "holdsat(n_2flu_perm,complex)",
                                                "holdsat(n_2flu_pow,complex)",
                                                "holdsat(n_1flu_perm_pow,complex)"]}]

        self.assertEqual(runner.run_test(query_file="noninertials/null.iaq",
                                         fact_files=["noninertials/complex-facts/obl.iaf",
                                                     "noninertials/complex-facts/perm.iaf",
                                                     "noninertials/complex-facts/pow.iaf"],
                                         verbose=self.verbose,
                                         conditions=only_perm_pow_obl_on), 0,
                         "Noninertial complex: only only_perm_pow_obl_on on")

    def test_complex_noninertial_flu123_pow(self):
        runner = InstalSingleShotTestRunner(input_files=["noninertials/complex.ial"], bridge_file=None,
                                            domain_files=["noninertials/domain.idc"], fact_files=[])

        flu_123pow = [{"holdsat": ["holdsat(n_all_in,complex)",
                                   "holdsat(n_2flu_pow,complex)", ],
                       "notholdsat": ["holdsat(n_2flu_perm,complex)",
                                      "holdsat(n_2flu_obl,complex)",
                                      "holdsat(n_1flu_perm_pow,complex)",
                                      "holdsat(n_perm_pow_obl,complex)"]
                       }]

        self.assertEqual(runner.run_test(query_file="noninertials/null.iaq",
                                         fact_files=["noninertials/complex-facts/flu1.iaf",
                                                     "noninertials/complex-facts/flu2.iaf",
                                                     "noninertials/complex-facts/flu3.iaf",
                                                     "noninertials/complex-facts/pow.iaf"],
                                         verbose=self.verbose,
                                         conditions=flu_123pow), 0, "Noninertial complex: flu1+2+3+pow on")

    def test_complex_noninertial_flu123_pow_perm(self):
        runner = InstalSingleShotTestRunner(input_files=["noninertials/complex.ial"], bridge_file=None,
                                            domain_files=["noninertials/domain.idc"], fact_files=[])

        flu_123powperm = [{"holdsat": ["holdsat(n_all_in,complex)",
                                       "holdsat(n_2flu_pow,complex)",
                                       "holdsat(n_2flu_perm,complex)",
                                       "holdsat(n_1flu_perm_pow,complex)"],
                           "notholdsat": [
                               "holdsat(n_2flu_obl,complex)",
                               "holdsat(n_perm_pow_obl,complex)"]
                           }]

        self.assertEqual(runner.run_test(query_file="noninertials/null.iaq",
                                         fact_files=["noninertials/complex-facts/flu1.iaf",
                                                     "noninertials/complex-facts/flu2.iaf",
                                                     "noninertials/complex-facts/flu3.iaf",
                                                     "noninertials/complex-facts/pow.iaf",
                                                     "noninertials/complex-facts/perm.iaf"],
                                         verbose=self.verbose,
                                         conditions=flu_123powperm), 0, "Noninertial complex: flu1+2+3+pow+perm on")

    def test_complex_noninertial_all_false_nofacts(self):
        runner = InstalSingleShotTestRunner(input_files=["noninertials/complex.ial"], bridge_file=None,
                                            domain_files=["noninertials/domain.idc"], fact_files=[])

        all_false = [{"notholdsat": ["holdsat(n_all_in,complex)",
                                     "holdsat(n_2flu_pow,complex)",
                                     "holdsat(n_2flu_perm,complex)",
                                     "holdsat(n_2flu_obl,complex)",
                                     "holdsat(n_1flu_perm_pow,complex)",
                                     "holdsat(n_perm_pow_obl,complex)"]
                      }]

        self.assertEqual(runner.run_test(query_file="noninertials/null.iaq",
                                         fact_files=[],
                                         verbose=self.verbose,
                                         conditions=all_false), 0, "Noninertial complex: all false (no facts)")

    def test_complex_noninertial_all_false_flu1(self):
        runner = InstalSingleShotTestRunner(input_files=["noninertials/complex.ial"], bridge_file=None,
                                            domain_files=["noninertials/domain.idc"], fact_files=[])

        all_false = [{"notholdsat": ["holdsat(n_all_in,complex)",
                                     "holdsat(n_2flu_pow,complex)",
                                     "holdsat(n_2flu_perm,complex)",
                                     "holdsat(n_2flu_obl,complex)",
                                     "holdsat(n_1flu_perm_pow,complex)",
                                     "holdsat(n_perm_pow_obl,complex)"]
                      }]

        self.assertEqual(runner.run_test(query_file="noninertials/null.iaq",
                                         fact_files=[
                                             "noninertials/complex-facts/flu1.iaf"],
                                         verbose=self.verbose,
                                         conditions=all_false), 0, "Noninertial complex: all false (flu1)")

    def test_complex_noninertial_all_false_flu12(self):
        runner = InstalSingleShotTestRunner(input_files=["noninertials/complex.ial"], bridge_file=None,
                                            domain_files=["noninertials/domain.idc"], fact_files=[])

        all_false = [{"notholdsat": ["holdsat(n_all_in,complex)",
                                     "holdsat(n_2flu_pow,complex)",
                                     "holdsat(n_2flu_perm,complex)",
                                     "holdsat(n_2flu_obl,complex)",
                                     "holdsat(n_1flu_perm_pow,complex)",
                                     "holdsat(n_perm_pow_obl,complex)"]
                      }]

        self.assertEqual(runner.run_test(query_file="noninertials/null.iaq",
                                         fact_files=["noninertials/complex-facts/flu1.iaf",
                                                     "noninertials/complex-facts/flu2.iaf"],
                                         verbose=self.verbose,
                                         conditions=all_false), 0, "Noninertial complex: all false (flu1+2)")

    def test_complex_noninertial_all_false_perm(self):
        runner = InstalSingleShotTestRunner(input_files=["noninertials/complex.ial"], bridge_file=None,
                                            domain_files=["noninertials/domain.idc"], fact_files=[])

        all_false = [{"notholdsat": ["holdsat(n_all_in,complex)",
                                     "holdsat(n_2flu_pow,complex)",
                                     "holdsat(n_2flu_perm,complex)",
                                     "holdsat(n_2flu_obl,complex)",
                                     "holdsat(n_1flu_perm_pow,complex)",
                                     "holdsat(n_perm_pow_obl,complex)"]
                      }]

        self.assertEqual(runner.run_test(query_file="noninertials/null.iaq",
                                         fact_files=[
                                             "noninertials/complex-facts/perm.iaf"],
                                         verbose=self.verbose,
                                         conditions=all_false), 0, "Noninertial complex: all false (perm)")

    def test_complex_noninertial_all_false_pow(self):
        runner = InstalSingleShotTestRunner(input_files=["noninertials/complex.ial"], bridge_file=None,
                                            domain_files=["noninertials/domain.idc"], fact_files=[])

        all_false = [{"notholdsat": ["holdsat(n_all_in,complex)",
                                     "holdsat(n_2flu_pow,complex)",
                                     "holdsat(n_2flu_perm,complex)",
                                     "holdsat(n_2flu_obl,complex)",
                                     "holdsat(n_1flu_perm_pow,complex)",
                                     "holdsat(n_perm_pow_obl,complex)"]
                      }]

        self.assertEqual(runner.run_test(query_file="noninertials/null.iaq",
                                         fact_files=[
                                             "noninertials/complex-facts/pow.iaf"],
                                         verbose=self.verbose,
                                         conditions=all_false), 0, "Noninertial complex: all false (pow)")

    def test_complex_noninertial_all_false_permpow(self):
        runner = InstalSingleShotTestRunner(input_files=["noninertials/complex.ial"], bridge_file=None,
                                            domain_files=["noninertials/domain.idc"], fact_files=[])

        all_false = [{"notholdsat": ["holdsat(n_all_in,complex)",
                                     "holdsat(n_2flu_pow,complex)",
                                     "holdsat(n_2flu_perm,complex)",
                                     "holdsat(n_2flu_obl,complex)",
                                     "holdsat(n_1flu_perm_pow,complex)",
                                     "holdsat(n_perm_pow_obl,complex)"]
                      }]

        self.assertEqual(runner.run_test(query_file="noninertials/null.iaq",
                                         fact_files=["noninertials/complex-facts/perm.iaf",
                                                     "noninertials/complex-facts/pow.iaf"],
                                         verbose=self.verbose,
                                         conditions=all_false), 0, "Noninertial complex: all false (perm+pow)")

    def test_complex_noninertial_all_false_obl(self):
        runner = InstalSingleShotTestRunner(input_files=["noninertials/complex.ial"], bridge_file=None,
                                            domain_files=["noninertials/domain.idc"], fact_files=[])

        all_false = [{"notholdsat": ["holdsat(n_all_in,complex)",
                                     "holdsat(n_2flu_pow,complex)",
                                     "holdsat(n_2flu_perm,complex)",
                                     "holdsat(n_2flu_obl,complex)",
                                     "holdsat(n_1flu_perm_pow,complex)",
                                     "holdsat(n_perm_pow_obl,complex)"]
                      }]

        self.assertEqual(runner.run_test(query_file="noninertials/null.iaq",
                                         fact_files=[
                                             "noninertials/complex-facts/obl.iaf"],
                                         verbose=self.verbose,
                                         conditions=all_false), 0, "Noninertial complex: all false (obl)")
