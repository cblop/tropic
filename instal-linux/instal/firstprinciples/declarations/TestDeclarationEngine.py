from instal.firstprinciples.TestEngine import InstalTestCase, InstalSingleShotTestRunnerFromText
from instal.instalexceptions import InstalParserArgumentError, InstalParserError
from nose_parameterized import parameterized
from itertools import permutations
import random

#'["inevents", "exevents", "vievents", "fluents",
#                                "noninertial_fluents"]

ARGLIST_POSSIBILITIES = [
    [],
    ["Alpha"],
    ["Beta"],
    ["Alpha", "Alpha"],
    ["Alpha", "Beta"],
    ["Beta", "Alpha"],
    ["Beta", "Beta"]
]

TYPE_POSSIBILITIES = ["inevents", "exevents",
                      "vievents", "fluents", "noninertial_fluents"]

NAME_POSSIBILITIES = ["a", "b"]


def GENERATE_DECLARATION_TEST_CASES(number_cases=400):

    possibilities = []
    for a in ARGLIST_POSSIBILITIES:
        for t in TYPE_POSSIBILITIES:
            for n in NAME_POSSIBILITIES:
                possibilities.append((t, n, a))

    testcases = permutations(possibilities, r=2)
    return random.sample(list(testcases), number_cases)


DECLARATION_TEST_CASES = GENERATE_DECLARATION_TEST_CASES()


class DeclarationEngine(InstalTestCase):
    IAL_PRELUDE = """
    institution inst_name;
    type Alpha;

    """

    def get_declaration(self, instaltype, name, arglist):
        def argpart(args):
            rV = ""
            if len(args) == 0:
                return ""
            first = True
            for a in args:
                if first:
                    rV += a
                    first = False
                else:
                    rV += ",{}".format(a)
            return "({})".format(rV)

        def get_boilerplate(instaltype):
            if instaltype == "inevents":
                return "inst event"
            if instaltype == "exevents":
                return "exogenous event"
            if instaltype == "vievents":
                return "violation event"
            if instaltype == "fluents":
                return "fluent"
            if instaltype == "noninertial_fluents":
                return "noninertial fluent"
            raise NotImplementedError
        return "{} {}{};\n".format(get_boilerplate(instaltype), name, argpart(arglist))

    def declaration_tes(self, *args):
        if not len(args) == 2:
            raise Exception
        type1, name1, args1 = args[0]
        type2, name2, args2 = args[1]

        fail = False

        if name1 == name2:
            fail = True
            print("Name the same")

        if "Beta" in args1:
            fail = True
            print("Beta in args1")

        if "Beta" in args2:
            fail = True
            print("Beta in args2")

        ial = self.IAL_PRELUDE
        ial += self.get_declaration(type1, name1, args1)
        ial += self.get_declaration(type2, name2, args2)

        print(ial)

        runner = InstalSingleShotTestRunnerFromText(
            input_files=[ial], domain_files=["declarations/domains.idc"])

        if fail:
            with self.assertRaises(InstalParserError):
                runner.run_test(query_file="declarations/blank.iaq")
        else:
            runner.run_test(query_file="declarations/blank.iaq")


class TestDeclarationAutomated(DeclarationEngine):

    @parameterized.expand(DECLARATION_TEST_CASES)
    def test_declarations(self, *args):
        self.declaration_tes(*args)
