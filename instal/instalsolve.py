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
from instalargparse import getargs
from instalcompile import instal_compile, instal_state_facts, instal_domain_facts
from instaltrace import instal_trace, instal_gantt
from sensor import Sensor
from collections import defaultdict
import fileinput
import sys
import os.path
import shutil

def dummy_callback(x,y):
    return

def instal_solve():
    args,unk=getargs()
    model_files = instal_compile(args)
    initial_state = instal_state_facts(args)
    domain_facts = instal_domain_facts(args)
    sensor = Sensor(dummy_callback,initial_state,model_files,domain_facts,args)
    # delete temporary files
    if os.path.dirname(args.output_file)=='/tmp': 
        if os.path.isdir(args.output_file):
            shutil.rmtree(args.output_file)
        else:
            os.remove(args.output_file)
    observed = {}
    occurred = defaultdict(list)
    holdsat = defaultdict(list)
    holdsat[0] = sensor.holdsat
    for event in fileinput.input(args.query):
        sensor.solve(event)
        if args.trace_file or args.gantt_file: # only save for later if needed
            observed[sensor.cycle] = sensor.observation
            occurred[sensor.cycle] = sensor.occurred
            holdsat[sensor.cycle] = sensor.holdsat
    # write LaTeX visualizations
    if args.trace_file:
        instal_trace(args,sensor,observed,occurred,holdsat)
    if args.gantt_file:
        instal_gantt(args,sensor,observed,occurred,holdsat)

if __name__=="__main__": 
    instal_solve()

