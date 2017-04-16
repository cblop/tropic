from instal.firstprinciples.TestEngine import InstalSingleShotTestRunner, InstalTestCase


class InitiallyTerminatePows(InstalTestCase):

    def generate_condition(self, description, alphas, betas):
        # generates the dictionary of required holdsats for a particular
        # description
        condition = []
        for a in alphas:
            for b in betas:
                condition.append(description.format(
                    description, Alpha=a, Beta=b))
        return condition

    def test_terminate_pows_onearg(self):
        alphas = ["alpha_one"]
        betas = ["beta_one"]
        runner = InstalSingleShotTestRunner(input_files=["initially/initially_killpow.ial"], bridge_file=None,
                                            domain_files=["initially/one_domain.idc"], fact_files=[])

        condition = [{"notholdsat": self.generate_condition(
            "holdsat(pow(in_a({Alpha})),init)", alphas, betas)}] * 2
        self.assertEqual(runner.run_test(query_file="initially/kill_event.iaq", fact_files=[], verbose=self.verbose,
                                         conditions=condition), 0, "Kill power from initially file  (one arg, in)")

    def test_terminate_pows_twosameargs(self):
        alphas = ["alpha_one"]
        betas = ["beta_one"]
        runner = InstalSingleShotTestRunner(input_files=["initially/initially_killpow.ial"], bridge_file=None,
                                            domain_files=["initially/one_domain.idc"], fact_files=[])

        condition = [{"notholdsat": self.generate_condition("holdsat(pow(in_b({Alpha},{Alpha})),init)", alphas,
                                                            betas)}] * 2
        self.assertEqual(runner.run_test(query_file="initially/kill_event.iaq", fact_files=[], verbose=self.verbose,
                                         conditions=condition), 0,
                         "Kill power from initially file  (two args, same, in)")

    def test_terminate_pows_twodiffargs(self):
        alphas = ["alpha_one"]
        betas = ["beta_one"]
        runner = InstalSingleShotTestRunner(input_files=["initially/initially_killpow.ial"], bridge_file=None,
                                            domain_files=["initially/one_domain.idc"], fact_files=[])

        condition = [{"notholdsat": self.generate_condition("holdsat(pow(in_c({Alpha},{Beta})),init)", alphas,
                                                            betas)}] * 2
        self.assertEqual(runner.run_test(query_file="initially/kill_event.iaq", fact_files=[], verbose=self.verbose,
                                         conditions=condition), 0,
                         "Kill power from initially file (two args, diff, in)")
