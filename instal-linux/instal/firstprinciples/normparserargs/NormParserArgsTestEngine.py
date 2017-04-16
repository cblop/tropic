from instal.firstprinciples.TestEngine import InstalTestCase, temporary_text_file, InstalSingleShotTestRunner
from instal.instalexceptions import InstalParserArgumentError

NORMPARSER_ARGDICT = {
    "zero": {"zero": ""},
    "one": {
        "1_a": "(A)",
        "1_b": "(B)",
        "1_c": "(C)"},
    "two": {
        "2_a_a": "(A, A)",  # will never work
        "2_a_b": "(A, B)",
        "2_a_c": "(A, C)",
        "2_c_a": "(C, A)",
        "2_b_a": "(B, A)",

    },
    "three": {
        "3_a_a_a": "(A, A, A)",  # will never work
        "3_a_a_c": "(A, A, C)",
        "3_a_b_c": "(A, B, C)",
        "3_a_c_c": "(A, C, C)",  # will never work
        "3_c_c_c": "(C, C, C)"  # will never work
    }
}


def NORMPARSER_ARGS_GET(arg_descriptor):
    for k, v in NORMPARSER_ARGDICT.items():
        if arg_descriptor in v:
            return v[arg_descriptor]
    raise Exception


class NormParserArgsTestEngine(InstalTestCase):
    IAL_PRELUDE = """
    institution inst_name;
    type Alpha; % Ground with {a, b}
    type Beta; % Ground with {c}
    inst event zero;
    inst event one(Alpha);
    inst event two(Alpha, Beta);
    inst event three(Alpha, Alpha, Beta);
    """

    def get_ial_file(self, lhs, rhs):
        file_text = self.IAL_PRELUDE
        file_text += "{lhs} {norm} {rhs};".format(
            lhs=lhs, norm="generates", rhs=rhs)
        f = temporary_text_file(file_text, ".ial", delete=True)
        f.flush()
        return f

    def norm_parser_arg_true(self, *args):
        lhs_event, lhs_args = args[0]
        rhs_event, rhs_args = args[1]
        ial = self.get_ial_file(
            lhs_event + NORMPARSER_ARGS_GET(lhs_args), rhs_event + NORMPARSER_ARGS_GET(rhs_args))

        runner = InstalSingleShotTestRunner(input_files=[ial.name], bridge_file=None,
                                            domain_files=[
                                                "normparserargs/domain.idc"],
                                            fact_files=[])

        runner.run_test(query_file="normparserargs/blank.iaq", verbose=self.verbose,
                        conditions=[])

    def norm_parser_arg_false(self, *args):
        lhs_event, lhs_args = args[0]
        rhs_event, rhs_args = args[1]
        ial = self.get_ial_file(
            lhs_event + NORMPARSER_ARGS_GET(lhs_args), rhs_event + NORMPARSER_ARGS_GET(rhs_args))

        runner = InstalSingleShotTestRunner(input_files=[ial.name], bridge_file=None,
                                            domain_files=[
                                                "normparserargs/domain.idc"],
                                            fact_files=[])

        with(self.assertRaises(InstalParserArgumentError)):
            runner.run_test(query_file="normparserargs/blank.iaq", verbose=self.verbose,
                            conditions=[])
