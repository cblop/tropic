#!/usr/bin/python3
from instal.firstprinciples.TestEngine import InstalTestCase, temporary_text_file, InstalSingleShotTestRunner
from instal.instalexceptions import InstalParserError

NORMPARSER_TYPE_DICTIONARY = {
    "institution": ["inst_name", "inst_name"],
    "type": ["Alpha", "Beta"],
    "exogenous": ["ex_a", "ex_b"],
    "institutional": ["in_a", "in_b"],
    "violation": ["vi_a", "vi_b"],
    "inertial": ["flu_a", "flu_b"],
    "noninertial": ["nif_a", "nif_b"],
    "permission": ["perm(ex_no)", "perm(in_no)"],
    "power": ["pow(in_no)", "pow(in_no2)"],
    "obligation": ["obl(in_a, in_b, in_no)", "obl(in_a, in_b, in_no2)"],
    "undeclared": ["rshrsriuhrg", "seheuhruhe"],
    "undeclared_uppercase": ["Afeiurhfu", "Bfruirhur"]

}


def NORMPARSER_ALLTESTS():
    tuple_list = []
    for k1, v1 in NORMPARSER_TYPE_DICTIONARY.items():
        for k2, v2 in NORMPARSER_TYPE_DICTIONARY.items():
            tuple_list.append(((k1, k2), v1[0], v2[1]))
    return tuple_list


def NORMPARSER_FALSETESTS(true_tests):
    false = NORMPARSER_ALLTESTS()
    print("Initial length " + str(len(false)))
    for t in true_tests:
        if t in false:
            false.remove(t)
        else:
            print(
                "Trying to remove thing from all cases that doesn't exist - is this okay?")
    print("Length now " + str(len(false)))
    return false


def NORMPARSER_GETTRUETESTS(true_tests_unrefined):
    retVal = []
    for t in true_tests_unrefined:
        retVal.append(((t[0], t[1]), NORMPARSER_TYPE_DICTIONARY[
                      t[0]][0], NORMPARSER_TYPE_DICTIONARY[t[1]][1]))
    return retVal


class NormParserTestEngine(InstalTestCase):
    # Just for non-bridge tests. Extend this for bridge tests.
    IAL_PRELUDE = """
        institution inst_name;
        type Alpha;
        type Beta;
        exogenous event ex_a;
        exogenous event ex_b;
        exogenous event ex_no;
        inst event in_a;
        inst event in_b;
        inst event in_no;
        inst event in_no2;
        violation event vi_a;
        violation event vi_b;
        fluent flu_a;
        fluent flu_b;
        noninertial fluent nif_a;
        noninertial fluent nif_b;
        obligation fluent obl(in_a, in_b, in_no);
        obligation fluent obl(in_a, in_b, in_no2);
        """

    def norm_name(self):
        raise NotImplementedError

    def get_ial_file(self, lhs, rhs):
        file_text = self.IAL_PRELUDE
        file_text += "{lhs} {norm} {rhs};".format(
            lhs=lhs, norm=self.norm_name(), rhs=rhs)
        f = temporary_text_file(file_text, ".ial", delete=True)
        f.flush()
        return f

    def norm_parser_true(self, *args):
        lhs = args[1]
        rhs = args[2]
        types = args[0]
        ial = self.get_ial_file(lhs, rhs)

        runner = InstalSingleShotTestRunner(input_files=[ial.name], bridge_file=None,
                                            domain_files=[
                                                "normparser/blank.idc"],
                                            fact_files=[])

        self.assertEqual(runner.run_test(query_file="normparser/blank.iaq", verbose=self.verbose,
                                         conditions=[]), 0,
                         "Norm parser test: {lhs_type} {norm} {rhs_type} (should work)".format(lhs_type=types[0],
                                                                                               norm=self.norm_name(),
                                                                                               rhs_type=types[1]))

    def norm_parser_false(self, *args):
        lhs = args[1]
        rhs = args[2]
        types = args[0]
        ial = self.get_ial_file(lhs, rhs)
        runner = InstalSingleShotTestRunner(input_files=[ial.name], bridge_file=None,
                                            domain_files=[
                                                "normparser/blank.idc"],
                                            fact_files=[])

        with self.assertRaises(InstalParserError):
            print("Norm parser test: {lhs_type} {norm} {rhs_type} (shouldn't work)".format(lhs_type=types[0],
                                                                                           norm=self.norm_name(),
                                                                                           rhs_type=types[1]))
            runner.run_test(query_file="normparser/blank.iaq", verbose=self.verbose,
                            conditions=[])
            # "Norm parser test: {lhs_type} {norm} {rhs_type} (shouldn't work)".format(lhs_type=types[0],norm=self.norm_name(),rhs_type=types[1]))
