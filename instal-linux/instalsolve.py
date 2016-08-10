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
from instalargparse import getargs, check_args, buildargparser
from instalcompile import instal_compile, instal_state_facts, instal_domain_facts
from instaltrace import instal_trace, instal_gantt
from sensor import Sensor
from collections import defaultdict
import fileinput
import sys
import os.path
import shutil
import simplejson as json
from gringo import Fun
import time

#import __builtin__

#try:	#stack overflow 18229628
#	__builtin__.profile
#except AttributeError:
#	def profile(f): return f

def dummy_callback(x,y):
    return

def encode_Fun(obj):
    if isinstance(obj, Fun):
        return {"__Fun__": True, "name": obj.name(), "args": obj.args() }
    raise TypeError(repr(obj) + " is not JSON serializable")

def decode_Fun(obj):
    return

def instal_solve():
    args,unk=getargs()
    instal_solve_with_args(args,unk)

def instal_solve_keyword(bridge_file=False, domain_files=[],fact_files=[],gantt_file=None,input_files=[],json_file=None,output_file=None,trace_file=None,verbose=0,query=None,states=None,text_file=None):
    parser = buildargparser()
    args = []
    if bridge_file:
        args += ["-b",bridge_file]

    args += ["-d"] + domain_files

    if len(fact_files) > 0:
        args += ["-f"] + fact_files

    if gantt_file is not None:
        args += ["-g"] + gantt_file

    args += ["-i"] + input_files

    if json_file is not None:
        args += ["-j", json_file]

    if output_file is not None:
        args += ["-o", output_file]

    if trace_file is not None:
        args += ["-t", trace_file]

    if verbose > 0: args += ["-{v}".format(v="v"*verbose)]

    if query is not None:
        args += ["-q" ,query]

    if states is not None:
        args += ["-s",states]

    if json_file is not None:
        args += ["-j",json_file]

    (a,u) = parser.parse_known_args(args)
    check_args(a,u)
    instal_solve_with_args(a,u)



def instal_solve_with_args(args,unk):
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
    metadata = {}
    metadata['pid'] = os.getpid()
    metadata['source_files'] = args.input_files + args.domain_files
    metadata['timestamp'] = 0
    if args.json_file: jf = open(args.json_file,'w')
    observed = {}
    occurred = defaultdict(list)
    holdsat = defaultdict(list)
    holdsat[0] = sensor.holdsat
    if args.json_file:
        metadata['timestamp'], metadata['previous_timestamp'] = time.time(), metadata['timestamp']
	out_json = sensor.get_state_json()
	out_json.update({"metadata" : metadata})
        print(json.dumps(out_json,
                         sort_keys=True,separators=(',',':'),default=encode_Fun),file=jf)
    for event in fileinput.input(args.query):
        sensor.solve(event)
        # dump trace data in JSON format
        if args.json_file:
	    out_json = sensor.get_state_json()
	    out_json.update({"metadata" : metadata})
            print(json.dumps(out_json,
                             sort_keys=True,separators=(',',':'),default=encode_Fun),file=jf)
        # keep trace data in internal format if visualization option selected
        if args.trace_file or args.gantt_file:
            observed[sensor.cycle-1] = sensor.observation
            occurred[sensor.cycle-1] = sensor.occurred
            holdsat[sensor.cycle] = sensor.holdsat
    if args.json_file: jf.close()
    # write LaTeX visualizations
    # print(observed)
    if args.trace_file:
        instal_trace(args,observed,occurred,holdsat)
    if args.gantt_file:
        instal_gantt(args,observed,occurred,holdsat)

if __name__=="__main__": 
    instal_solve()

