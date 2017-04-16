from instal.firstprinciples.TestEngine import InstalTestCase, InstalCompareJSONTestCase
from instal.instalexceptions import InstalTestNotImplemented
import subprocess
import os
from instal.instalsolve import instal_solve_keyword
from instal.instalutility import temporary_text_file
import tempfile


class SolveCLIInvocation(InstalTestCase):

    def test_solve_cli_runs(self):
        return_code = subprocess.call(["../../instalsolve.py", "-i", "cliinvocation/inst.ial", "-d",
                                       "cliinvocation/domain.idc", "-q", "cliinvocation/query.iaq"], stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)
        self.assertTrue(return_code == 0)

    def test_solve_cli_json_out(self):
        out_txt = temporary_text_file("", ".json")
        return_code = subprocess.call(["../../instalsolve.py", "-i", "cliinvocation/inst.ial", "-d", "cliinvocation/domain.idc",
                                       "-q", "cliinvocation/query.iaq", "-j", out_txt.name], stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)
        self.assertTrue(return_code == 0)
        self.assertTrue(len(out_txt.read()) > 0)

    def test_solve_cli_json_dir(self):
        out_dir = tempfile.TemporaryDirectory()
        return_code = subprocess.call(["../../instalsolve.py", "-i", "cliinvocation/inst.ial", "-d", "cliinvocation/domain.idc",
                                       "-q", "cliinvocation/query.iaq", "-j", out_dir.name], stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)

        self.assertTrue(return_code == 0)
        contents = os.listdir(out_dir.name)
        self.assertTrue(len(contents) == 1)

    def test_solve_invalid_ial(self):
        return_code = subprocess.call(["../../instalsolve.py", "-i", "cliinvocation/invalid.ial", "-d",
                                       "cliinvocation/domain.idc", "-q", "cliinvocation/query.iaq"], stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)
        self.assertTrue(return_code != 0)

    def test_solve_cli_compare_to_keyword(self):
        out_1_json = temporary_text_file("", ".json")
        out_2_json = temporary_text_file("", ".json")

        return_code = subprocess.call(["../../instalsolve.py", "-i", "cliinvocation/inst.ial", "-d", "cliinvocation/domain.idc",
                                       "-q", "cliinvocation/query.iaq", "-j", out_1_json.name], stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)
        self.assertTrue(return_code == 0)

        instal_solve_keyword(input_files=["cliinvocation/inst.ial"], domain_files=[
                             "cliinvocation/domain.idc"], query="cliinvocation/query.iaq", json_file=out_2_json.name)

        test_runner = InstalCompareJSONTestCase(out_1_json, out_2_json)

        test_runner.run_test()
