#------------------------------------------------------------------------
# REVISION HISTORY:
# 20160308 JAP: created file from pystream.py.  changed verbose to allow
#               levels

from __future__ import print_function
from gringo import Control, Model, Fun, parse_term

class Sensor:
    def __init__(self, initially, files, args):
        self.last_initially = initially
        self.last_solution = None
        self.cycle = 0
        self.args = args
        self.undo_external = []
        self.horizon = 1
        self.ctl = Control(['-c', 'horizon={0}'.format(self.horizon)])
        for x in files:
            # print("loading ",x)
            self.ctl.load(x)
        self.ctl.ground([("base", [])])

    def print_universe(self):
        print("universe:", len(self.ctl.domains))
        for x in self.ctl.domains:
            print(x.atom, x.is_fact, x.is_external)

    def solve(self, event):
        for x in self.undo_external:
            if self.args.verbose>=1:
                print("unassign",x)
            self.ctl.assign_external(x, False)
        self.undo_external = []
        if self.args.verbose>=1:
            print(self.cycle,"----------------------------------------")
        for x in self.last_initially + [event]:
            if self.args.verbose>=1:
                print("assign",x)
            self.ctl.assign_external(x, True)
            self.undo_external.append(x)
        self.last_solution = None
        if self.args.verbose>=1:
            print(self.cycle,"----------------------------------------")
        self.ctl.solve(on_model=self.on_model)
        # self.print_universe()
        return self.last_solution

    def on_model(self, model):
        self.last_solution = model.atoms()
        self.last_initially = []
        for atom in model.atoms(Model.ATOMS):
            if ((atom.name()=="holdsat") and len(atom.args()) == 3 and atom.args()[2] == 1):
                print(atom.name()+'('+','.join(str(x) for x in atom.args())+')')
                self.last_initially.append(Fun(atom.name(), atom.args()[:-1]))
