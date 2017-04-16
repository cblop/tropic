from instal.firstprinciples.TestEngine import InstalSingleShotTestRunner, InstalTestCase


class InitiallyInitiateFluents(InstalTestCase):

    def generate_condition(self, description, alphas, betas):
        # generates the dictionary of required holdsats for a particular
        # description
        condition = []
        for a in alphas:
            for b in betas:
                condition.append(description.format(
                    description, Alpha=a, Beta=b))
        return condition

    def test_ial_initially_fluents_onearg(self):
        alphas = ["alpha_one"]
        betas = ["beta_one"]
        runner = InstalSingleShotTestRunner(input_files=["initially/initially.ial"], bridge_file=[],
                                            domain_files=["initially/one_domain.idc"], fact_files=[])

        condition = [{"holdsat": self.generate_condition(
            "holdsat(flu_a({Alpha}),init)", alphas, betas)}] * 2
        self.assertEqual(runner.run_test(query_file="initially/null_event.iaq", fact_files=[], verbose=self.verbose,
                                         conditions=condition), 0,
                         "A fluent from initially file should be true. (one arg)")

    def test_ial_initially_fluents_twodiffarg(self):
        alphas = ["alpha_one"]
        betas = ["beta_one"]
        runner = InstalSingleShotTestRunner(input_files=["initially/initially.ial"], bridge_file=None,
                                            domain_files=["initially/one_domain.idc"], fact_files=[])

        condition = [{"holdsat": self.generate_condition(
            "holdsat(flu_b({Alpha}, {Beta}),init)", alphas, betas)}] * 2
        self.assertEqual(runner.run_test(query_file="initially/null_event.iaq", fact_files=[], verbose=self.verbose,
                                         conditions=condition), 0,
                         "A fluent in initially file should be true. (two diff args)")

    def test_ial_initially_fluents_twosamearg(self):
        alphas = ["alpha_one"]
        betas = ["beta_one"]
        runner = InstalSingleShotTestRunner(input_files=["initially/initially.ial"], bridge_file=None,
                                            domain_files=["initially/one_domain.idc"], fact_files=[])

        condition = [{"holdsat": self.generate_condition(
            "holdsat(flu_c({Alpha}, {Alpha}),init)", alphas, betas)}] * 2
        self.assertEqual(runner.run_test(query_file="initially/null_event.iaq", fact_files=[], verbose=self.verbose,
                                         conditions=condition), 0,
                         "A fluent in initially file should be true. (two same args)")

    def test_ial_initially_fluents_onearg_domains(self):
        runner = InstalSingleShotTestRunner(input_files=["initially/initially.ial"], bridge_file=None,
                                            domain_files=["initially/three_each.idc"], fact_files=[])
        alphas = ["alpha_one", "alpha_two", "alpha_three"]
        betas = ["beta_one", "beta_two", "beta_three"]

        condition = [{"holdsat": self.generate_condition(
            "holdsat(flu_a({Alpha}),init)", alphas, betas)}] * 2
        self.assertEqual(runner.run_test(query_file="initially/null_event.iaq", fact_files=[], verbose=self.verbose,
                                         conditions=condition), 0,
                         "A fluent from initially file should be true. (one arg, 3 groundings)")

    def test_ial_initially_fluents_twodiffarg_domains(self):
        runner = InstalSingleShotTestRunner(input_files=["initially/initially.ial"], bridge_file=None,
                                            domain_files=["initially/three_each.idc"], fact_files=[])
        alphas = ["alpha_one", "alpha_two", "alpha_three"]
        betas = ["beta_one", "beta_two", "beta_three"]

        condition = [{"holdsat": self.generate_condition(
            "holdsat(flu_b({Alpha},{Beta}),init)", alphas, betas)}] * 2
        self.assertEqual(runner.run_test(query_file="initially/null_event.iaq", fact_files=[], verbose=self.verbose,
                                         conditions=condition), 0,
                         "A fluent in initially file should be true. (two diff args, 3 groundings)")

    def test_ial_initially_fluents_twosamearg_domains(self):
        runner = InstalSingleShotTestRunner(input_files=["initially/initially.ial"], bridge_file=None,
                                            domain_files=["initially/three_each.idc"], fact_files=[])
        alphas = ["alpha_one", "alpha_two", "alpha_three"]
        betas = ["beta_one", "beta_two", "beta_three"]

        condition = [{"holdsat": self.generate_condition(
            "holdsat(flu_c({Alpha}, {Alpha}),init)", alphas, betas)}] * 2
        self.assertEqual(runner.run_test(query_file="initially/null_event.iaq", fact_files=[], verbose=self.verbose,
                                         conditions=condition), 0,
                         "A fluent in initially file should be true. (two same args, 3 groundings)")
