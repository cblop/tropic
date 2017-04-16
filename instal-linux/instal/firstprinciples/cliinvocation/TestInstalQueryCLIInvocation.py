from instal.firstprinciples.TestEngine import InstalTestCase
from instal.instalexceptions import InstalTestNotImplemented
import subprocess
import os
import tempfile


class QueryCLIInvocation(InstalTestCase):

    def test_query_cli_runs(self):
        return_code = subprocess.call(["../../instalquery.py", "-i", "cliinvocation/inst.ial", "-d",
                                       "cliinvocation/domain.idc", "-q", "cliinvocation/query.iaq"], stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)
        self.assertTrue(return_code == 0)

    def test_query_cli_json_out(self):
        tmpdir = tempfile.TemporaryDirectory()
        json_filename = tmpdir.name + "/out.json"
        return_code = subprocess.call(["../../instalquery.py", "-i", "cliinvocation/inst.ial", "-d",
                                       "cliinvocation/domain.idc", "-q", "cliinvocation/query.iaq", "-j", json_filename, "-n", "0", "-l", "1"], stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)
        self.assertTrue(return_code == 0)
        self.assertTrue(os.path.isfile(json_filename))
        with open(json_filename, "rt") as f:
            self.assertTrue(len(f.read()) > 0)

    def test_query_cli_json_multiple(self):
        tmpdir = tempfile.TemporaryDirectory()
        base_json_filename = tmpdir.name + "/out.json"
        return_code = subprocess.call(["../../instalquery.py", "-i", "cliinvocation/inst.ial", "-d",
                                       "cliinvocation/domain.idc", "-j", base_json_filename, "-n", "0", "-l", "2"], stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)
        self.assertTrue(return_code == 0)
        for i in range(1, 5):
            json_filename = tmpdir.name + "/{}_".format(i) + "out.json"
            self.assertTrue(os.path.isfile(json_filename))
            with open(json_filename, "rt") as f:
                self.assertTrue(len(f.read()) > 0)

    def test_query_cli_json_dir(self):
        tmpdir = tempfile.TemporaryDirectory()
        return_code = subprocess.call(["../../instalquery.py", "-i", "cliinvocation/inst.ial", "-d",
                                       "cliinvocation/domain.idc", "-j", tmpdir.name, "-n", "0", "-l", "2"], stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)
        self.assertTrue(return_code == 0)
        contents = os.listdir(tmpdir.name)
        self.assertTrue(len(contents) == 4)
