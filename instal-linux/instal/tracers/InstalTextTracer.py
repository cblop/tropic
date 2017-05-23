

import sys

from .InstalTracer import InstalTracer
from instal.instaljsonhelpers import json_dict_to_string


class InstalTextTracer(InstalTracer):
    """
        InstalTextTracer
        Implementation of ABC InstalTracer for text output.
        Will produce same output as instalsolve's verbose=1 option.
    """

    def trace_to_file(self):
        start = 0 if self.zeroth_term else 1
        f = None
        if self.output_file_name == "-":
            f = sys.stdout
        with open(self.output_file_name, 'w') if not f else f as tfile:
            timestep = 0
            print("Answer Set " + str(self.trace[0]["metadata"]["answer_set_n"]) + ":\n", file=tfile)
            for i in range(start, len(self.trace)):
                timestep += 1
                t = self.trace[i]
                print("Time Step " + str(timestep) + ":\n", file=tfile)
                print(json_dict_to_string(t) + "\n", file=tfile)
