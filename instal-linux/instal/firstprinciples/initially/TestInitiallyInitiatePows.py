from instal.firstprinciples.TestEngine import InstalSingleShotTestRunner, InstalTestCase


class InitiallyInitiatePows(InstalTestCase):

    def generate_condition(self, description, alphas, betas):
        # generates the dictionary of required holdsats for a particular
        # description
        condition = []
        for a in alphas:
            for b in betas:
                condition.append(description.format(
                    description, Alpha=a, Beta=b))
        return condition

    def test_initially_pows_institutional_onearg(self):
        alphas = ["alpha_one"]
        betas = ["beta_one"]
        runner = InstalSingleShotTestRunner(input_files=["initially/initially.ial"], bridge_file=None,
                                            domain_files=["initially/one_domain.idc"], fact_files=[])

        condition = [{"holdsat": self.generate_condition(
            "holdsat(pow(in_a({Alpha})),init)", alphas, betas)}] * 2
        self.assertEqual(runner.run_test(query_file="initially/null_event.iaq", fact_files=[], verbose=self.verbose,
                                         conditions=condition), 0, "Power from initially file true (one arg, in)")

    def test_initially_pows_institutional_twosameargs(self):
        alphas = ["alpha_one"]
        betas = ["beta_one"]
        runner = InstalSingleShotTestRunner(input_files=["initially/initially.ial"], bridge_file=None,
                                            domain_files=["initially/one_domain.idc"], fact_files=[])

        condition = [{"holdsat": self.generate_condition("holdsat(pow(in_b({Alpha},{Alpha})),init)", alphas,
                                                         betas)}] * 2
        self.assertEqual(runner.run_test(query_file="initially/null_event.iaq", fact_files=[], verbose=self.verbose,
                                         conditions=condition), 0,
                         "Power from initially file true (two args, same, in)")

    def test_initially_pows_institutional_twodiffargs(self):
        alphas = ["alpha_one"]
        betas = ["beta_one"]
        runner = InstalSingleShotTestRunner(input_files=["initially/initially.ial"], bridge_file=None,
                                            domain_files=["initially/one_domain.idc"], fact_files=[])

        condition = [{"holdsat": self.generate_condition("holdsat(pow(in_c({Alpha},{Beta})),init)", alphas,
                                                         betas)}] * 2
        self.assertEqual(runner.run_test(query_file="initially/null_event.iaq", fact_files=[], verbose=self.verbose,
                                         conditions=condition), 0,
                         "Power from initially file true (two args, diff, in)")

    def test_initially_pows_institutional_onearg_domains(self):
        alphas = ["alpha_one", "alpha_two", "alpha_three"]
        betas = ["beta_one", "beta_two", "beta_three"]
        runner = InstalSingleShotTestRunner(input_files=["initially/initially.ial"], bridge_file=None,
                                            domain_files=["initially/three_each.idc"], fact_files=[])

        condition = [{"holdsat": self.generate_condition(
            "holdsat(pow(in_a({Alpha})),init)", alphas, betas)}] * 2
        self.assertEqual(runner.run_test(query_file="initially/null_event.iaq", fact_files=[], verbose=self.verbose,
                                         conditions=condition), 0, "Power from initially file true (one arg, in)")

    def test_initially_pows_institutional_twosameargs_domains(self):
        alphas = ["alpha_one", "alpha_two", "alpha_three"]
        betas = ["beta_one", "beta_two", "beta_three"]
        runner = InstalSingleShotTestRunner(input_files=["initially/initially.ial"], bridge_file=None,
                                            domain_files=["initially/three_each.idc"], fact_files=[])

        condition = [{"holdsat": self.generate_condition("holdsat(pow(in_b({Alpha},{Alpha})),init)", alphas,
                                                         betas)}] * 2
        self.assertEqual(runner.run_test(query_file="initially/null_event.iaq", fact_files=[], verbose=self.verbose,
                                         conditions=condition), 0,
                         "Power from initially file true (two args, same, in)")

    def test_initially_pows_institutional_twodiffargs_domains(self):
        alphas = ["alpha_one", "alpha_two", "alpha_three"]
        betas = ["beta_one", "beta_two", "beta_three"]
        runner = InstalSingleShotTestRunner(input_files=["initially/initially.ial"], bridge_file=None,
                                            domain_files=["initially/three_each.idc"], fact_files=[])

        condition = [{"holdsat": self.generate_condition("holdsat(pow(in_c({Alpha},{Beta})),init)", alphas,
                                                         betas)}] * 2
        self.assertEqual(runner.run_test(query_file="initially/null_event.iaq", fact_files=[], verbose=self.verbose,
                                         conditions=condition), 0,
                         "Power from initially file true (two args, diff, in)")
