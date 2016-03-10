#!/usr/bin/python

#------------------------------------------------------------------------
# REVISION HISTORY:
# 20160308 JAP: removed unused code, moved Sensor class to own file to
#               facilitate testing framework, removed -t option, removed -e
#               option and set up main loop to read via fileinput to permit
#               either stdin or a filename on the command line
# 20160301 JAP: first version of incremental solver; added command line
#               options -f for initial fact file and -e for event file/stream
# 20160204 JAP: call solver and process answer set (lots of assumptions)
#               tested with pcd/query and laptop/in4 models
# 20160203 JAP: started coding and log, imported code from pyinstal.py
#               refactored instal_print_xxx code into instalparser method


from __future__ import print_function
import re
import sys
import argparse
import bridgeparser
import instalparser
import copy
import string 
from gringo import Control, Model, Fun, parse_term
import gringo
from sensor import Sensor
import ply.lex as lex
from collections import defaultdict
from itertools import count
import fileinput

def arb(s): return s

def getargs():
    argparser = argparse.ArgumentParser()
    argparser.add_argument(
        "-b", "--bridge-file", type=arb,
        help="specify bridge instal file")
    argparser.add_argument(
        "-bd", "--bridge-domain-file", type=arb,
        help="specify domain file for bridge institution")
    argparser.add_argument(
        "-d", "--domain-file", type=arb, 
        help="specify domain file")
    argparser.add_argument(
        "-f", "--fact-file", type=arb,
        help="specify initial fact file")
    argparser.add_argument(
        "-i", "--instal-file", type=arb,
        help="specify single instal file")
    argparser.add_argument(
        "-il", "--instal-files-list", type=str, nargs='+', 
        help="specify a list of instal files")
    argparser.add_argument(
        "-m", "--mode-option", type=arb, nargs='?', default='s',
        help="specify the mode, single(s/S) or composite(c/C)")
    argparser.add_argument(
        "-o", "--output-file", type=arb,
        help="specify output file for single instal file, or output directory for a list of instal files")
    argparser.add_argument(
        "-q", "--query-file", type=arb,
        help="specify query file")
    # argparser.add_argument(
    #     "-t", "--time", type=int,
    #     help="specify number of time steps")
    argparser.add_argument(
        "-v", "--verbose", type=int,
        help="turns on trace output, 0 for holdsat, 1 for more")
    # got following line from http://stackoverflow.com/questions/1450393/how-do-you-read-from-stdin-in-python
    # which allows fileinput and argparse to co-exist
    args,unk = argparser.parse_known_args()
    # some self-check argument failure cases 
    if args.instal_file and args.instal_files_list:
        sys.stderr.write("Argument Error: either give a single instal file (-i) or a list of instal files (-il) \n")
        exit(-1)
    if (args.mode_option == ('s' or 'S'))and args.instal_files_list:
        sys.stderr.write("Argument Error: when processing a list of instal files, mode (-m) can only be composite (c/C) \n")
        exit(-1)
    if  args.bridge_file and not args.bridge_domain_file:
        sys.stderr.write("Argument Error: bridge domain file (-bd) is needed to process bridge file \n")
        exit(-1)
    if  args.bridge_file and not args.instal_files_list:
        sys.stderr.write("Argument Error: bridge instal needs the participiting instal files (-il) \n")
        exit(-1)
    if args.mode_option not in ('s', 'S', 'c', 'C'):
        sys.stderr.write("Argument Error: mode option (-m) can only be s/S or c/C \n")
        exit(-1)
    # or get on with the work
    return args,unk

# function to print domain file 
def print_domain(parser, domain_file):
    typename = r"([A-Z][a-zA-Z0-9_]*)"
    literal = r"([a-z|\d][a-zA-Z0-9_]*)"
    f = open(domain_file,'r')
    parser.instal_print("%\n% Domain declarations for {institution}\n%".format(**parser.names))
    for l in f.readlines():
        l = l.rstrip() # lose trailing \n
        [t,r] = re.split(": ",l)
        if not(re.search(typename,l)):
            parser.instal_error("ERROR: No type name in {x}".format(x=l))
            exit(-1)
        #check t is declared
        if not(t in parser.types):
            parser.instal_error("ERROR: type not declared in {x}".format(x=l))
            exit(-1)
        t = parser.types[t]
        r = re.split(" ",r)
        for s in r:
            if not(re.search(literal,s)):
                parser.instal_error("ERROR: Unrecognized literal in {x}".format(x=l))
                exit(-1)
            parser.instal_print("{typename}({literalname}).".format(
                typename=t,literalname=s))
    f.close() 

def initially(i,l):
    return map(lambda (f): Fun("holdsat",[parse_term(f),parse_term(i)]),l)

def pystream():
    args,unk=getargs()
    iparser = instalparser.makeInstalParser()
    if args.instal_file:    
        f = open(args.instal_file,'r')
    if args.output_file and args.instal_file:
        iparser.instal_output = open(args.output_file,'w')
    if args.mode_option and args.instal_file:
        if args.mode_option in ('s','S'):
            iparser.mode = "single" 
        elif args.mode_option in ('c','C'):
            iparser.mode = "composite"
        else:
            sys.stderr.write("Mode option can only be s/S or c/C \n")
    # set up default mode to single 
    if not args.mode_option and args.instal_file:
        iparser.mode = "default" 
    idocument = ""
    if args.instal_file: idocument = idocument + f.read(-1)
    if args.instal_file:
        iparser.instal_parse(idocument) 
    if args.domain_file and args.instal_file:
        print_domain(iparser, args.domain_file) 
    if args.instal_file:
        iparser.instal_print_all()
    if args.instal_file: f.close()
    if args.output_file: iparser.instal_output.close()
    if args.output_file and args.fact_file:
        institution = [
            "externals.lp",
            "time.lp",
            args.output_file
            ]
        facts = open(args.fact_file,'r')
        initial_state = initially(iparser.names["institution"],facts.readlines())
        sensor = Sensor(initial_state,institution,args)
        # print("initially:")
        # for i in initial_state:
        #     print(i.name(),i.args())
        # print("events from:",args.event_file)
        # with open(args.event_file,'r') as events:
        #     for e in events:
        for event in fileinput.input(unk):
            observation = parse_term(event)
            if args.verbose>=0: print(sensor.cycle,"<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")
            sensor.solve(observation)
            if args.verbose>=0: print(sensor.cycle,">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
            sensor.cycle += 1
        # print("*** end of stream")

pystream()

exit(0)
