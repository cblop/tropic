from instal.firstprinciples.TestEngine import InstalSingleShotTestRunnerFromText, InstalTestCase
from instal.instalexceptions import InstalTestNotImplemented, InstalParserError


class ConditionalTermsNot(InstalTestCase):

    def test_not_true(self):
        inst = """
        institution conditional;
        type Alpha;
        exogenous event a(Alpha, Alpha);
        inst event b(Alpha, Alpha);

        a(A, B) generates b(A, B) if not A != B;

        initially perm(a(A, B)), pow(b(A, B)), perm(b(A, B));
        """

        runner = InstalSingleShotTestRunnerFromText(
            input_files=[inst], domain_files=["conditionals/domains.idc"])

        base_condition = [{"occurred": [
            "occurred(a(foo, foo), conditional)", "occurred(b(foo, foo), conditional)"]}]

        runner.run_test(conditions=base_condition,
                        query_file="conditionals/a_matching.iaq")

    def test_not_false(self):
        inst = """
        institution conditional;
        type Alpha;
        exogenous event a(Alpha, Alpha);
        inst event b(Alpha, Alpha);

        a(A, B) generates b(A, B) if not A != B;

        initially perm(a(A, B)), pow(b(A, B)), perm(b(A, B));
        """

        runner = InstalSingleShotTestRunnerFromText(
            input_files=[inst], domain_files=["conditionals/domains.idc"])

        base_condition = [{"occurred": ["occurred(a(foo, bar), conditional)"],
                           "notoccurred": ["occurred(b(foo, bar), conditional)"]}]

        runner.run_test(conditions=base_condition,
                        query_file="conditionals/a_notmatching.iaq")

    def test_not_unbound(self):
        inst = """
        institution conditional;
        type Alpha;
        exogenous event a(Alpha, Alpha);
        inst event b(Alpha, Alpha);

        a(A, B) generates b(A, B) if not A == C;

        initially perm(a(A, B)), pow(b(A, B)), perm(b(A, B));
        """

        runner = InstalSingleShotTestRunnerFromText(
            input_files=[inst], domain_files=["conditionals/domains.idc"])

        with self.assertRaises(InstalParserError):
            runner.run_test(query_file="conditionals/a_notmatching.iaq")

    def test_not_fluent_true(self):
        inst = """
        institution conditional;
        type Alpha;
        exogenous event a(Alpha, Alpha);
        inst event b(Alpha, Alpha);
        fluent flu(Alpha, Alpha);

        a(A, B) generates b(A, B) if not flu(A, B);

        initially perm(a(A, B)), pow(b(A, B)), perm(b(A, B));
        """

        runner = InstalSingleShotTestRunnerFromText(
            input_files=[inst], domain_files=["conditionals/domains.idc"])

        base_condition = [{"occurred": [
            "occurred(a(foo, foo), conditional)", "occurred(b(foo, foo), conditional)"]}]

        runner.run_test(conditions=base_condition,
                        query_file="conditionals/a_matching.iaq")

    def test_not_fluent_false(self):
        inst = """
        institution conditional;
        type Alpha;
        exogenous event a(Alpha, Alpha);
        inst event b(Alpha, Alpha);
        fluent flu(Alpha, Alpha);

        a(A, B) generates b(A, B) if not flu(A, B);

        initially perm(a(A, B)), pow(b(A, B)), perm(b(A, B));
        initially flu(A, B);
        """

        runner = InstalSingleShotTestRunnerFromText(
            input_files=[inst], domain_files=["conditionals/domains.idc"])

        base_condition = [{"occurred": ["occurred(a(foo, foo), conditional)"],
                           "notoccurred": ["occurred(b(foo, foo), conditional)"]}]

        runner.run_test(conditions=base_condition,
                        query_file="conditionals/a_matching.iaq")

    def test_not_fluent_undeclared(self):
        inst = """
        institution conditional;
        type Alpha;
        exogenous event a(Alpha, Alpha);
        inst event b(Alpha, Alpha);
        fluent flu(Alpha, Alpha);

        a(A, B) generates b(A, B) if not flu2(A, B);

        initially perm(a(A, B)), pow(b(A, B)), perm(b(A, B));
        """

        runner = InstalSingleShotTestRunnerFromText(
            input_files=[inst], domain_files=["conditionals/domains.idc"])

        with self.assertRaises(InstalParserError):
            runner.run_test(query_file="conditionals/a_notmatching.iaq")
