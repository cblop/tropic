import os
from abc import ABCMeta

from instal.instalutility import temporary_text_file


class InstalCompilerWrapper(metaclass=ABCMeta):
    """
        InstalCompilerWrapper
        See __init__.py for more details.
    """

    def __init__(self):
        pass

    def compile(self, instal_dictionary: dict, save_output_file: str = "/tmp/") -> dict:
        """
        This method strings together compile_ial and compile_bridge - allows subclasses to just deal with them.
        """
        instal_compiled_dictionary = {"institution_asp": [], "bridge_asp": []}
        for i in instal_dictionary["institution_ir"]:
            asp = self.compile_ial(i["contents"])
            if save_output_file == "/tmp/":
                i["filename"] = None
            file = self.lp_file(save_output_file, asp, filename=i["filename"])
            instal_compiled_dictionary["institution_asp"].append(
                {"file": file, "contents": asp})

        for b in instal_dictionary["bridge_ir"]:
            asp = self.compile_bridge(
                b["contents"], instal_dictionary["institution_ir"])
            if save_output_file == "/tmp/":
                b["filename"] = None
            file = self.lp_file(save_output_file, asp, filename=b["filename"])
            instal_compiled_dictionary["bridge_asp"].append(
                {"file": file, "contents": asp})

        return instal_compiled_dictionary

    def compile_ial(self, ial_ast: dict) -> str:
        """

        input: an ast produced by the instal parser
        output: compiled ASP for that institution
        """
        raise NotImplementedError

    def compile_bridge(self, bridge_ast: dict, ial_ast: dict) -> str:
        """
        input: an ast produced by the instal bridge parser
        output: compiled ASP for that bridge
        """
        raise NotImplementedError

    def lp_file(self, directory: str, contents: str, filename: str=None):
        """
            Writes ASP to file.
        """
        if filename is None:
            f = temporary_text_file(
                contents, file_extension=".lp", delete=True)
            return f
        new_file = os.path.basename(filename).replace(
            ".ial", ".lp").replace(
            ".iab", ".lp")
        new_file = directory + new_file
        f = open(new_file, "wt")
        f.write(contents)
        return f
