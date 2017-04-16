#!/usr/bin/python3
from instal.firstprinciples.TestEngine import InstalSingleShotTestRunner, InstalTestCase


class FactFileInitiates(InstalTestCase):

    def test_iaf_fluent(self):
        runner = InstalSingleShotTestRunner(input_files=["facts/facts.ial"], bridge_file=None,
                                            domain_files=["facts/facts.idc"],
                                            fact_files=[])

        in_fact_holdsat_condition = [
            {"holdsat": ["holdsat(in_fact(foo),fact)"]}]
        self.assertEqual(
            runner.run_test(query_file="facts/dummy-1.iaq", fact_files=["facts/fluent_true.iaf"], verbose=self.verbose,
                            conditions=in_fact_holdsat_condition), 0, "A fluent in .iaf file should be true.")

        self.assertEqual(
            runner.run_test(query_file="facts/dummy-5.iaq", fact_files=["facts/fluent_true.iaf"], verbose=self.verbose,
                            conditions=in_fact_holdsat_condition * 5), 0, "A fluent in .iaf file should stay true.")

    def test_iaf_fluent_perm_exogenous(self):
        runner = InstalSingleShotTestRunner(input_files=["facts/facts.ial"], bridge_file=None,
                                            domain_files=["facts/facts.idc"],
                                            fact_files=[])

        perm_ex_a_condition = [{"holdsat": ["holdsat(perm(ex_a(foo)),fact)"]}]
        # Permission, in .iaf, fluent holds.
        self.assertEqual(
            runner.run_test(query_file="facts/dummy-1.iaq", fact_files=["facts/perm_ex_true.iaf"], verbose=self.verbose,
                            conditions=perm_ex_a_condition), 0, "Permission for ex event in .iaf file should be true.")

        self.assertEqual(
            runner.run_test(query_file="facts/dummy-5.iaq", fact_files=["facts/perm_ex_true.iaf"], verbose=self.verbose,
                            conditions=perm_ex_a_condition * 5), 0,
            "Permission for ex event in .iaf file should stay true.")

    def test_iaf_fluent_pow_exogenous(self):
        runner = InstalSingleShotTestRunner(input_files=["facts/facts.ial"], bridge_file=None,
                                            domain_files=["facts/facts.idc"],
                                            fact_files=[])

        pow_ex_a_condition = [{"notholdsat": ["holdsat(pow(ex_a(foo)),fact)"]}]

        self.assertEqual(
            runner.run_test(query_file="facts/dummy-1.iaq", fact_files=["facts/pow_ex_true.iaf"], verbose=self.verbose,
                            conditions=pow_ex_a_condition), 0,
            "Power for exogenous event in .iaf file should be false.")

        self.assertEqual(
            runner.run_test(query_file="facts/dummy-5.iaq", fact_files=["facts/pow_ex_true.iaf"], verbose=self.verbose,
                            conditions=pow_ex_a_condition * 5), 0,
            "Power for exogenous event in .iaf file should stay false.")

    def test_iaf_fluent_perm_institutional(self):
        runner = InstalSingleShotTestRunner(input_files=["facts/facts.ial"], bridge_file=None,
                                            domain_files=["facts/facts.idc"],
                                            fact_files=[])

        perm_in_a_condition = [{"holdsat": ["holdsat(perm(in_a(foo)),fact)"]}]

        self.assertEqual(
            runner.run_test(query_file="facts/dummy-1.iaq", fact_files=["facts/perm_in_true.iaf"], verbose=self.verbose,
                            conditions=perm_in_a_condition), 0,
            "Permission for inst event in .iaf file should be true.")

        self.assertEqual(
            runner.run_test(query_file="facts/dummy-5.iaq", fact_files=["facts/perm_in_true.iaf"], verbose=self.verbose,
                            conditions=perm_in_a_condition * 5), 0,
            "Permission for inst event in .iaf file should stay true.")

    def test_iaf_fluent_pow_institutional(self):
        runner = InstalSingleShotTestRunner(input_files=["facts/facts.ial"], bridge_file=None,
                                            domain_files=["facts/facts.idc"],
                                            fact_files=[])

        pow_in_a_condition = [{"holdsat": ["holdsat(pow(in_a(foo)),fact)"]}]

        self.assertEqual(
            runner.run_test(query_file="facts/dummy-1.iaq", fact_files=["facts/pow_in_true.iaf"], verbose=self.verbose,
                            conditions=pow_in_a_condition), 0, "Power for inst event in .iaf file should be true.")

        self.assertEqual(
            runner.run_test(query_file="facts/dummy-5.iaq", fact_files=["facts/pow_in_true.iaf"], verbose=self.verbose,
                            conditions=pow_in_a_condition * 5), 0,
            "Power for inst event in .iaf file should stay true.")

    def test_iaf_fluent_obligation(self):
        runner = InstalSingleShotTestRunner(input_files=["facts/facts.ial"], bridge_file=None,
                                            domain_files=["facts/facts.idc"],
                                            fact_files=[])

        pow_in_a_condition = [
            {"holdsat": ["holdsat(obl(in_a(foo), in_b(foo), in_c(foo)),fact)"]}]

        self.assertEqual(
            runner.run_test(query_file="facts/dummy-1.iaq", fact_files=["facts/obl_true.iaf"], verbose=self.verbose,
                            conditions=pow_in_a_condition), 0, "Obligation in .iaf file should be true.")

        self.assertEqual(
            runner.run_test(query_file="facts/dummy-5.iaq", fact_files=["facts/obl_true.iaf"], verbose=self.verbose,
                            conditions=pow_in_a_condition * 5), 0,
            "Obligation from .iaf file should stay true.")
