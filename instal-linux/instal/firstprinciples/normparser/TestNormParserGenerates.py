from nose_parameterized import parameterized

from instal.firstprinciples.normparser.NormParserTestEngine import NormParserTestEngine, NORMPARSER_FALSETESTS, \
    NORMPARSER_GETTRUETESTS


NORMPARSER_GENERATES_TRUETESTS = [
    ("exogenous", "institutional"),
    ("exogenous", "violation"),
    ("institutional", "institutional"),
    ("institutional", "violation"),
    ("violation", "institutional"),
    ("violation", "violation"),
]


class NormParserTerminates(NormParserTestEngine):

    def norm_name(self):
        return "generates"

    @parameterized.expand(NORMPARSER_GETTRUETESTS(NORMPARSER_GENERATES_TRUETESTS))
    def test_initiates_true(self, *args):
        self.norm_parser_true(*args)

    @parameterized.expand(NORMPARSER_FALSETESTS(NORMPARSER_GETTRUETESTS(NORMPARSER_GENERATES_TRUETESTS)))
    def test_initiates_false(self, *args):
        self.norm_parser_false(*args)
