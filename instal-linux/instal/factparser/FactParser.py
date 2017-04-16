import os
from io import StringIO

# noinspection PyUnresolvedReferences
from instal.clingo import parse_term
from instal.instaljsonhelpers import dict_funs_to_list, trace_dicts_from_file
from instal.instalexceptions import InstalCompileError


class FactParser(object):
    """
        FactParser
        See __init__.py for more details.
    """

    def __init__(self):
        pass

    def get_facts(self, fact_filenames: list) -> list:
        """
        input: a set of fact filenames
        output: a list of Function objects that are true at the first timestep
        """
        initlist = []
        for f in fact_filenames:
            name, ext = os.path.splitext(f)
            with open(f, "rt") as factfile:
                if ext == ".iaf":
                    initlist += self.parse_iaf_factfile(factfile.read())
                if ext == ".json":
                    initlist += self.parse_json_factfile(factfile)

        return initlist

    def parse_json_factfile(self, json_file: "File") -> list:
        """
        input: a json file
        output: a list of the facts true in the *last* step in that json file.
        (This allows restarting from an old trace.)
        """
        jsons = trace_dicts_from_file(json_file)
        if len(jsons) == 0:
            return []
        return dict_funs_to_list(jsons[-1], keys=["holdsat"])

    def parse_iaf_factfile(self, iaf_text: str) -> list:
        """
        input: an iaf text (as a string)
        output: a list of the facts
        """
        initlist = []
        iafIO = StringIO(iaf_text)
        for init in iafIO.readlines():
            init = init.rstrip()
            if init == '':
                continue
            term = parse_term(init)
            if term.name in ["initially"]:
                where = term.arguments[1]
                what = term.arguments[0]
                initlist = [
                    "holdsat(" + str(what) + "," + str(where) + ")"] + initlist
            else:
                raise InstalCompileError(
                    ".iaf file should be in the format initially({holdsat}, {institution})")
        return map(parse_term, initlist)
