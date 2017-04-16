import argparse
import sys

import os.path

from .instalexceptions import InstalArgParserError


def buildargparser():
    argparser = argparse.ArgumentParser()
    argparser.add_argument(
        "-b", "--bridge-file", type=str,
        help="specify bridge instal file")
    # argparser.add_argument(
    # "-bd", "--bridge-domain-file", type=str,
    # help="specify domain file for bridge institution")
    argparser.add_argument(
        "-d", "--domain-files", type=str, nargs='+',
        help="specify one or more domain files (.idc)")
    argparser.add_argument(
        "-f", "--fact-files", type=str, nargs='+',
        help="specify initial fact file(s) (.iaf or .json)")
    argparser.add_argument(
        "-i", "--input-files", type=str, nargs='+',
        help="specify one or more instal files (.ial)")
    argparser.add_argument(
        "-j", "--json-file", type=str,
        help="specify json output file")
    argparser.add_argument(
        "-o", "--output-file", type=str,
        help="output file/directory for one/several inputs: uses /tmp if omitted")
    argparser.add_argument(
        "-v", "--verbose", action='count',
        help="turns on trace output, v for holdsat, vv for more")
    argparser.add_argument(
        "-q", "--query", type=str,
        help="specify query file (.iaq) - use \"-\" to take from stdin.")
    return argparser


def buildqueryargparser():
    argparser = buildargparser()
    argparser.add_argument(
        '-a', '--answer-set', type=int, default=0,
        help='choose an answer set (default all)')
    argparser.add_argument(
        '-n', '--number', type=int, default=1,
        help='compute at most <n> models (default 1, 0 for all)')
    argparser.add_argument(
        '-l', '--length', type=int, default=1,
        help='length of trace (default 1)')

    return argparser


def buildtraceargparser():
    argparser = argparse.ArgumentParser()
    argparser.add_argument(
        "-t", "--trace-file", type=str,
        help="specify output file for trace visualization")
    argparser.add_argument(
        "-v", "--verbose", action='count',
        help="turns on trace output, v for holdsat, vv for more")
    argparser.add_argument(
        "-g", "--gantt-file", type=str,
        help="specify output file for gantt visualization")
    argparser.add_argument(
        "-x", "--text-file", type=str,
        help="specify output file for text trace")
    argparser.add_argument(
        "-j", "--json-file", type=str,
        help="specify json output file")
    # hold this pending major rework of instaltrace
    # argparser.add_argument(
    # "-s", "--states", type=str,
    # help="specify which states to display (default all)")
    return argparser


def check_args(args, unk):
    # unk checking
    if len(unk) > 1:
        raise InstalArgParserError(
            "ERROR: More than one argument not connected to a flag.")

    # Query file checking
    if args.query is None:
        if not unk:
            args.query = None
        else:
            args.query = unk[0]

    if args.query:
        name, ext = os.path.splitext(args.query)
        if not ext == ".iaq":
            sys.stderr.write(
                "WARNING: Query file extension incorrect (should be .iaq)\n")

    # Fact file checking
    if args.fact_files is not None:
        for f in args.fact_files:
            name, ext = os.path.splitext(f)
            if not (ext == ".iaf" or ext == ".json"):
                sys.stderr.write(
                    "WARNING: Fact file extension incorrect (should be .iaf or .json)\n")
    else:
        args.fact_files = []

    if args.verbose is None:
        args.verbose = 0

    # Domain file checking
    if args.domain_files is not None:
        for domain_file in args.domain_files:
            name, ext = os.path.splitext(domain_file)
            if not ext == ".idc":
                sys.stderr.write(
                    "WARNING: Domain file extension incorrect (should be .idc)\n")
    else:
        args.domain_files = []
        sys.stderr.write(
            "WARNING: No domain files provided - is this deliberate?\n")

    # bridge file checking
    if args.bridge_file and (not args.input_files or len(args.input_files) < 2):
        raise InstalArgParserError(
            "ERROR: bridge instal needs at least two instal files (-i) \n")

    # TODO: deal with number and file extension of input files
    # input file checking
    # if len(args.input_files) == 1 and not (args.output_file):
    # (fd, ofile) = mkstemp()
    # os.close(fd)
    # args.output_file = ofile

    # if len(args.input_files) > 1 and not (args.output_file):
    # args.output_file = mkdtemp()

    # if len(args.input_files) > 1 and not (os.path.isdir(args.output_file)):
    #    raise InstalArgParserError("ERROR: -o argument must be a directory for multiple input files\n")

    args.ial_files = []
    args.lp_files = []
    for input_file in args.input_files:
        name, ext = os.path.splitext(input_file)
        if ext == ".ial":
            args.ial_files.append(input_file)
        elif ext == ".lp":
            args.lp_files.append(input_file)
        else:
            raise InstalArgParserError(
                "ERROR: Unrecognised input file extension (should be .ial or .lp)\n")

    return


def getargs():
    argparser = buildargparser()
    # got following line from http://stackoverflow.com/questions/1450393/how-do-you-read-from-stdin-in-python
    # which allows fileinput and argparse to co-exist, but might be better to
    # use .REMAINDER
    args, unk = argparser.parse_known_args()

    check_args(args, unk)

    return args, unk


def getqueryargs():
    argparser = buildqueryargparser()
    # got following line from http://stackoverflow.com/questions/1450393/how-do-you-read-from-stdin-in-python
    # which allows fileinput and argparse to co-exist, but might be better to
    # use .REMAINDER
    args, unk = argparser.parse_known_args()

    check_args(args, unk)

    return args, unk
