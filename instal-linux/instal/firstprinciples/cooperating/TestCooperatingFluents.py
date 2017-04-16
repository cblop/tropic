#!/usr/bin/python3
from instal.firstprinciples.TestEngine import InstalTestCase, InstalSingleShotTestRunner
from instal.instalexceptions import InstalTestNotImplemented


class CooperatingFluents(InstalTestCase):
    # These are to test that facts and fact changes in one institution are not
    # true in the other.

    def test_twoinstitutions_fact_file_permissions_pows(self):
        runner = InstalSingleShotTestRunner(input_files=["cooperating/inst1.ial", "cooperating/inst2.ial"],
                                            bridge_file=None,
                                            domain_files=[
                                                "cooperating/blank.idc"],
                                            fact_files=["cooperating/halfshared_inst1.iaf"])

        condition = [
            {"holdsat": ["holdsat(perm(ex_halfshared), inst1)", "holdsat(pow(in_halfshared), inst1)"],
             "notholdsat": ["holdsat(perm(ex_halfshared), inst2)", "holdsat(pow(in_halfshared), inst2)"]}
        ]

        self.assertEqual(runner.run_test(query_file="cooperating/ex_halfshared.iaq",
                                         verbose=self.verbose,
                                         conditions=condition), 0, "")
    
    def test_twoinstitutions_initiate_terminate_in_one(self):
        runner = InstalSingleShotTestRunner(input_files=["cooperating/inst1.ial", "cooperating/inst2.ial"],
                                            bridge_file=None,
                                            domain_files=[
                                                "cooperating/blank.idc"],
                                            fact_files=["cooperating/halfshared_inst1.iaf",
                                                        "cooperating/halfshared_inst2.iaf"])

        condition = [
            {
                "holdsat" : ["holdsat(flu_halfshared, inst1)"],
                "notholdsat" : ["holdsat(flu_halfshared, inst2)"]
            },
            {
                "notholdsat" : ["holdsat(flu_halfshared, inst1)", "holdsat(flu_halfshared, inst2)"]
            }
        ]

        self.assertEqual(runner.run_test(query_file="cooperating/ex_ini_term.iaq",
                                         verbose=self.verbose,
                                         conditions=condition), 0, "")