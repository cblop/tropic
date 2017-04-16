from instal.clingo import Control, Function, parse_term

from instal.instaljsonhelpers import model_atoms_to_lists, state_dict_from_lists, state_to_string
from instal.models.ClingoWrapper import ClingoWrapper

from instal.instalexceptions import InstalRuntimeError

class Sensor(ClingoWrapper):
    """
        Sensor
        The ClingoWrapper for single shot solves.
        A significant chunk of this code is legacy and thus fragile.
    """

    def __init__(self, initially, model_files, domain_facts, args):
        self.holdsat = initially
        self.occurred = []
        self.last_solution = None
        self.cycle = 0
        self.horizon = 1
        self.args = args
        self.observation = None

        self.observed = []
        self.undo_external = []
        self.ctl = Control(['-c', 'horizon={0}'.format(self.horizon)])
        super(Sensor, self).__init__(
            initially, model_files, domain_facts, args)

    def print_universe(self):
        print("universe:", len(self.ctl.domains))
        for x in self.ctl.domains:
            print(x.atom, x.is_fact, x.is_external)

    def check_events(self, event, present, absent):
        return self.check_sensor_data(event, self.occurred, present, absent)

    def check_facts(self, event, present, absent):
        return self.check_sensor_data(event, self.holdsat, present, absent)

    def check_sensor_data(self, event, data, present, absent):
        satisfied = True
        for f in present:
            # print("checking",f,present_state,sensor.holdsat)
            if not (parse_term(f) in data):
                print("Not satisfied({n})\n{event} |="
                      .format(event=event, n=self.cycle), f)
                satisfied = False
        for f in absent:
            # print("checking",f,present_state,sensor.holdsat)
            if parse_term(f) in data:
                print("Not satisfied({n})\n{event} !|="
                      .format(event=event, n=self.cycle), f)
                satisfied = False
        # print("check_final",satisfied)
        return satisfied

    def solve(self, event):
        self.ctl.assign_external(Function('_eventSet', [0]), True)
        if self.args.verbose > 1:
            print(self.cycle, "<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")
        self.observation = parse_term(event)
        for x in self.undo_external:
            if self.args.verbose > 1:
                print("unassign", x)
            self.ctl.assign_external(x, False)
        self.undo_external = []
        if self.args.verbose > 1:
            print(self.cycle, "----------------------------------------")
        for x in self.holdsat + [self.observation]:
            if self.args.verbose > 1:
                print("assign", x)
            self.ctl.assign_external(x, True)
            self.undo_external.append(x)
        self.last_solution = None
        if self.args.verbose > 1:
            print(self.cycle, "----------------------------------------")
        solveResult = self.ctl.solve(on_model=self.on_model)
        if solveResult.unsatisfiable:
            raise InstalRuntimeError(
                "Solver produced 0 answer sets. This usually means:\n"
                "- You have included additional .lp files with constraints in them."
                "- You have forgotten to ground types that exist in your institutions.")
        # self.print_universe()
        if self.args.verbose > 1:
            print(self.cycle, ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
        if self.args.verbose > 0:
            print("")
        self.cycle += 1
        return self.last_solution

    def on_model(self, model):
        self.last_solution = model.symbols(atoms=True)
        self.holdsat = []
        self.occurred = []
        self.observed, self.occurred, self.holdsat = model_atoms_to_lists(model.symbols(shown=True),
                                                                          verbose=self.args.verbose)
        if self.args.verbose > 0:
            print(state_to_string(self.observed, self.occurred, self.holdsat))

    def get_state_json(self):
        return state_dict_from_lists(self.observed, self.occurred, self.holdsat)
