#!/usr/bin/python

# 20160421 JAP: remove code for grounding file: see print_types in instalparser
# 20160413 JAP: revise domain file handling for multiple files
# 20160412 JAP: made domain file optional as consequence of staging
#               function to write grounding file for domain facts
#               function to extract domain facts from domain file
# 201603XX JAP: created file from parts of pyinstal

from __future__ import print_function
import instalparser
import bridgeparser
from collections import defaultdict
from instalargparse import getargs
from gringo import Fun, parse_term
import os.path
from tempfile import mkstemp, mkdtemp
import sys
import re

def instal_state_facts(args):
    if not(args.fact_file): return [] # ([],[])
    initlist = []
    finallylist = []
    for init in open(args.fact_file,'r').readlines():
        init = init.rstrip() # should be unnecessary, but parse_term is sensitive
        if init=='': continue # ditto
        term = parse_term(init)
        if term.name() in ["initially"]: # ,"finally"]:
            where = term.args()[0]
            what = term.args()[1]
            # if term.name()=="initially":
            initlist = ["holdsat("+str(what)+","+str(where)+")"] + initlist
            # else:
            #    finallylist = ["holdsat("+str(what)+","+str(where)+")"] + finallylist
        else:
            sys.write.stderr("WARNING: Fact not recognized:",init)
    return initlist # (initlist,finallylist)

def instal_domain_facts(args):
    domain_facts = defaultdict(set)
    typename = r"([A-Z][a-zA-Z0-9_]*)"
    literal = r"([a-z|\d][a-zA-Z0-9_]*)"
    # domain_files = [args.domain_file] if args.domain_file else []
    # JAP 20160412: do we need the bridge domain file?  multiple domain files better?
    # domain_files += [args.bridge_domain_file] if args.bridge_domain_file else []
    for dpath in args.domain_files:
        f = open(dpath,'r')
        for l in f.readlines():
            l = l.rstrip() # lose trailing \n
            if l=='': continue # 20160323 JAP: skip blank lines
            [t,r] = re.split(": ",l)
            t = t.lower()
            r = re.split(" ",r)
            for s in r:
                if not(re.search(literal,s)):
                    print("ERROR: Unrecognized literal in {x}".format(x=l))#,file=stderr)
                    exit(-1)
                domain_facts[t].update([s])
        f.close()
    return domain_facts

def instal_compile_file(args,mode,ifile,ofile,parser):
    parser.instal_input = open(ifile,'r')
    if args.output_file:
        parser.instal_output = open(ofile,'w')
    parser.mode = mode 
    document = ""
    document = document + parser.instal_input.read(-1)
    parser.instal_parse(document) 
    parser.instal_print_all()
    parser.instal_input.close()
    parser.instal_output.close()

def instal_compile(args):
    if len(args.input_files)==1:
        mode = "single"
    else:
        mode = "composite"
        all_lists = {}
    output_files = args.lp_files
    for ifile in args.ial_files:
        if mode=="composite":
            ofile = os.path.basename(ifile)
            ofile = ofile.replace('.ial','.lp')
            ofile = args.output_file + '/' + ofile
        else:
            ofile = args.output_file
        output_files = [ofile] + output_files
        iparser = instalparser.makeInstalParser()
        instal_compile_file(args,mode,ifile,ofile,iparser)
        if mode=="composite":
            all_lists[iparser.names["institution"]] = [iparser.exevents,
                                                       iparser.inevents,
                                                       iparser.vievents,
                                                       iparser.fluents,
                                                       iparser.obligation_fluents,
                                                       iparser.noninertial_fluents]
        iparser.instal_input.close()
    if args.bridge_file:
        ofile = os.path.basename(args.bridge_file)
        ofile = ofile.replace('.ial','.lp')
        ofile = args.output_file + '/' + ofile
        output_files = [ofile] + output_files
        bparser = bridgeparser.makeInstalParser()
        bparser.all_lists = all_lists
        instal_compile_file(args,"composite",args.bridge_file,ofile,bparser)
    return output_files

if __name__=="__main__":
    args,_ = getargs()
    instal_compile(args)
