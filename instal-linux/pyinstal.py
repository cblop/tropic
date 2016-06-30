#!/usr/bin/python

#------------------------------------------------------------------------
# REVISION HISTORY:
# 20160315 JAP: refactored back changes from pystream: use getargs for argument
#               processing, use instal_print_all method and likewise for
#               bridgeparser.  Made top-level code into a procedure (pyinstal)
# 20160314 JAP: removed -t option, call print_domain in parser
# 20140618 JAP: started log, fixed mode-option to default to 's'

# Examples:
# - process single institution:
#       ./main_br_all.py -i inst.ial -d domain.idc -m s -o inst.lp 
# - process a list of insitutions:
#       ./main_br_all.py -il inst1.ial inst2.ial inst3.ial -m c -o /ASPFiles 
# - process a list of insitutions AND a bridge institution:  
#       ./main_br_all.py -il inst1.ial inst2.ial inst3.ial -bd domain_br.idc -b bridge.ial -o /ASPFiles -m c 
# 
#
#
#

from __future__ import print_function
import re
import sys
import argparse
import bridgeparser
import instalparser
import copy
import string 


# sys.path.insert(0,"../..")

# if sys.version_info[0] >= 3:
#     raw_input = input

#bridge_output = sys.stdout

# TL: ideally, we need to create instance parser for each institutions like below 

#------------------------------------------------------------------------
# command-line parameter processing

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
    # got following line from http://stackoverflow.com/questions/1450393/how-do-you-read-from-stdin-in-python
    # which allows fileinput and argparse to co-exist
    # note: fileinput is only used in pystream and kept here to limit code inconsistency
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

def pyinstal():
    args,unk=getargs()
    bparser = bridgeparser.makeInstalParser()
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
        iparser.print_domain(args.domain_file) 
    if args.instal_file: iparser.instal_print_all()
    if args.instal_file: f.close()
    if args.output_file: iparser.instal_output.close()
    #####-----------process list of instal files ----------#################
    parser_dict = {} 
    output_dict = {}
    input_dict = {}
    bparser.all_lists = {} 
    if args.instal_files_list:
        for name in args.instal_files_list:
            parser= instalparser.makeInstalParser()
            f = open(name,'r')
            document = ""
            document = document + f.read(-1)
            hIn = string.rfind(name,'/') + 1  # get the index of '/' to extract the file name only     
            name = name[hIn:]
            name = name.replace('.ial','')
            input_dict[name] = f
            #print name
            #name_of_parser = name + '_parser'
            parser.mode = "composite"
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
            # JAP: can't see why copy is needed since these are all instance vars.
            #      hangover from pre-class version?
            # all_lists[name] = [copy.deepcopy(parser.exevents),
            #                    copy.deepcopy(parser.inevents),
            #                    copy.deepcopy(parser.vievents),
            #                    copy.deepcopy(parser.fluents),
            #                    copy.deepcopy(parser.obligation_fluents),
            #                    copy.deepcopy(parser.noninertial_fluents)]
            f.close()
            parser_dict[name] = parser
            output_dict[name] = name_of_output 
            # parser.clear_all_dicts()
    #####-----------process bridge file ----------#################
    if args.bridge_file:
        # collect all_lists from each institution parser for bridge parser 
        # bparser.all_lists = all_lists 
        # print(bparser.all_lists,file=sys.stderr)
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

pyinstal()

exit(0)














