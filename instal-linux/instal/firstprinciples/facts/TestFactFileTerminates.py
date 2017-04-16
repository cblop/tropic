#!/usr/bin/python3
from instal.firstprinciples.TestEngine import InstalSingleShotTestRunner, InstalTestCase


class FactFileTerminates(InstalTestCase):

    def test_iaf_kill_fluent(self):
        runner = InstalSingleShotTestRunner(input_files=["facts/fact_kill.ial"], bridge_file=None,
                                            domain_files=["facts/facts.idc"], fact_files=[])

        in_fact_holdsat_condition = [{"holdsat": ["holdsat(in_fact(foo),fact)"]}] + [{"notholdsat": [
            "holdsat(in_fact(foo),fact)"]}] * 2
        self.assertEqual(runner.run_test(query_file="facts/kill_event.iaq", fact_files=["facts/fluent_true.iaf"],
                                         verbose=self.verbose,
                                         conditions=in_fact_holdsat_condition), 0, "Kill fluent in iaf.")

    def test_iaf_kill_perm_institutional(self):
        runner = InstalSingleShotTestRunner(input_files=["facts/fact_kill.ial"], bridge_file=None,
                                            domain_files=["facts/facts.idc"], fact_files=[])

        in_fact_holdsat_condition = [{"holdsat": ["holdsat(perm(ex_a(foo)),fact)"]}] + [{"notholdsat": [
            "holdsat(perm(ex_a(foo)),fact)"]}] * 2
        self.assertEqual(runner.run_test(query_file="facts/kill_event.iaq", fact_files=["facts/perm_ex_true.iaf"],
                                         verbose=self.verbose,
                                         conditions=in_fact_holdsat_condition), 0, "Kill perm (in) in iaf.")

    def test_iaf_kill_perm_exogenous(self):
        runner = InstalSingleShotTestRunner(input_files=["facts/fact_kill.ial"], bridge_file=None,
                                            domain_files=["facts/facts.idc"], fact_files=[])

        in_fact_holdsat_condition = [{"holdsat": ["holdsat(perm(in_a(foo)),fact)"]}] + [{"notholdsat": [
            "holdsat(perm(in_a(foo)),fact)"]}] * 2
        self.assertEqual(runner.run_test(query_file="facts/kill_event.iaq", fact_files=["facts/perm_in_true.iaf"],
                                         verbose=self.verbose,
                                         conditions=in_fact_holdsat_condition), 0, "Kill perm (ex) in iaf.")

    def test_iaf_kill_pow_institutional(self):
        runner = InstalSingleShotTestRunner(input_files=["facts/fact_kill.ial"], bridge_file=None,
                                            domain_files=["facts/facts.idc"], fact_files=[])

        in_fact_holdsat_condition = [{"holdsat": ["holdsat(pow(in_a(foo)),fact)"]}] + [{"notholdsat": [
            "holdsat(pow(in_a(foo)),fact)"]}] * 2
        self.assertEqual(runner.run_test(query_file="facts/kill_event.iaq", fact_files=["facts/pow_in_true.iaf"],
                                         verbose=self.verbose,
                                         conditions=in_fact_holdsat_condition), 0, "Kill pow (in) in iaf.")

    def test_iaf_kill_obligation(self):
        runner = InstalSingleShotTestRunner(input_files=["facts/fact_kill.ial"], bridge_file=None,
                                            domain_files=["facts/facts.idc"], fact_files=[])

        in_fact_holdsat_condition = [{"holdsat": ["holdsat(obl(in_a(foo), in_b(foo), in_c(foo)),fact)"]}] + [{
            "notholdsat": [
                "holdsat(obl(in_a(foo), in_b(foo), in_c(foo)),fact)"]}] * 2
        self.assertEqual(
            runner.run_test(query_file="facts/kill_event.iaq", fact_files=["facts/obl_true.iaf"], verbose=self.verbose,
                            conditions=in_fact_holdsat_condition), 0, "Kill obl in iaf.")
