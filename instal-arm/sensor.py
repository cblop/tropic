#------------------------------------------------------------------------
# REVISION HISTORY:

# 20160414 JAP: changed class def to follow new convention
# 20160414 CAP: add domain fact check after grounding in __init__
# 20160412 JAP: add domain_facts arg to constructor + multi-program grounding
# 201603XX JAP: added check_events and check_facts methods
#               moved satisfied output up to run_test
# 20160308 JAP: created file from pystream.py.  changed verbose to allow
#               levels

from __future__ import print_function
from gringo import Control, Model, Fun, parse_term
import json
import sys

from instaljsonhelpers import model_atoms_to_lists, state_dict_from_lists, atom_str, state_to_string, dict_funs_to_list

class Sensor(object):

    def __init__(self, callback, initially, model_files, domain_facts, args):
        self.holdsat = initially
        self.occurred = []
        self.callback = callback
        self.last_solution = None
        self.cycle = 0
        self.horizon = 1
        self.args = args
        self.observation = None
	self.observed = []
        self.undo_external = []
        self.ctl = Control(['-c', 'horizon={0}'.format(self.horizon)])
        for x in model_files:
            if args.verbose>2: print("loading: ",x)
            self.ctl.load(x)
	parts = []
        for typename,literals in domain_facts.iteritems():
            for l in literals:
                parts += [(typename, [parse_term(l)])]
        if args.verbose>2: print("grounding: ", parts+[("base",[])])
        self.ctl.ground(parts+[("base", [])])
        if args.verbose>2: print("grounded")
	signature_types = [s[0] for s in self.ctl.domains.signatures()]
	from_domain_types = [d for d in domain_facts]
	#Testing for type names in domain file not in grounded file
	for d in from_domain_types:
            if d not in signature_types:
                print("WARNING: Type {} in domain file is not in grounded model.".format(d),file=sys.stderr)
        if args.verbose>2: print("initialized")

    def print_universe(self):
        print("universe:", len(self.ctl.domains))
        for x in self.ctl.domains:
            print(x.atom, x.is_fact, x.is_external)

    def check_events(self,event,present,absent):
        return self.check_sensor_data(event,self.occurred,present,absent)

    def check_facts(self,event,present,absent):
        return self.check_sensor_data(event,self.holdsat,present,absent)

    def check_sensor_data(self,event,data,present,absent):
        satisfied = True
        for f in present:
            # print("checking",f,present_state,sensor.holdsat)
            if not(parse_term(f) in data):
                print("Not satisfied({n})\n{event} |="
                      .format(event=event,n=self.cycle),f)
                satisfied = False
        for f in absent:
            # print("checking",f,present_state,sensor.holdsat)
            if (parse_term(f) in data):
                print("Not satisfied({n})\n{event} !|="
                      .format(event=event,n=self.cycle),f)
                satisfied = False
        # print("check_final",satisfied)
        return satisfied

    def solve(self, event):
        if self.args.verbose>1:
            print(self.cycle,"<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")
        self.observation = parse_term(event)
        for x in self.undo_external:
            if self.args.verbose>1:
                print("unassign",x)
            self.ctl.assign_external(x, False)
        self.undo_external = []
        if self.args.verbose>1:
            print(self.cycle,"----------------------------------------")
        for x in self.holdsat + [self.observation]:
            if self.args.verbose>1:
                print("assign",x)
            self.ctl.assign_external(x, True)
            self.undo_external.append(x)
        self.last_solution = None
        if self.args.verbose>1:
            print(self.cycle,"----------------------------------------")
        self.ctl.solve(on_model=self.on_model)
        # self.print_universe()
        if self.args.verbose>1:
            print(self.cycle,">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
        if self.args.verbose>0: print("")
        self.cycle += 1
        return self.last_solution

    def on_model(self, model):
        self.last_solution = model.atoms()
        self.holdsat = []
        self.occurred = []
        self.observed, self.occurred, self.holdsat = model_atoms_to_lists(model.atoms(Model.ATOMS),verbose=self.args.verbose)
        if self.args.verbose>0:
            print(state_to_string(self.observed,self.occurred,self.holdsat))
			

    def get_state_json(self):
	return state_dict_from_lists(self.observed,self.occurred,self.holdsat)
