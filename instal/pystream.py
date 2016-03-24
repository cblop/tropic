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
import os.path

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
        "-c", "--composite", action='store_true',
        help="specify domain file")
    argparser.add_argument(
        "-d", "--domain-file", type=arb, 
        help="specify domain file")
    argparser.add_argument(
        "-f", "--fact-file", type=arb,
        help="specify initial fact file")
    # this might be better as nargs='?'
    argparser.add_argument(
        "-i", "--instal-file", type=arb,
        help="specify single instal file")
    argparser.add_argument(
        "-il", "--instal-files-list", type=str, nargs='+', 
        help="specify a list of instal files")
    argparser.add_argument(
        "-o", "--output-file", type=arb,
        help="specify output file for single instal file, or output directory for a list of instal files")
    argparser.add_argument(
        "-q", "--query-file", type=arb,
        help="specify query file")
    argparser.add_argument(
        "-v", "--verbose", action='count',
        help="turns on trace output, v for holdsat, vv for more")
    # got following line from http://stackoverflow.com/questions/1450393/how-do-you-read-from-stdin-in-python
    # which allows fileinput and argparse to co-exist, but might be better to use .REMAINDER
    args,unk = argparser.parse_known_args()
    # some self-check argument failure cases 
    if args.instal_file and args.instal_files_list:
        sys.stderr.write("Argument Error: either give a single instal file (-i) or a list of instal files (-il) \n")
        exit(-1)
    if not(args.composite) and args.instal_files_list:
        sys.stderr.write("Argument Error: when processing a list of instal files, composite mode (-c) must be specified\n")
        exit(-1)
    if  args.bridge_file and not args.bridge_domain_file:
        sys.stderr.write("Argument Error: bridge domain file (-bd) is needed to process bridge file \n")
        exit(-1)
    if  args.bridge_file and not args.instal_files_list:
        sys.stderr.write("Argument Error: bridge instal needs the participating instal files (-il) \n")
        exit(-1)
    # or get on with the work
    return args,unk

def initially(i,l):
    return map(lambda (f): Fun("holdsat",[parse_term(f),parse_term(i)]),l)

def pystream_single(args,unk):
    iparser = instalparser.makeInstalParser()
    iparser.instal_input = open(args.instal_file,'r')
    if args.output_file:
        iparser.instal_output = open(args.output_file,'w')
    iparser.mode = "default" 
    idocument = ""
    idocument = idocument + iparser.instal_input.read(-1)
    iparser.instal_parse(idocument) 
    if args.domain_file and args.instal_file:
        iparser.print_domain(args.domain_file) 
    if args.instal_file:
        iparser.instal_print_all()
    if args.instal_file: iparser.instal_input.close()
    if args.output_file: iparser.instal_output.close()
    ##### start of multi-shot solving cycle
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
            if args.verbose>1: print(sensor.cycle,"<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")
            sensor.solve(observation)
            if args.verbose>1: print(sensor.cycle,">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
            sensor.cycle += 1
            if args.verbose>0: print("")
        # print("*** end of stream")

def pystream():
    args,unk=getargs()
    if not(args.composite) and args.instal_file:
        pystream_single(args,unk)
        return
    #####-----------process list of instal files ----------#################
    if not(args.output_file):
        sys.stderr.write("Output directory required for composite mode\n")
        exit(-1)
    if not(os.path.isdir(args.output_file)):
        sys.stderr.write("-o argument must be a directory in composite mode\n")
    parser_dict = {} 
    output_dict = {}
    input_dict = {}
    bparser = bridgeparser.makeInstalParser()
    bparser.all_lists = {} 
    if args.instal_files_list:
        for name in args.instal_files_list:
            parser = instalparser.makeInstalParser()
            parser.instal_input = open(name,'r')
            parser.mode = "composite"
            document = ""
            document = document + parser.instal_input.read(-1)
            hIn = string.rfind(name,'/') + 1  # get the index of '/' to extract the file name only     
            name = name[hIn:]
            name = name.replace('.ial','')
            input_dict[name] = parser.instal_input
            #print name
            #name_of_parser = name + '_parser'
            if args.output_file:
                name_of_output = args.output_file + '/' + name + '.lp'
                parser.instal_output = open(name_of_output,'w')            
            else:
                name_of_output = name + '.lp'
                parser.instal_output = open(name_of_output,'w')
            parser.instal_parse(document) 
            parser.print_domain(args.domain_file)
            parser.instal_print_all()
            bparser.all_lists[name] = [parser.exevents,
                                       parser.inevents,
                                       parser.vievents,
                                       parser.fluents,
                                       parser.obligation_fluents,
                                       parser.noninertial_fluents]
            parser.instal_input.close()
            parser_dict[name] = parser
            output_dict[name] = name_of_output 
    #####-----------process bridge file ----------#################
    if args.bridge_file:
        # set input and output for bridge file 
        bf = open(args.bridge_file,'r')
        bdocument = ""
        bdocument = bdocument + bf.read(-1)
        name = args.bridge_file
        hIn = string.rfind(name,'/') + 1  # get the index of '/' to extract the file name only     
        name = name[hIn:] 
        boutput = name.replace('.ial','.lp')
        #boutput = args.bridge_file.replace('.ial','.lp')
        if args.output_file:
            boutput = args.output_file + '/' + boutput      
            bparser.instal_output = open(boutput,'w')
        else:      
            bparser.instal_output = open(boutput,'w')
        bparser.instal_parse(bdocument) 
        bparser.mode = "composite" 
        if args.bridge_domain_file:
            bparser.print_domain(args.bridge_domain_file)
        bparser.instal_print_all()
    #####-----------closing files ----------#################
    for name, f in input_dict.iteritems():
        f.close()
    for name, parser in parser_dict.iteritems():
        parser.instal_output.close()
    if args.bridge_file: 
        bf.close()
        bparser.instal_output.close()
    ##### start of multi-shot solving cycle
    if args.composite and args.output_file: # and args.fact_file:
        institution = [
            "externals.lp",
            "bridge_externals.lp",
            "time.lp",
            boutput
            ] + output_dict.values()
        # print("files = ",institution)
        # facts = open(args.fact_file,'r')
        initial_state = [] # initially(iparser.names["institution"],facts.readlines())
        sensor = Sensor(initial_state,institution,args)
        # print("initially:")
        # for i in initial_state:
        #     print(i.name(),i.args())
        # print("events from:",args.event_file)
        # with open(args.event_file,'r') as events:
        #     for e in events:
        for event in fileinput.input(unk):
            observation = parse_term(event)
            if args.verbose>1: print(sensor.cycle,"<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")
            sensor.solve(observation)
            if args.verbose>1: print(sensor.cycle,">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
            sensor.cycle += 1
            if args.verbose>0: print("")
        # print("*** end of stream")

pystream()

exit(0)
