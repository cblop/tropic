#!/usr/bin/python

from __future__ import print_function
import instalparser
import bridgeparser
from sensor import Sensor
from collections import defaultdict
from instalargparse import getargs
from gringo import Fun, parse_term
import os.path
import sys

def instal_check_facts(sensor,final_state):
    present = True
    for f in final_state:
        # print("checking",f,final_state,sensor.holdsat)
        if not(parse_term(f) in sensor.holdsat):
            print("Failed({n}):".format(n=sensor.cycle),f)
            present = False
    # print("check_final",present)
    if present and sensor.args.verbose>0:
        print("Passed({n})".format(n=sensor.cycle))
    return present

def instal_state_facts(args):
    if not(args.fact_file): return ([],[])
    initlist = []
    finallylist = []
    for init in open(args.fact_file,'r').readlines():
        init = init.rstrip() # should be unnecessary, but parse_term is sensitive
        if init=='': continue # ditto
        term = parse_term(init)
        if term.name() in ["initially","finally"]:
            where = term.args()[0]
            what = term.args()[1]
            if term.name()=="initially":
                initlist = ["holdsat("+str(what)+","+str(where)+")"] + initlist
            else:
                finallylist = ["holdsat("+str(what)+","+str(where)+")"] + finallylist
        else:
            sys.write.stderr("WARNING: Fact not recognized:",init)
    return (initlist,finallylist)

def instal_compile_file(args,mode,ifile,ofile,dfile,parser):
    parser.instal_input = open(ifile,'r')
    if args.output_file:
        parser.instal_output = open(ofile,'w')
    parser.mode = mode 
    document = ""
    document = document + parser.instal_input.read(-1)
    parser.instal_parse(document) 
    parser.print_domain(dfile) 
    parser.instal_print_all()
    parser.instal_input.close()
    parser.instal_output.close()
    return parser

def instal_compile(args):
    if len(args.input_files)==1:
        mode = "single"
    else:
        mode = "composite"
        all_lists = {}
    output_files = []
    for ifile in args.input_files:
        if mode=="composite":
            ofile = os.path.basename(ifile)
            ofile = ofile.replace('.ial','.lp')
            ofile = args.output_file + '/' + ofile
        else:
            ofile = args.output_file
        output_files = [ofile] + output_files
        iparser = instalparser.makeInstalParser()
        instal_compile_file(args,mode,ifile,ofile,args.domain_file,iparser)
        if mode=="composite":
            all_lists[iparser.names["institution"]] = [iparser.exevents,
                                                       iparser.inevents,
                                                       iparser.vievents,
                                                       iparser.fluents,
                                                       iparser.obligation_fluents,
                                                       iparser.noninertial_fluents]
        iparser.instal_input.close()
    if args.bridge_file and args.bridge_domain_file:
        ofile = os.path.basename(args.bridge_file)
        ofile = ofile.replace('.ial','.lp')
        ofile = args.output_file + '/' + ofile
        output_files = [ofile] + output_files
        bparser = bridgeparser.makeInstalParser()
        bparser.all_lists = all_lists
        instal_compile_file(args,"composite",args.bridge_file,ofile,args.bridge_domain_file,bparser)
    return output_files # + ["externals.lp", "time.lp"] + (["bridge_externals.lp"] if mode=="composite" else [])


# instal_solve()

# exit(0)

# keyTerms = ['holdsat','observed','occurred','initiated','terminated']
# dictByWhen = defaultdict(lambda: defaultdict(list))
# dictByTerm = defaultdict(lambda: defaultdict(list))

# def build_trace(atom,cycle):
#     if atom.name() in keyTerms:
#         [what, where, when] = atom.args() # should always be 3 items.
#         when = cycle
#         dictByTerm[atom.name()][when].append({'what': what, 'where': where})
#         dictByWhen[when][atom.name()] = dictByTerm[atom.name()][when]

# def print_trace():
#     # can be used between cycles or at the end of the event stream
#     for when in dictByWhen:
#         print(when)
#         for what in dictByWhen[when]:
#             # print(what,dictByWhen[when][what]['what'],
#             #       'in',dictByWhen[when][what]['where'])
#             for x in dictByWhen[when][what]:
#                 # join(str(x) for x in atom.args())
#                 print(what,'(',x['what'],',',x['where'],')')
#     # need to clear dicts if printing between solving steps
#     dictByWhen.clear()
#     dictByTerm.clear()
