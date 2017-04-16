from instal.firstprinciples.TestEngine import InstalSingleShotTestRunner, InstalTestCase


class CooperatingEvents(InstalTestCase):
    # These tests exist to check that events - recognition of exogenous events and generation of institutional events
    # Work with two seperate institutions

    def test_twoinstitutions_exogenous_onerecognises(self):
        runner = InstalSingleShotTestRunner(input_files=["cooperating/inst1.ial", "cooperating/inst2.ial"],
                                            bridge_file=None,
                                            domain_files=[
                                                "cooperating/blank.idc"],
                                            fact_files=[])

        condition = [
            {"occurred": ["occurred(ex_inst1_only,inst1)", "occurred(null,inst2)"],
             "notoccurred": ["occurred(ex_inst1_only,inst2)"]}
        ]

        self.assertEqual(runner.run_test(query_file="cooperating/ex_inst1_only.iaq",
                                         verbose=self.verbose,
                                         conditions=condition), 0, "")

    def test_twoinstitutions_exogenous_bothrecognise(self):
        runner = InstalSingleShotTestRunner(input_files=["cooperating/inst1.ial", "cooperating/inst2.ial"],
                                            bridge_file=None,
                                            domain_files=[
                                                "cooperating/blank.idc"],
                                            fact_files=[])

        condition = [
            {"occurred": ["occurred(ex_shared,inst1)",
                          "occurred(ex_shared,inst2)"]}
        ]

        self.assertEqual(runner.run_test(query_file="cooperating/ex_shared.iaq",
                                         verbose=self.verbose,
                                         conditions=condition), 0, "")

    def test_twoinstitutions_exogenous_nonerecognise(self):
        runner = InstalSingleShotTestRunner(input_files=["cooperating/inst1.ial", "cooperating/inst2.ial"],
                                            bridge_file=None,
                                            domain_files=[
                                                "cooperating/blank.idc"],
                                            fact_files=[])

        condition = [
            {"occurred": ["occurred(null,inst1)", "occurred(null,inst2)"]}
        ]

        self.assertEqual(runner.run_test(query_file="cooperating/ex_none.iaq",
                                         verbose=self.verbose,
                                         conditions=condition), 0, "")

    def test_twoinstitutions_generates(self):
        runner = InstalSingleShotTestRunner(input_files=["cooperating/inst1.ial", "cooperating/inst2.ial"],
                                            bridge_file=None,
                                            domain_files=[
                                                "cooperating/blank.idc"],
                                            fact_files=[])

        condition = [
            {"occurred": ["occurred(ex_shared,inst1)", "occurred(ex_shared,inst2)",
                          "occurred(in_shared,inst1)", "occurred(in_shared,inst2)"]}
        ]

        self.assertEqual(runner.run_test(query_file="cooperating/ex_shared.iaq",
                                         verbose=self.verbose,
                                         conditions=condition), 0, "")

    def test_twoinstitutions_generates_oneinstitution(self):
        runner = InstalSingleShotTestRunner(input_files=["cooperating/inst1.ial", "cooperating/inst2.ial"],
                                            bridge_file=None,
                                            domain_files=[
                                                "cooperating/blank.idc"],
                                            fact_files=[])

        condition = [
            {"occurred": ["occurred(ex_inst1_only,inst1)", "occurred(null,inst2)", "occurred(in_inst1_only,inst1)"],
             "notoccurred": ["occurred(ex_inst1_only,inst2)"]}
        ]

        self.assertEqual(runner.run_test(query_file="cooperating/ex_inst1_only.iaq",
                                         verbose=self.verbose,
                                         conditions=condition), 0, "")

    def test_twoinstitutions_generates_twodifferentevents(self):
        runner = InstalSingleShotTestRunner(input_files=["cooperating/inst1.ial", "cooperating/inst2.ial"],
                                            bridge_file=None,
                                            domain_files=[
                                                "cooperating/blank.idc"],
                                            fact_files=["cooperating/halfshared_inst1.iaf",
                                                        "cooperating/halfshared_inst2.iaf"])

        condition = [
            {"occurred": ["occurred(ex_halfshared,inst1)", "occurred(ex_halfshared,inst2)",
                          "occurred(in_inst1_only,inst1)", "occurred(in_inst2_only,inst2)"],
             "notoccurred": ["occurred(viol(ex_halfshared),inst1)", "occurred(viol(ex_halfshared),inst2)"]}
        ]

        self.assertEqual(runner.run_test(query_file="cooperating/ex_halfshared.iaq",
                                         verbose=self.verbose,
                                         conditions=condition), 0, "")

    def test_twoinstitutions_generates_powers_twodifferent(self):
        runner = InstalSingleShotTestRunner(input_files=["cooperating/inst1.ial", "cooperating/inst2.ial"],
                                            bridge_file=None,
                                            domain_files=[
                                                "cooperating/blank.idc"],
                                            fact_files=[])

        condition = [
            {"occurred": ["occurred(ex_halfshared,inst1)", "occurred(ex_halfshared,inst2)",
                          "occurred(in_halfshared,inst1)"],
             "notoccurred": ["occurred(in_halfshared,inst2)",
                             "occurred(viol(ex_halfshared),inst1)", "occurred(viol(ex_halfshared),inst2)"]}
        ]

        self.assertEqual(runner.run_test(query_file="cooperating/ex_halfshared.iaq",
                                         verbose=self.verbose,
                                         fact_files=["cooperating/halfshared_inst1.iaf",
                                                     "cooperating/perm_halfshared_inst2.iaf"],
                                         conditions=condition), 0, "")

    def test_twoinstitutions_generates_permissions_exogenous(self):
        runner = InstalSingleShotTestRunner(input_files=["cooperating/inst1.ial", "cooperating/inst2.ial"],
                                            bridge_file=None,
                                            domain_files=[
                                                "cooperating/blank.idc"],
                                            fact_files=[])

        condition = [
            {"occurred": ["occurred(ex_halfshared,inst1)", "occurred(ex_halfshared,inst2)",
                          "occurred(in_halfshared,inst1)", "occurred(viol(ex_halfshared),inst2)"],
             "notoccurred": ["occurred(in_halfshared,inst2)",
                             "occurred(viol(ex_halfshared),inst1)"]}
        ]

        self.assertEqual(runner.run_test(query_file="cooperating/ex_halfshared.iaq",
                                         verbose=self.verbose,
                                         fact_files=[
                                             "cooperating/halfshared_inst1.iaf"],
                                         conditions=condition), 0, "")
