#!/usr/bin/python

#------------------------------------------------------------------------
# REVISION HISTORY:
# 20160203 JAP: started coding and log, imported code from pyinstal.py
#               refactored instal_print_xxx code into instalparser method
# 20160204 JAP: call solver and process answer set (lots of assumptions)
#               tested with pcd/query and laptop/in4 models

from __future__ import print_function
import re
import sys
import argparse
import bridgeparser
import instalparser
import copy
import string 
import gringo
import ply.lex as lex
from collections import defaultdict

class aspTermLexer():

    # Build the lexer
    # def build(self,**kwargs):
    #    self.lexer = lex.lex(object=self, **kwargs)

    def __init__(self):
        self.lexer = lex.lex(module=self)

    reserved = { }

    tokens =  ['NAME','NUMBER','LPAR','RPAR','COMMA']

    # Tokens

    t_COMMA = r','
    t_LPAR = r'\('
    t_RPAR = r'\)'

    def t_NAME(self,t):
        r'[a-z][a-zA-Z_0-9]*'
        return t
    
    def t_NUMBER(self,t):
        r'\d+'
        # t.value = int(t.value)
        return t

    t_ignore = " \t\r"

    # Comments
    def t_COMMENT(self,t):
        r'%.*'
        pass
    # No return value. Token discarded

    def t_newline(self,t):
        r'\n+'
        t.lexer.lineno += t.value.count("\n")

    def t_error(self,t):
        print("Illegal character '%s'" % t.value[0])
        t.lexer.skip(1)

def arb(s): return s

def getargs():
    argparser = argparse.ArgumentParser()
    argparser.add_argument(
        "-d", "--domain-file", type=arb, 
        help="specify domain file")
    argparser.add_argument(
        "-il", "--instal-files-list", type=str, nargs='+', 
        help="specify a list of instal files")
    argparser.add_argument(
        "-i", "--instal-file", type=arb,
        help="specify single instal file")
    argparser.add_argument(
        "-q", "--query-file", type=arb,
        help="specify query file")
    argparser.add_argument(
        "-o", "--output-file", type=arb,
        help="specify output file for single instal file, or output directory for a list of instal files")
    argparser.add_argument(
        "-b", "--bridge-file", type=arb,
        help="specify bridge instal file")
    argparser.add_argument(
        "-bd", "--bridge-domain-file", type=arb,
        help="specify domain file for bridge institution")
    argparser.add_argument(
        "-m", "--mode-option", type=arb, nargs='?', default='s',
        help="specify the mode, single(s/S) or composite(c/C)")
    argparser.add_argument(
        "-t", "--time", type=int,
        help="specify number of time steps")
    args = argparser.parse_args()
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
    return args

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

def print_time(parser, time):
    parser.instal_print("instant(0).")
    for i in range(0,time-1):
        parser.instal_print("next({i},{j}).\ninstant({j}).".format(i=i,j=i+1))
    parser.instal_print("final({i}).".format(i=time-1))
    parser.instal_print("start(0).")

keyTerms = ['holdsat','observed','initiated','terminated','occurred']
dictByTerm = defaultdict(lambda: defaultdict(list))
dictByWhen = defaultdict(lambda: defaultdict(list))

def processAnswerSet(terms):
    mylex = aspTermLexer()
    for term in terms: # re.split(' ',terms):
        mylex.lexer.input(term)
        l = [tok.value for tok in mylex.lexer]
        # print("% tok.value = ",l)
        if l==[]: continue # skip blanks
        if l[0] in keyTerms:
            # some rather tacky dead-reckoning
            # print("% tok.value = ",l)
            what = string.join(l[2:-5],'')
            where = l[-4]
            when = int(l[-2])
            # print(what,where,when)
            dictByTerm[l[0]][when].append({'what': what, 'where': where})
            dictByWhen[when][l[0]] = dictByTerm[l[0]][when]
#        else:
#            print("% skipping \"{term}\""
#                  .format(term=string.join(l,'')))

terms = []

def get_terms(m):
    global terms
    for atom in m.atoms(gringo.Model.ATOMS):
        terms.extend([(atom.name(),atom.args())])

def get_terms_as_string(m):
    global terms
    terms = str(m)

def get_holdsat(m):
    global terms
    for atom in m.atoms(gringo.Model.ATOMS):
        if ((atom.name() in keyTerms)): #  and len(atom.args()) == 3): 
            # print(atom.name()+'('+','.join(str(x) for x in atom.args())+')')
            terms.append(atom.name()+'('+','.join(str(x) for x in atom.args())+')')

def pysolve():
    args=getargs()
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
    if args.time:
        print_time(iparser, args.time)
    if args.instal_file:
        iparser.instal_print_all()
    if args.instal_file: f.close()
    if args.output_file: iparser.instal_output.close()
    # set up to solve
    if args.output_file and args.query_file:
        # print("building solver\n")
        ctl = gringo.Control()
        # print("loading model\n")
        ctl.load(args.output_file)
        # print("loading query\n")
        ctl.load(args.query_file)
        # print("grounding program\n")
        ctl.ground([("base", [])])
        # print("running solver\n")
        # ctl.solve(on_model=lambda m: terms=str(m))
        ctl.solve(on_model=get_holdsat)
        # print("done\n")
        processAnswerSet(terms)
        # print(dictByTerm)
        # print(dictByWhen)
        for when in dictByWhen:
            print(when)
            for what in dictByWhen[when]:
                # print(what,dictByWhen[when][what]['what'],
                #       'in',dictByWhen[when][what]['where'])
                for x in dictByWhen[when][what]:
                    print(what+'('+x['what']+','+x['where']+')')

pysolve()
