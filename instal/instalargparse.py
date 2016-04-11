from __future__ import print_function
import argparse
import sys
import os.path
from tempfile import mkstemp, mkdtemp

def arb(s): return s

def buildargparser():
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
        "-i", "--input-files", type=str, nargs='+', 
        help="specify one or more instal files")
    argparser.add_argument(
        "-o", "--output-file", type=arb,
        help="output file/directory for one/several inputs: uses /tmp if omitted")
    argparser.add_argument(
        "-t", "--trace-file", type=arb,
        help="specify output file trace visualization")
    argparser.add_argument(
        "-v", "--verbose", action='count',
        help="turns on trace output, v for holdsat, vv for more")
    return argparser

def getargs():
    argparser = buildargparser()
    # got following line from http://stackoverflow.com/questions/1450393/how-do-you-read-from-stdin-in-python
    # which allows fileinput and argparse to co-exist, but might be better to use .REMAINDER
    args,unk = argparser.parse_known_args()
    # some self-check argument failure cases 
    if  args.bridge_file and not args.bridge_domain_file:
        sys.stderr.write("ERROR: bridge domain file (-bd) is needed to process a bridge file \n")
        exit(-1)
    if  args.bridge_file and (not(args.input_files) or len(args.input_files)<2):
        sys.stderr.write("ERROR: bridge instal needs at least two instal files (-i) \n")
        exit(-1)
    if len(args.input_files)==1 and not(args.output_file):
        (fd,ofile) = mkstemp()
        os.close(fd)
        args.output_file = ofile
    if len(args.input_files)>1 and not(args.output_file):
        # sys.stderr.write("ERROR: output directory (-o) needed with multiple input files\n")
        # exit(-1)
        args.output_file = mkdtemp()
    if len(args.input_files)>1 and not(os.path.isdir(args.output_file)):
        sys.stderr.write("ERROR: -o argument must be a directory for multiple input files\n")
        exit(-1)
    if len(args.input_files)>1 and not(args.bridge_file):
        sys.stderr.write("ERROR: a bridge file (-b) is needed with multiple input files\n")
        exit(-1)
    # or get on with the work
    return args,unk
