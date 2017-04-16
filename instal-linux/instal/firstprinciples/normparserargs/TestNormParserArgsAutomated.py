from nose_parameterized import parameterized

from instal.firstprinciples.normparserargs.NormParserArgsTestEngine import NORMPARSER_ARGDICT, NormParserArgsTestEngine


NORMPARSER_ARGS_TRUETESTS = [
    (("zero", "zero"), ("zero", "zero")),
    (("zero", "zero"), ("one", "1_a")),
    (("zero", "zero"), ("one", "1_b")),
    (("zero", "zero"), ("one", "1_c")),
    (("zero", "zero"), ("two", "2_a_b")),
    (("zero", "zero"), ("two", "2_b_a")),
    (("zero", "zero"), ("two", "2_a_c")),
    (("zero", "zero"), ("two", "2_c_a")),
    (("zero", "zero"), ("two", "2_b_a")),
    (("zero", "zero"), ("three", "3_a_a_c")),
    (("zero", "zero"), ("three", "3_a_b_c")),

    (("one", "1_a"), ("zero", "zero")),
    (("one", "1_a"), ("one", "1_a")),
    (("one", "1_a"), ("one", "1_b")),
    (("one", "1_a"), ("one", "1_c")),
    (("one", "1_a"), ("two", "2_a_b")),
    (("one", "1_a"), ("two", "2_a_c")),
    (("one", "1_a"), ("three", "3_a_a_c")),
    (("one", "1_a"), ("three", "3_a_b_c")),

    (("one", "1_b"), ("zero", "zero")),
    (("one", "1_b"), ("one", "1_a")),
    (("one", "1_b"), ("one", "1_b")),
    (("one", "1_b"), ("one", "1_c")),
    (("one", "1_b"), ("two", "2_b_a")),
    (("one", "1_b"), ("two", "2_c_a")),
    (("one", "1_b"), ("two", "2_a_c")),
    (("one", "1_b"), ("three", "3_a_a_c")),
    (("one", "1_b"), ("three", "3_a_b_c")),

    (("one", "1_c"), ("zero", "zero")),
    (("one", "1_c"), ("one", "1_a")),
    (("one", "1_c"), ("one", "1_b")),
    (("one", "1_c"), ("one", "1_c")),
    (("one", "1_c"), ("two", "2_a_b")),
    (("one", "1_c"), ("two", "2_c_a")),
    (("one", "1_c"), ("two", "2_b_a")),

    (("two", "2_a_b"), ("zero", "zero")),
    (("two", "2_a_b"), ("one", "1_a")),
    (("two", "2_a_b"), ("one", "1_c")),
    (("two", "2_a_b"), ("two", "2_a_b")),
    (("two", "2_a_b"), ("two", "2_a_c")),
    (("two", "2_a_b"), ("three", "3_a_a_c")),

    (("two", "2_a_c"), ("zero", "zero")),
    (("two", "2_a_c"), ("one", "1_a")),
    (("two", "2_a_c"), ("one", "1_b")),
    (("two", "2_a_c"), ("two", "2_a_b")),
    (("two", "2_a_c"), ("two", "2_a_c")),
    (("two", "2_a_c"), ("three", "3_a_a_c")),
    (("two", "2_a_c"), ("three", "3_a_b_c")),

    (("two", "2_c_a"), ("zero", "zero")),
    (("two", "2_c_a"), ("one", "1_c")),
    (("two", "2_c_a"), ("one", "1_b")),
    (("two", "2_c_a"), ("two", "2_c_a")),
    (("two", "2_c_a"), ("two", "2_b_a")),

    (("two", "2_b_a"), ("zero", "zero")),
    (("two", "2_b_a"), ("one", "1_b")),
    (("two", "2_b_a"), ("one", "1_c")),
    (("two", "2_b_a"), ("two", "2_b_a")),
    (("two", "2_b_a"), ("two", "2_c_a")),

    (("three", "3_a_a_c"), ("zero", "zero")),
    (("three", "3_a_a_c"), ("one", "1_a")),
    (("three", "3_a_a_c"), ("one", "1_b")),
    (("three", "3_a_a_c"), ("two", "2_a_b")),
    (("three", "3_a_a_c"), ("two", "2_a_c")),
    (("three", "3_a_a_c"), ("three", "3_a_a_c")),
    (("three", "3_a_a_c"), ("three", "3_a_b_c")),

    (("three", "3_a_b_c"), ("zero", "zero")),
    (("three", "3_a_b_c"), ("one", "1_a")),
    (("three", "3_a_b_c"), ("one", "1_b")),
    (("three", "3_a_b_c"), ("two", "2_a_c")),

    (("three", "3_a_b_c"), ("three", "3_a_a_c")),
    (("three", "3_a_b_c"), ("three", "3_a_b_c")),

]


def NORMPARSER_ARGS_ALLTESTS():
    test_list = []
    for k1, v1 in NORMPARSER_ARGDICT.items():
        for k2, v2 in NORMPARSER_ARGDICT.items():
            for lhsk in v1.keys():
                for rhsk in v2.keys():
                    test_list.append(((k1, lhsk), (k2, rhsk)))
    return test_list


def NORMPARSER_ARGS_FALSETESTS(true_tests):
    false = NORMPARSER_ARGS_ALLTESTS()
    print("Initial length " + str(len(false)))
    for t in true_tests:
        if t in false:
            false.remove(t)
        else:
            print(
                "Trying to remove thing from all cases that doesn't exist - is this okay?")
    print("Length now " + str(len(false)))
    return false


def NORMPARSER_ARGS_GETTRUETESTS():
    return NORMPARSER_ARGS_TRUETESTS


class TestNormParserArgsAutomated(NormParserArgsTestEngine):

    @parameterized.expand(NORMPARSER_ARGS_GETTRUETESTS())
    def test_args_true(self, *args):
        self.norm_parser_arg_true(*args)

    @parameterized.expand(NORMPARSER_ARGS_FALSETESTS(NORMPARSER_ARGS_GETTRUETESTS()))
    def test_argsinitiates_false(self, *args):
        self.norm_parser_arg_false(*args)
