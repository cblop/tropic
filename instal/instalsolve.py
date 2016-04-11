#!/usr/bin/python

#------------------------------------------------------------------------
# REVISION HISTORY:
# 20160322 JAP: created file

from __future__ import print_function
from instalargparse import getargs
from instalcompile import instal_compile, instal_state_facts, instal_check_facts
from instaltrace import instal_trace
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
    (initial_state,final_state) = instal_state_facts(args)
    observed = {}
    occurred = defaultdict(list)
    holdsat = defaultdict(list)
    sensor = Sensor(dummy_callback,initial_state,model_files,args)
    holdsat[0] = sensor.holdsat
    for event in fileinput.input(unk):
        sensor.solve(event)
        observed[sensor.cycle] = sensor.observation
        occurred[sensor.cycle] = sensor.occurred
        holdsat[sensor.cycle] = sensor.holdsat
    if os.path.dirname(args.output_file)=='/tmp': 
        if os.path.isdir(args.output_file):
            # print("removing directory:",args.output_file)
            shutil.rmtree(args.output_file)
        else:
            # print("removing file:",args.output_file)
            os.remove(args.output_file)
    if args.trace_file:
        instal_trace(args,sensor,observed,occurred,holdsat)
    if instal_check_facts(sensor,final_state):
        exit(0)
    else:
        exit(-1)

instal_solve()
