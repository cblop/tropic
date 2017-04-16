from nose_parameterized import parameterized

from instal.firstprinciples.normparser.NormParserTestEngine import NormParserTestEngine, NORMPARSER_FALSETESTS, \
    NORMPARSER_GETTRUETESTS


NORMPARSER_INITIATES_TRUETESTS = [
    ("institutional", "inertial"),
    ("institutional", "permission"),
    ("institutional", "obligation"),
    ("institutional", "power"),
    ("violation", "inertial"),
    ("violation", "permission"),
    ("violation", "obligation"),
    ("violation", "power"),
]


class NormParserInitiates(NormParserTestEngine):

    def norm_name(self):
        return "initiates"

    @parameterized.expand(NORMPARSER_GETTRUETESTS(NORMPARSER_INITIATES_TRUETESTS))
    def test_initiates_true(self, *args):
        self.norm_parser_true(*args)

    @parameterized.expand(NORMPARSER_FALSETESTS(NORMPARSER_GETTRUETESTS(NORMPARSER_INITIATES_TRUETESTS)))
    def test_initiates_false(self, *args):
        self.norm_parser_false(*args)
