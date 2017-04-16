from unittest import TestCase

from instal import instalsolve, instalquery, instaltrace
from instal.instaljsonhelpers import json_check_conditions, trace_dicts_from_file
from instal.instalutility import temporary_text_file
from abc import ABCMeta
# TODO: Deal with verbose levels properly.


class InstalTestRunner(metaclass=ABCMeta):
    """
        InstalTestRunner
        ABC for instal solve/query test cases.
        input_files, bridge_file, domain_files, fact_files are all lists of filenames.
    """

    def __init__(self, input_files: list=None, bridge_file: list=None, domain_files: list=None, fact_files: list=None):
        if not input_files:
            input_files = []
        if not domain_files:
            domain_files = []
        if not fact_files:
            fact_files = []
        self.original_input_files = input_files
        self.bridge_file = bridge_file
        self.domain_files = domain_files
        self.fact_files = fact_files

        if self.bridge_file is None:
            self.bridge_file = []

        if not isinstance(self.bridge_file, list):
            self.bridge_file = [self.bridge_file]

        if len(self.bridge_file) > 1:
            # TODO: Deal with multiple bridges. Need a test for it too.
            raise NotImplementedError
        self.input_files = []
        for i in self.original_input_files:
            if hasattr(i, "name"):
                self.input_files.append(i.name)
            else:
                self.input_files.append(i)

        self.verbose = 2

    def run_test(self, query_file: str, conditions: list=None, fact_files: list=None, verbose: int=None) -> int:
        pass


class InstalSingleShotTestRunner(InstalTestRunner):
    """
        InstalSingleShotTestRunner
        Implementation of InstalTestRunner for basic single shot solves of InstAL.
        Asserts that the output fits a certain set of conditions.
        (If conditions aren't passed, it doesn't do the comparison - but does run the program.)
        (This can be useful if you're expecting an error in the IAL you need to catch, for instance.)
    """

    def run_test(self, query_file, conditions=None, fact_files=None, verbose=None):
        if not verbose:
            verbose = self.verbose
        if not conditions:
            conditions = []
        if not fact_files:
            fact_files = []
        facts = fact_files + self.fact_files
        json_out = temporary_text_file("", file_extension="out.json")
        instalsolve.instal_solve_keyword(input_files=self.input_files,
                                         bridge_file=(self.bridge_file[0] if len(
                                             self.bridge_file) > 0 else None),
                                         domain_files=self.domain_files, fact_files=facts, json_file=json_out.name,
                                         query=query_file)

        if conditions:
            trace = trace_dicts_from_file(json_out.name)
            errors = json_check_conditions(trace, conditions, verbose=verbose)
            assert errors == 0
            return 0
        return 0


class InstalSingleShotTestRunnerFromText(InstalSingleShotTestRunner):
    """
        InstalSingleShotTestRunnerFromText
        Convenience wrapper for InstalSingleShotTestRunner.

        input_files and bridge_file should be a list of strings of ial files.
    """

    def __init__(self, input_files: list=None, bridge_file: list=None, domain_files: list=None, fact_files: list=None):
        if not input_files:
            input_files = []
        if not domain_files:
            domain_files = []
        if not fact_files:
            fact_files = []
        self.new_input_files = []
        for i in input_files:
            newfile = temporary_text_file(
                i, file_extension=".ial", delete=True)
            newfile.flush()
            self.new_input_files.append(newfile)

        self.new_bridge_file = []
        if bridge_file:
            for b in bridge_file:
                newfile = temporary_text_file(
                    b, file_extension=".iab", delete=True)
                newfile.flush()
                self.new_bridge_file.append(newfile)
        super(InstalSingleShotTestRunnerFromText, self).__init__(input_files=[n.name for n in self.new_input_files],
                                                                 bridge_file=[
                                                                     n.name for n in self.new_bridge_file],
                                                                 domain_files=domain_files, fact_files=fact_files)


class InstalMultiShotTestRunner(InstalTestRunner):
    """
        InstalMultiShotTestRunner
        Implementation of InstalTestRunner for basic single shot solves of InstAL

        Note the additional parameters: -l (length), -n (n_answersets)
        Conditions at present doesn't do anything.
        expected_answersets asserts that the # of answersets produced is a certain value.

    """

    def run_test(self, query_file=None, conditions=None, fact_files=None, verbose=0, length=1, n_answersets=0,
                 expected_answersets=0):
        if not conditions:
            conditions = []
        if not fact_files:
            fact_files = []
        facts = fact_files + self.fact_files

        answersets = instalquery.instal_query_keyword(input_files=self.input_files,
                                                      bridge_file=(
                                                          self.bridge_file[0] if len(self.bridge_file) > 0 else None),
                                                      domain_files=self.domain_files, fact_files=facts,
                                                      query=query_file, length=length, number=n_answersets)
        print("Expected answersets: {}. Got: {}".format(
            expected_answersets, len(answersets)))
        assert(expected_answersets == len(answersets))
        return 0  # unexpected


class InstalCompareJSONTestCase(object):
    """
        InstalCompareJSONTestCase
        Given two .json files, assert that they are the identical.
    """

    def __init__(self, file1, file2):
        self.file1 = file1
        self.file2 = file2

    def run_test(self):
        text_out_1 = temporary_text_file("", ".json")
        text_out_2 = temporary_text_file("", ".json")

        instaltrace.instal_trace_keyword(
            text_file=text_out_1.name, json_file=self.file1.name)
        instaltrace.instal_trace_keyword(
            text_file=text_out_2.name, json_file=self.file2.name)

        text_out_1.seek(0)
        text_out_2.seek(0)
        out_1 = text_out_1.read()
        out_2 = text_out_2.read()

        print(out_1)
        print(out_2)
        assert(out_1 == out_2)
        return out_1, out_2


class InstalCompareQuerySolve(object):
    """
        InstalCompareQuerySolve
        A convenience test wrapper that checks the output from a solve call is the same as the output from a query call.
    """

    def __init__(self, input_files=None, bridge_file=None, domain_files=None, fact_files=None, query="", length=1,
                 number=1):
        if not domain_files:
            domain_files = []
        if not input_files:
            input_files = []
        if not fact_files:
            fact_files = []
        self.input_files = input_files
        self.bridge_file = bridge_file
        self.domain_files = domain_files
        self.fact_files = fact_files
        self.query = query
        self.length = length
        self.number = number

    def run_test(self):
        json_out_query = temporary_text_file("", file_extension=".json")
        json_out_solve = temporary_text_file("", file_extension=".json")

        instalquery.instal_query_keyword(input_files=self.input_files,
                                         bridge_file=self.bridge_file,
                                         domain_files=self.domain_files, fact_files=self.fact_files,
                                         query=self.query, length=self.length, number=1,
                                         json_file=json_out_query.name)

        instalsolve.instal_solve_keyword(input_files=self.input_files,
                                         bridge_file=self.bridge_file,
                                         domain_files=self.domain_files, fact_files=self.fact_files,
                                         query=self.query,
                                         json_file=json_out_solve.name)

        json_test = InstalCompareJSONTestCase(json_out_solve, json_out_query)
        solve_text, query_text = json_test.run_test()
        return solve_text, query_text


class InstalTestCase(TestCase):
    """
        InstalTestCase
        Base class for all tests.
    """
    verbose = 1
