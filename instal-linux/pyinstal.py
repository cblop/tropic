#!/usr/bin/python

#------------------------------------------------------------------------
# REVISION HISTORY:
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


sys.path.insert(0,"../..")

if sys.version_info[0] >= 3:
    raw_input = input

#bridge_output = sys.stdout

bparser = bridgeparser.makeInstalParser()


typename = r"([A-Z][a-zA-Z0-9_]*)"
literal = r"([a-z|\d][a-zA-Z0-9_]*)"


# TL: ideally, we need to create instance parser for each institutions like below 

#------------------------------------------------------------------------
# command-line parameter processing

def arb(s): return s

argparser = argparse.ArgumentParser()
argparser.add_argument("-d", "--domain-file", type=arb, help="specify domain file")
argparser.add_argument("-il", "--instal-files-list", type=str, nargs='+', help="specify a list of instal files")
argparser.add_argument("-i", "--instal-file", type=arb, help="specify single instal file")
argparser.add_argument("-o", "--output-file", type=arb, help="specify output file for single instal file, or output directory for a list of instal files")
argparser.add_argument("-b", "--bridge-file", type=arb, help="specify bridge instal file")
argparser.add_argument("-bd", "--bridge-domain-file", type=arb, help="specify domain file for bridge institution")
#argparser.add_argument("-p1", "--part1-file", type=arb, help="specify part 1 file of a single instal")
#argparser.add_argument("-p2", "--part2-file", type=arb, help="specify part 2 file of a single instal")
argparser.add_argument("-m", "--mode-option", type=arb, nargs='?', default='s', help="specify the mode, single(s/S) or composite(c/C)")
# JAP 20121124
argparser.add_argument("-t", "--time", type=int, help="specify number of time steps")
args=argparser.parse_args()



#if args.output_file:
#    parser.bridge_output = open(args.output_file,'w')

# function to print domain file 
def print_domain(parser, domain_file):
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

def print_time(parser, time):
    parser.instal_print("instant(0).")
    for i in range(0,time-1):
        parser.instal_print("next({i},{j}).\ninstant({j}).".format(i=i,j=i+1))
    parser.instal_print("final({i}).".format(i=time-1))
    parser.instal_print("start(0).")


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

#####-----------process single instal file ----------#################
# set up output defaults
#print_part1 = True
#print_part2 = True

iparser = instalparser.makeInstalParser()

if args.instal_file:    
    f = open(args.instal_file,'r')

#if args.part1_file:
#    p1 = open(args.part1_file,'r')

#if args.part2_file:
#    if not(args.part1_file):
#        sys.stderr.write("Part2 parameter can only be used in conjunction with a part1")
#    p2 = open(args.part2_file,'r')
#    exit(-1)

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
# read inputs

#if args.part1_file: idocument = p1.read(-1); print_part1 = False
#if args.part2_file: idocument = idocument + p2.read(-1); print_part2 = False
if args.instal_file: idocument = idocument + f.read(-1)

#else: idocument = idocument + sys.stdin.read(-1)

# document should now contain part1 + part2 + part3
if args.instal_file:
    iparser.instal_parse(idocument) 

if args.domain_file and args.instal_file:
    print_domain(iparser, args.domain_file) 
  

if args.time:
    print_time(iparser, args.time)


# JAP 20121121: what follows attempts to implement the division of code
# generation according to the -p1 and -p2 flags
if args.instal_file:
    iparser.instal_print("%\n% "
                 "-------------------------------"
                 "PART 1"
                 "-------------------------------"
                 "\n%")
    iparser.instal_print_standard_prelude()
    iparser.instal_print_constraints()
    iparser.instal_print_types()
    iparser.instal_print_exevents()
    iparser.instal_print_nullevent()
    iparser.instal_print_inevents()
    iparser.instal_print_vievents()
    iparser.instal_print_crevents()
    iparser.instal_print_dievents()
    iparser.instal_print_dissolve()
    iparser.instal_print_inertial_fluents()
    iparser.instal_print_noninertial_fluents()
    iparser.instal_print_violation_fluents()
    iparser.instal_print_obligation_fluents()
#else if :
#    iparser.instal_print("%\n% Using part1 from: {f}\n%".format(f=args.part1_file))
#if print_part2:
    iparser.instal_print("%\n% "
                 "-------------------------------"
                 "PART 2"
                 "-------------------------------"
                 "\n%")
    iparser.instal_print_generates()
    iparser.instal_print_initiates()
    iparser.instal_print_terminates()
    iparser.instal_print_noninertials()
#else:
#    iparser.instal_print("%\n% Using part2 from: {f}\n%".format(f=args.part2_file))

    iparser.instal_print("%\n% "
                 "-------------------------------"
                 "PART 3"
                 "-------------------------------"
                 "\n%")
    iparser.instal_print_initially()
    iparser.instal_print("%\n% End of file\n%")

if args.instal_file: f.close()
#if args.part1_file: p1.close()
#if args.part2_file: p2.close()
if args.output_file: iparser.instal_output.close()

#####-----------process list of instal files ----------#################
parser_dict = {} 
output_dict = {}
input_dict = {}
all_lists = {} 

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
        print_domain(parser, args.domain_file)
        if args.time:
            print_time(parser, args.time)

        parser.instal_print("%\n% "
                     "-------------------------------"
                     "PART 1"
                     "-------------------------------"
                    "\n%")
        parser.instal_print_standard_prelude()
        parser.instal_print_constraints()
        parser.instal_print_types()
        parser.instal_print_exevents()
        parser.instal_print_nullevent()
        parser.instal_print_inevents()
        parser.instal_print_vievents()
        parser.instal_print_crevents()
        parser.instal_print_dievents()
        parser.instal_print_dissolve()
        parser.instal_print_inertial_fluents()
        parser.instal_print_noninertial_fluents()
        parser.instal_print_violation_fluents()
        parser.instal_print_obligation_fluents()
        parser.instal_print("%\n% "
                     "-------------------------------"
                     "PART 2"
                     "-------------------------------"
                    "\n%")
        parser.instal_print_generates()
        parser.instal_print_initiates()
        parser.instal_print_terminates()
        parser.instal_print_noninertials()
        parser.instal_print("%\n% "
                     "-------------------------------"
                     "PART 3"
                     "-------------------------------"
                    "\n%")
        parser.instal_print_initially()
        parser.instal_print("%\n% End of file\n%")
        all_lists[name] = [copy.deepcopy(parser.exevents), copy.deepcopy(parser.inevents), copy.deepcopy(parser.vievents), copy.deepcopy(parser.fluents), copy.deepcopy(parser.obligation_fluents), copy.deepcopy(parser.noninertial_fluents)]
        f.close()
        parser_dict[name] = parser
        output_dict[name] = name_of_output 
        parser.clear_all_dicts()



#####-----------process bridge file ----------#################

# collect all_lists from each institution parser for bridge parser 
#all_lists = {} 
#for name, parser in parser_dict.iteritems():
#    list_name = name
#    all_lists[list_name] = [parser.exevents, parser.inevents, parser.vievents, parser.fluents, parser.obligation_fluents, parser.noninertial_fluents] 

bparser.all_lists = all_lists 



# set input and output for bridge file 
if args.bridge_file:
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
        print_domain(bparser, args.bridge_domain_file)
    if args.time and args.bridge_file:
        print_time(bparser, args.time)

    bparser.instal_print("%\n% "
                 "-------------------------------"
                 "PART 1"
                 "-------------------------------"
                 "\n%")
    bparser.instal_print_standard_prelude()
    #bparserinstal_print_constraints()
    bparser.instal_print_types()
    bparser.instal_print_exevents()
    bparser.instal_print_nullevent()
    bparser.instal_print_inevents()
    bparser.instal_print_vievents()
    bparser.instal_print_crevents()
    bparser.instal_print_dievents()
    bparser.instal_print_dissolve()
    bparser.instal_print_inertial_fluents()
    bparser.instal_print_noninertial_fluents()
    bparser.instal_print_violation_fluents()
    bparser.instal_print_obligation_fluents()
    bparser.instal_print_cross_fluents()
    bparser.instal_print("%\n% "
                 "-------------------------------"
                 "PART 2"
                 "-------------------------------"
                 "\n%")
    bparser.instal_print_xgenerates()
    bparser.instal_print_xinitiates()
    bparser.instal_print_xterminates()
    bparser.instal_print("%\n% "
                 "-------------------------------"
                 "PART 3"
                 "-------------------------------"
                 "\n%")
    bparser.instal_print_initially()

    bparser.instal_print("%\n% End of file\n%")
    

#####-----------closing files ----------#################

for name, f in input_dict.iteritems():
    f.close()

for name, parser in parser_dict.iteritems():
    parser.instal_output.close()

if args.bridge_file: 
    bf.close()
    bparser.instal_output.close()















