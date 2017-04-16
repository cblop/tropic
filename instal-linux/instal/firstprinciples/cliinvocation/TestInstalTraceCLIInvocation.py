from instal.firstprinciples.TestEngine import InstalTestCase
from instal.instalexceptions import InstalTestNotImplemented
from instal.instalutility import temporary_text_file
import subprocess
import os
import tempfile


class TraceCLIInvocation(InstalTestCase):

    def test_trace_cli_runs(self):
        out_txt = temporary_text_file("", ".txt")
        return_code = subprocess.call(["../../instaltrace.py", "-x", out_txt.name,
                                       "-j", "cliinvocation/test.json"], stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)
        self.assertTrue(return_code == 0)

    def test_trace_demands_json(self):
        out_txt = temporary_text_file("", ".txt")
        return_code = subprocess.call(
            ["../../instaltrace.py", "-x", out_txt.name], stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)
        self.assertTrue(return_code != 0)

    def test_trace_text(self):
        out_txt = temporary_text_file("", ".txt")
        return_code = subprocess.call(["../../instaltrace.py", "-x", out_txt.name,
                                       "-j", "cliinvocation/test.json"], stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)
        self.assertTrue(return_code == 0)
        self.assertTrue(len(out_txt.read()) > 0)

    def test_trace_pdf(self):
        out_tex = temporary_text_file("", ".tex")
        return_code = subprocess.call(["../../instaltrace.py", "-t", out_tex.name,
                                       "-j", "cliinvocation/test.json"], stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)
        self.assertTrue(return_code == 0)
        self.assertTrue(len(out_tex.read()) > 0)

        output_dir = tempfile.TemporaryDirectory()
        return_code = subprocess.call(["pdflatex", "-output-directory", output_dir.name, "-halt-on-error", out_tex.name],
                                      stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)

        self.assertTrue(return_code == 0)

    def test_trace_gantt(self):
        out_tex = temporary_text_file("", ".tex")
        return_code = subprocess.call(["../../instaltrace.py", "-g", out_tex.name,
                                       "-j", "cliinvocation/test.json"], stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)
        self.assertTrue(return_code == 0)
        self.assertTrue(len(out_tex.read()) > 0)

        output_dir = tempfile.TemporaryDirectory()
        return_code = subprocess.call(["pdflatex", "-output-directory", output_dir.name, "-halt-on-error",  out_tex.name],
                                      stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)

        self.assertTrue(return_code == 0)

    def test_trace_dir_input_gantt(self):
        tmpdir = tempfile.TemporaryDirectory()
        return_code = subprocess.call(["../../instaltrace.py", "-g", tmpdir.name,
                                       "-j", "cliinvocation/testjson/"], stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)
        self.assertTrue(return_code == 0)
        contents = os.listdir(tmpdir.name)
        self.assertTrue(len(contents) == 2)

    def test_trace_dir_input_pdf(self):
        tmpdir = tempfile.TemporaryDirectory()
        return_code = subprocess.call(["../../instaltrace.py", "-t", tmpdir.name,
                                       "-j", "cliinvocation/testjson/"], stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)
        self.assertTrue(return_code == 0)
        contents = os.listdir(tmpdir.name)
        self.assertTrue(len(contents) == 2)

    def test_trace_dir_input_text(self):
        tmpdir = tempfile.TemporaryDirectory()
        return_code = subprocess.call(["../../instaltrace.py", "-x", tmpdir.name,
                                       "-j", "cliinvocation/testjson/"], stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)
        self.assertTrue(return_code == 0)
        contents = os.listdir(tmpdir.name)
        self.assertTrue(len(contents) == 2)

    def test_trace_multiple(self):
        out_txt = temporary_text_file("", ".txt")
        out_trace = temporary_text_file("", ".tex")
        out_gantt = temporary_text_file("", ".tex")
        return_code = subprocess.call(["../../instaltrace.py", "-x", out_txt.name,
                                       "-t", out_trace.name, "-g", out_gantt.name,
                                       "-j", "cliinvocation/test.json"], stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)
        self.assertTrue(return_code == 0)
        self.assertTrue(len(out_txt.read()) > 0)
        self.assertTrue(len(out_trace.read()) > 0)
        self.assertTrue(len(out_gantt.read()) > 0)
