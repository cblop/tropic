from instal.firstprinciples.TestEngine import InstalSingleShotTestRunner, InstalTestCase


class TerminateNormsObligations(InstalTestCase):

    def test_terminate_obligations_institutional_defined(self):
        runner = InstalSingleShotTestRunner(input_files=["obligation/obligation.ial"], bridge_file=None,
                                            domain_files=["obligation/domain.idc"], fact_files=[])

        base_condition = [{"holdsat": ["holdsat(obl(i_req, i_deadline, i_viol), oblig)",
                                       "holdsat(obl(i_req, i_deadline, v_viol), oblig)"]},
                          {"notholdsat": ["holdsat(obl(i_req, i_deadline, i_viol), oblig)",
                                          "holdsat(obl(i_req, i_deadline, v_viol), oblig)"]}
                          ]

        self.assertEqual(runner.run_test(query_file="obligation/initiate-terminate.iaq", verbose=self.verbose,
                                         conditions=base_condition), 0, "Obligations get terminated.")

    def test_terminate_obligations_institutional_undefined(self):
        runner = InstalSingleShotTestRunner(input_files=["obligation/obligation.ial"], bridge_file=None,
                                            domain_files=["obligation/domain.idc"], fact_files=[])

        base_notdefined_condition = [{"holdsat": ["holdsat(obl(i_notdefinedreq, i_deadline, i_viol), oblig)",
                                                  "holdsat(obl(i_notdefinedreq, i_deadline, v_viol), oblig)"]},
                                     {"notholdsat": ["holdsat(obl(i_notdefinedreq, i_deadline, i_viol), oblig)",
                                                     "holdsat(obl(i_notdefinedreq, i_deadline, v_viol), oblig)"]}]

        self.assertEqual(runner.run_test(query_file="obligation/initiate-terminate.iaq", verbose=self.verbose,
                                         conditions=base_notdefined_condition), 0,
                         "Obligations get terminated. (That aren't defined. Expected behaviour?)")
