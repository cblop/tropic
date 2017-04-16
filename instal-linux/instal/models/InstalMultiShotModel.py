import time

from io import StringIO
import os

from .InstalModel import InstalModel
from .Oracle import Oracle
from instal.clingo import Function, parse_term
from instal.instaljsonhelpers import state_dict_from_lists
from instal.instalexceptions import InstalRuntimeError


class InstalMultiShotModel(InstalModel):
    """
        InstalMultiShotModel
        Deals with multi shot solving - instance of InstalModel.
        Used for instalquery.
    """

    def __init__(self, instal_args):
        super(InstalMultiShotModel, self).__init__(instal_args)
        self.timestamp = 0
        self.oracle = Oracle(self.initial_facts,
                             self.model_files, self.domain_facts, instal_args)

    def solve(self, query_text=""):
        self.timestamp = time.time()
        observed = []
        queryIO = StringIO(query_text)
        for i, e in enumerate(queryIO):
            observed += [Function('observed', [parse_term(e).arguments[0], i]),
                         Function('_eventSet', [i])]
        # note: events is a list of Fun not strings
        self.oracle.solve(observed)
        of = len(self.oracle.answersets)
        if of == 0:
            raise InstalRuntimeError(
                "Solver produced 0 answer sets. This usually means:\n"
                "- You have included additional .lp files with constraints in them."
                "- You have forgotten to ground types that exist in your institutions.")
        for n, triplestatelist in self.oracle.answersets.items():
            zeroth = {"metadata": self.generate_json_metadata(n + 1, of, 0), "state": {"observed": [],
                                                                                       "occurred": [],
                                                                                       "holdsat": self.initial_facts}}
            aset = [zeroth]
            for timestep in range(1, self.instal_args.length + 1):
                timestepdict = state_dict_from_lists(triplestatelist[0][timestep], triplestatelist[1][timestep],
                                                     triplestatelist[2][timestep])
                timestepdict["metadata"] = self.generate_json_metadata(
                    n + 1, of, timestep)
                aset.append(timestepdict)
            self.answersets.append(aset)

        self.check_and_output_json()

    def generate_json_metadata(self, n, of, timestep):
        metadata = {
            "pid": os.getpid(),
            "source_files": self.instal_args.input_files + self.instal_args.domain_files,
            "timestamp": self.timestamp,
            "timestep": timestep,
            "mode": "multi_shot",
            "answer_set_n": n,
            "answer_set_of": of,
        }
        return metadata
