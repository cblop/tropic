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

    def test_terminate_obligation(self):
        alphas = ["alpha_one"]
        betas = ["beta_one"]
        runner = InstalSingleShotTestRunner(input_files=["initially/initially_killobl.ial"], bridge_file=None,
                                            domain_files=["initially/one_domain.idc"], fact_files=[])

        condition = [{"notholdsat": self.generate_condition(
            "holdsat(obl(in_a({Alpha}), in_b({Alpha}, {Alpha}), in_c({Alpha}, {Beta})),init)", alphas, betas)}] * 2
        self.assertEqual(runner.run_test(query_file="initially/kill_event.iaq", fact_files=[], verbose=self.verbose,
                                         conditions=condition), 0,
                         "An obl from initially file should be terminatable.  (two diff args)")
