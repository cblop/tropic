from instal.firstprinciples.TestEngine import InstalSingleShotTestRunner, InstalTestCase


class Permissions(InstalTestCase):

    def test_violation_exogenous(self):
        runner = InstalSingleShotTestRunner(input_files=["permissions/basic.ial"], bridge_file=None,
                                            domain_files=[
                                                "permissions/basic-domains.idc"],
                                            fact_files=["permissions/empty-fact.iaf"])

        in_a_true_condition = [{"occurred": ["occurred(viol(a), basic)"]}]

        self.assertEqual(runner.run_test(query_file="permissions/one-a.iaq", verbose=self.verbose,
                                         conditions=in_a_true_condition), 0,
                         "An exogenous event with no permission generates a violation.")

    def test_permission_exogenous(self):
        runner = InstalSingleShotTestRunner(input_files=["permissions/basic.ial"], bridge_file=None,
                                            domain_files=[
                                                "permissions/basic-domains.idc"],
                                            fact_files=["permissions/empty-fact.iaf"])

        in_a_true_condition = [{"notoccurred": ["occurred(viol(a), basic)"], "occurred": [
            "occurred(a,basic)"]}]

        self.assertEqual(
            runner.run_test(query_file="permissions/one-a.iaq", fact_files=["permissions/perm-a-fact.iaf"],
                            verbose=self.verbose,
                            conditions=in_a_true_condition), 0,
            "An exogenous event with permission generates no violation.")

    def test_violation_institutional(self):
        runner = InstalSingleShotTestRunner(input_files=["permissions/inst-perm.ial"], bridge_file=None,
                                            domain_files=[
                                                "permissions/basic-domains.idc"],
                                            fact_files=["permissions/perm-a-fact.iaf", "permissions/pow-b-fact.iaf"])

        in_a_true_condition = [{"occurred": [
            "occurred(viol(b), basic)", "occurred(b, basic)", "occurred(a, basic)"]}]

        self.assertEqual(runner.run_test(query_file="permissions/one-a.iaq", verbose=self.verbose,
                                         conditions=in_a_true_condition), 0,
                         "An institutional event with no permission generates a violation.")

    def test_permission_institutional(self):
        runner = InstalSingleShotTestRunner(input_files=["permissions/inst-perm.ial"], bridge_file=None,
                                            domain_files=[
                                                "permissions/basic-domains.idc"],
                                            fact_files=["permissions/perm-a-fact.iaf", "permissions/pow-b-fact.iaf"])

        in_a_true_condition = [
            {"notoccurred": ["occurred(viol(b), basic)"], "occurred": ["occurred(b,basic)", "occurred(a,basic)"]}]

        self.assertEqual(
            runner.run_test(query_file="permissions/one-a.iaq", fact_files=["permissions/perm-b-fact.iaf"],
                            verbose=self.verbose,
                            conditions=in_a_true_condition), 0,
            "An institutional event with permission generates no violation.")

    def test_permission_violation(self):
        # Test currently doesn't work because violation events require power to
        # happen, for some reason.
        runner = InstalSingleShotTestRunner(input_files=["permissions/viol-perm.ial"], bridge_file=None,
                                            domain_files=[
                                                "permissions/basic-domains.idc"],
                                            fact_files=["permissions/perm-a-fact.iaf"])

        condition = [{"occurred": ["occurred(b, basic)"],
                      "notoccurred": ["occurred(viol(b), basic)"],
                      "notholdsat": ["holdsat(perm(b), basic)"]}]

        self.assertEqual(
            runner.run_test(query_file="permissions/one-a.iaq", fact_files=["permissions/perm-b-fact.iaf"],
                            verbose=self.verbose,
                            conditions=condition), 0, "A violation event shouldn't need permission - shouldn't hold.")

    def test_violation_violation(self):
        runner = InstalSingleShotTestRunner(input_files=["permissions/viol-perm.ial"], bridge_file=None,
                                            domain_files=[
                                                "permissions/basic-domains.idc"],
                                            fact_files=["permissions/perm-a-fact.iaf", "permissions/perm-b-fact.iaf"])

        condition = [{"occurred": ["occurred(b, basic)"],
                      "notoccurred": ["occurred(viol(b), basic)"],
                      "notholdsat": ["holdsat(perm(b), basic)"]}]

        self.assertEqual(runner.run_test(query_file="permissions/one-a.iaq", fact_files=[], verbose=self.verbose,
                                         conditions=condition), 0,
                         "A violation event without permission shouldn't throw a violation.")
