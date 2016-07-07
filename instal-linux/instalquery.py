#!/usr/bin/python

#------------------------------------------------------------------------
# REVISION HISTORY:

# 20160421 JAP: remove code to delete grounding program (see next comment)
# 20160412 JAP: code to process domain_facts (see instalcompile)
#               delete last file on model_files list (grounding program)
# 20160405 JAP: move code to release files as early as possible
#               made event and state saving conditional on args.trace_file
# 20160322 JAP: created file

from __future__ import print_function
from instalargparse import buildargparser, check_args
from instalcompile import instal_compile, instal_state_facts, instal_domain_facts
from instaltrace import instal_trace, instal_gantt
from sensor import Sensor
from collections import defaultdict
import fileinput
import sys
import os.path
import shutil
from gringo import Control, Model, Fun, parse_term

class Oracle(object):

    def __init__(self, callback, initially, model_files, domain_facts, args):
	self.holdsat = defaultdict(list)
        self.occurred = defaultdict(list)
        self.callback = callback
        self.last_solution = None
        self.cycle = 0
        self.args = args
        self.observations = None
        self.undo_external = []
        self.ctl = Control(['-n', str(args.number), '-c', 'horizon={0}'.format(args.length)])
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

    def solve_iter(self,events):
        self.observations = events
        for x in self.observations:
            if self.args.verbose>1:
                print("assign",x)
            self.ctl.assign_external(x, True)
        self.cycle = len(self.observations)
        answers = 0
        with self.ctl.solve_iter() as it:
            for m in it:
                if self.args.verbose>0: print("Answer set {}".format(answers))
                self.process_answer_set(m,answers)
                answers +=1
        if answers==1:
            print("There is 1 answer set")
        else:
            print("There are {} answer sets".format(answers))
        return

    def process_answer_set(self, model, answer):
        for atom in model.atoms(Model.ATOMS):
            # hook for client processing of atoms
            # if len(atom.args())==3: self.callback(atom,self.cycle)
            if (atom.name()=="occurred"):
                # self.occurred[atom.args()[2]].append(atom)
                self.occurred[atom.args()[2]].append(Fun(atom.name(), atom.args()[:-1]))
            if (atom.name()=="holdsat"):
                # self.holdsat[atom.args()[2]].append(atom)
                self.holdsat[atom.args()[2]].append(Fun(atom.name(), atom.args()[:-1]))

def dummy_callback(x,y):
    return

def instal_query():
    argparser = buildargparser()
    # additional parameters for instalquery
    argparser.add_argument(
        '-l', '--length', type=int, default=1,
        help='length of trace (default 1)')
    argparser.add_argument(
        '-n', '--number', type=int, default=1,
        help='compute at most <n> models (default 1, 0 for all)')
    args,unk = argparser.parse_known_args()
    check_args(args,unk)
    model_files = instal_compile(args)
    initial_state = instal_state_facts(args)
    domain_facts = instal_domain_facts(args)
    oracle = Oracle(dummy_callback,initial_state,model_files,domain_facts,args)
    # delete temporary files
    if os.path.dirname(args.output_file)=='/tmp': 
        if os.path.isdir(args.output_file):
            shutil.rmtree(args.output_file)
        else:
            os.remove(args.output_file)
    observed = []
    # enumerate the events in the query file
    for i,e in enumerate(fileinput.input(args.query)):
        observed += [Fun('observed',[parse_term(e).args()[0],i])]
    # note: events is a list of Fun not strings
    oracle.solve_iter(observed)
    # print("occurred = ",oracle.occurred)
    # print("holdsat = ",oracle.holdsat)
    # write LaTeX visualizations
    if args.trace_file:
        instal_trace(args,oracle,observed,oracle.occurred,oracle.holdsat)
    if args.gantt_file:
        instal_gantt(args,oracle,observed,oracle.occurred,oracle.holdsat)

if __name__=="__main__": 
    instal_query()

