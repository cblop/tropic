from instal.firstprinciples.TestEngine import InstalSingleShotTestRunnerFromText, InstalTestCase
from instal.instalexceptions import InstalTestNotImplemented, InstalParserError


class ConditionalTermsAnd(InstalTestCase):

    def test_and_true(self):
        inst = """
        institution conditional;
        type Alpha;
        exogenous event c(Alpha, Alpha, Alpha);
        inst event d(Alpha, Alpha, Alpha);

        c(A, B, C) generates d(A, B, C) if A == B, B == C;

        initially perm(c(A, B, C)), pow(d(A, B, C)), perm(d(A, B, C));
        """

        runner = InstalSingleShotTestRunnerFromText(
            input_files=[inst], domain_files=["conditionals/domains.idc"])

        base_condition = [{"occurred": [
            "occurred(c(foo, foo, foo), conditional)", "occurred(d(foo, foo, foo), conditional)"]}]

        runner.run_test(conditions=base_condition,
                        query_file="conditionals/c_matching.iaq")

    def test_and_false(self):
        inst = """
        institution conditional;
        type Alpha;
        exogenous event c(Alpha, Alpha, Alpha);
        inst event d(Alpha, Alpha, Alpha);

        c(A, B, C) generates d(A, B, C) if A == B, B == C;

        initially perm(c(A, B, C)), pow(d(A, B, C)), perm(d(A, B, C));
        """

        runner = InstalSingleShotTestRunnerFromText(
            input_files=[inst], domain_files=["conditionals/domains.idc"])

        base_condition = [{"occurred": ["occurred(c(foo, bar, foo), conditional)"],
                           "notoccurred": ["occurred(d(foo, bar, foo), conditional)"]}]

        runner.run_test(conditions=base_condition,
                        query_file="conditionals/c_notmatching.iaq")

    def test_and_one_unbound(self):
        inst = """
        institution conditional;
        type Alpha;
        exogenous event c(Alpha, Alpha, Alpha);
        inst event d(Alpha, Alpha, Alpha);

        c(A, B, C) generates d(A, B, C) if A == B, B == D;

        initially perm(c(A, B, C)), pow(d(A, B, C)), perm(d(A, B, C));
        """

        runner = InstalSingleShotTestRunnerFromText(
            input_files=[inst], domain_files=["conditionals/domains.idc"])

        with(self.assertRaises(InstalParserError)):
            runner.run_test(query_file="conditionals/c_notmatching.iaq")

    def test_and_both_unbound(self):
        inst = """
        institution conditional;
        type Alpha;
        exogenous event c(Alpha, Alpha, Alpha);
        inst event d(Alpha, Alpha, Alpha);

        c(A, B, C) generates d(A, B, C) if D == B, B == D;

        initially perm(c(A, B, C)), pow(d(A, B, C)), perm(d(A, B, C));
        """

        runner = InstalSingleShotTestRunnerFromText(
            input_files=[inst], domain_files=["conditionals/domains.idc"])

        with(self.assertRaises(InstalParserError)):
            runner.run_test(query_file="conditionals/c_notmatching.iaq")

    def test_and_fluent_true(self):
        inst = """
        institution conditional;
        type Alpha;
        exogenous event c(Alpha, Alpha, Alpha);
        inst event d(Alpha, Alpha, Alpha);
        fluent flu(Alpha, Alpha);

        c(A, B, C) generates d(A, B, C) if A == B, flu(A, A);

        initially perm(c(A, B, C)), pow(d(A, B, C)), perm(d(A, B, C));
        initially flu(A, A);
        """

        runner = InstalSingleShotTestRunnerFromText(
            input_files=[inst], domain_files=["conditionals/domains.idc"])

        base_condition = [{"occurred": [
            "occurred(c(foo, foo, foo), conditional)", "occurred(d(foo, foo, foo), conditional)"]}]

        runner.run_test(conditions=base_condition,
                        query_file="conditionals/c_matching.iaq")

    def test_and_fluent_false(self):
        inst = """
        institution conditional;
        type Alpha;
        exogenous event c(Alpha, Alpha, Alpha);
        inst event d(Alpha, Alpha, Alpha);
        fluent flu(Alpha, Alpha);

        c(A, B, C) generates d(A, B, C) if A == B, flu(A, A);

        initially perm(c(A, B, C)), pow(d(A, B, C)), perm(d(A, B, C));
        """

        runner = InstalSingleShotTestRunnerFromText(
            input_files=[inst], domain_files=["conditionals/domains.idc"])

        base_condition = [{"occurred": ["occurred(c(foo, foo, foo), conditional)"],
                           "notoccurred": ["occurred(d(foo, foo, foo), conditional)"]}]

        runner.run_test(conditions=base_condition,
                        query_file="conditionals/c_matching.iaq")

    def test_and_fluent_exists(self):
        inst = """
        institution conditional;
        type Alpha;
        type Beta;
        exogenous event c(Alpha, Alpha, Alpha);
        inst event d(Alpha, Alpha, Alpha);
        fluent flu1(Alpha, Alpha);
        fluent flu2(Alpha, Beta);

        c(A, B, C) generates d(A, B, C) if flu1(A, B), flu2(B, D);

        initially perm(c(A, B, C)), pow(d(A, B, C)), perm(d(A, B, C));
        initially flu1(foo, bar);
        initially flu2(bar, baz);
        """

        runner = InstalSingleShotTestRunnerFromText(
            input_files=[inst], domain_files=["conditionals/domains.idc"])

        base_condition = [{"occurred": [
            "occurred(c(foo, bar, foo), conditional)", "occurred(d(foo, bar, foo), conditional)"]}]

        runner.run_test(conditions=base_condition,
                        query_file="conditionals/c_notmatching.iaq")

    def test_and_fluent_exists_one_false(self):
        inst = """
        institution conditional;
        type Alpha;
        type Beta;
        exogenous event c(Alpha, Alpha, Alpha);
        inst event d(Alpha, Alpha, Alpha);
        fluent flu1(Alpha, Alpha);
        fluent flu2(Alpha, Beta);

        c(A, B, C) generates d(A, B, C) if flu1(A, B), flu2(B, D);

        initially perm(c(A, B, C)), pow(d(A, B, C)), perm(d(A, B, C));
        initially flu2(bar, baz);
        """

        runner = InstalSingleShotTestRunnerFromText(
            input_files=[inst], domain_files=["conditionals/domains.idc"])

        base_condition = [{"occurred": ["occurred(c(foo, bar, foo), conditional)"],
                           "notoccurred": ["occurred(d(foo, bar, foo), conditional)"]}]

        runner.run_test(conditions=base_condition,
                        query_file="conditionals/c_notmatching.iaq")

    def test_and_fluent_exists_one_false_other(self):
        inst = """
        institution conditional;
        type Alpha;
        type Beta;
        exogenous event c(Alpha, Alpha, Alpha);
        inst event d(Alpha, Alpha, Alpha);
        fluent flu1(Alpha, Alpha);
        fluent flu2(Alpha, Beta);

        c(A, B, C) generates d(A, B, C) if flu1(A, B), flu2(B, D);

        initially perm(c(A, B, C)), pow(d(A, B, C)), perm(d(A, B, C));
        initially flu1(foo, bar);
        """

        runner = InstalSingleShotTestRunnerFromText(
            input_files=[inst], domain_files=["conditionals/domains.idc"])

        base_condition = [{"occurred": ["occurred(c(foo, bar, foo), conditional)"],
                           "notoccurred": ["occurred(d(foo, bar, foo), conditional)"]}]

        runner.run_test(conditions=base_condition,
                        query_file="conditionals/c_notmatching.iaq")
