from nose_parameterized import parameterized

from instal.firstprinciples.normparser.NormParserTestEngine import NormParserTestEngine, NORMPARSER_FALSETESTS, \
    NORMPARSER_GETTRUETESTS


NORMPARSER_WHEN_TRUETESTS = [
    ("noninertial", "inertial"),
    ("noninertial", "noninertial"),
    ("noninertial", "permission"),
    ("noninertial", "power"),
    ("noninertial", "obligation"),
]


class NormParserWHEN(NormParserTestEngine):

    def norm_name(self):
        return "when"

    @parameterized.expand(NORMPARSER_GETTRUETESTS(NORMPARSER_WHEN_TRUETESTS))
    def test_initiates_true(self, *args):
        self.norm_parser_true(*args)

    @parameterized.expand(NORMPARSER_FALSETESTS(NORMPARSER_GETTRUETESTS(NORMPARSER_WHEN_TRUETESTS)))
    def test_initiates_false(self, *args):
        self.norm_parser_false(*args)
