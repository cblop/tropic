from instal.firstprinciples.TestEngine import InstalTestCase, InstalCompareJSONTestCase
from instal.instalexceptions import InstalTestNotImplemented
import subprocess
import os
from instal.instalsolve import instal_solve_keyword
from instal.instalutility import temporary_text_file


class CompareJSONEngine(InstalTestCase):

    def test_compare_two_json(self):

        test_runner = InstalCompareJSONTestCase(
            self.CORRECT_JSON, self.CORRECT_JSON)

        test_runner.run_test()

    def test_compare_two_fail(self):

        test_runner = InstalCompareJSONTestCase(
            self.CORRECT_JSON, self.WRONG_JSON)

        with self.assertRaises(AssertionError):
            test_runner.run_test()

    def setUp(self):
        self.CORRECT_JSON = open("testenginetests/correct.json", "rt")
        self.WRONG_JSON = open("testenginetests/wrong.json", "rt")
