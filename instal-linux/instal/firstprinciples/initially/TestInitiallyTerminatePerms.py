from instal.firstprinciples.TestEngine import InstalSingleShotTestRunner, InstalTestCase


class InitiallyTerminateFluents(InstalTestCase):

    def generate_condition(self, description, alphas, betas):
        # generates the dictionary of required holdsats for a particular
        # description
        condition = []
        for a in alphas:
            for b in betas:
                condition.append(description.format(
                    description, Alpha=a, Beta=b))
        return condition

    def test_terminate_perms_onearg(self):
        alphas = ["alpha_one"]
        betas = ["beta_one"]
        runner = InstalSingleShotTestRunner(input_files=["initially/initially_killperm.ial"], bridge_file=None,
                                            domain_files=["initially/one_domain.idc"], fact_files=[])

        condition = [{"notholdsat": self.generate_condition(
            "holdsat(perm(ex_a({Alpha})),init)", alphas, betas)}] * 2
        self.assertEqual(runner.run_test(query_file="initially/kill_event.iaq", fact_files=[], verbose=self.verbose,
                                         conditions=condition), 0,
                         "A perm from initially file should be terminatable. (one arg)")

    def test_terminate_perms_twodiffargs(self):
        alphas = ["alpha_one"]
        betas = ["beta_one"]
        runner = InstalSingleShotTestRunner(input_files=["initially/initially_killperm.ial"], bridge_file=None,
                                            domain_files=["initially/one_domain.idc"], fact_files=[])

        condition = [{"notholdsat": self.generate_condition("holdsat(perm(ex_b({Alpha}, {Beta})),init)", alphas,
                                                            betas)}] * 2
        self.assertEqual(runner.run_test(query_file="initially/kill_event.iaq", fact_files=[], verbose=self.verbose,
                                         conditions=condition), 0,
                         "A perm from initially file should be terminatable.  (two diff args)")

    def test_terminate_perms_twosameargs(self):
        alphas = ["alpha_one"]
        betas = ["beta_one"]
        runner = InstalSingleShotTestRunner(input_files=["initially/initially_killperm.ial"], bridge_file=None,
                                            domain_files=["initially/one_domain.idc"], fact_files=[])

        condition = [{"notholdsat": self.generate_condition(
            "holdsat(perm(in_a({Alpha})),init)", alphas, betas)}] * 2
        self.assertEqual(runner.run_test(query_file="initially/kill_event.iaq", fact_files=[], verbose=self.verbose,
                                         conditions=condition), 0,
                         "A perm from initially file should be terminatable. (two same args)")
