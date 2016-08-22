#!/usr/bin/python
#------------------------------------------------------------------------
# REVISION HISTORY:

# 20160819 JAP: added code to print out text trace but need to check format
# 20160428 JAP: forgot code to remove - in two calls to number_to_words
# 20160415 JAP: changed render_observed to account for observed/compObserved unification
# 20160405 JAP: add render_observed and differentiate observed/compObserved
#               add Gantt-style trace output, suppressed overprint in ganntbar
# 20160330 JAP: bold for new fluents, sout for deleted
# 20160325 JAP: created file

from __future__ import print_function
import string
import inflect
import os
import sys
from gringo import Fun
from collections import defaultdict
from instalargparse import buildargparser
import simplejson as json

from instaljsonhelpers import as_Fun, check_trace_integrity, json_dict_to_string

latex_trace_header = r"""
\documentclass{article}
%\usepackage[a4paper,margin=0cm]{geometry}
\usepackage{todonotes}
\usepackage{array}
\usepackage{longtable}
\usepackage{enumitem}
\usepackage{tikz}
\pagestyle{empty}
\thispagestyle{empty}
\usetikzlibrary{shadows}
\usetikzlibrary{decorations}
\usetikzlibrary{shapes}
\usetikzlibrary{arrows}
\usetikzlibrary{calc}
\usetikzlibrary{fit}
\usetikzlibrary{backgrounds}
\usetikzlibrary{positioning}
\usetikzlibrary{chains}
\usetikzlibrary{scopes}
% \usetikzlibrary{matrix}
% \usepackage{pgfgantt}
\renewcommand*\familydefault{\sfdefault} %% Only if the base font of the document is to be sans serif
% \usepackage[T1]{fontenc}
\usepackage[normalem]{ulem}
\begin{document}
"""

# not currently used: may be useful for selective state printing
def neighborhood(iterable):
    iterator = iter(iterable)
    prev = None
    item = iterator.next()  # throws StopIteration if empty.
    for next in iterator:
        yield (prev,item,next)
        prev = item
        item = next
    yield (prev,item,None)

# Usage:
# for prev,item,next in neighborhood(l):
#     print prev, item, next

def render_observed(observed,t):
    stem = ""
    obs = observed[t]
    if len(obs) != 1:
	return
    else:
	obs = obs[0]
    if obs.name() =="observed":
        stem = str(obs.args()[0])
    else: print("% Unrecognised observation",observed[t])
    return stem.rstrip().replace('_','\_').replace(',',', ').replace('(','(\\allowbreak{}')

def render_occurred(occurred,t):
    return string.join([(str(x.args()[0])+": "+str(x.args()[1])+r"\\""\n").replace('_','\_').replace(',',', ').replace('(','(\\allowbreak{}') for x in occurred[t]], '')

def render_holdsat(holdsat,t,max):
    def prefix(x):
        p = r"\item"
        p = p+(r"\textbf{" if t==0 or (not x in holdsat[t-1]) else r"{")
        p = p+(r"\sout{" if t<max and (not x in holdsat[t+1]) else r"{")
        return p
    suffix = r"}}"
    if holdsat[t]==[]: return r"\item" # to avoid LaTeX "missing item" error
    return string.join([prefix(x)+(str(x.args()[0])+": "+str(x.args()[1])+suffix).replace('_','\_').replace(',',', ').replace('(','(\\allowbreak{}')+"\n" for x in holdsat[t]], '')

def parse_range(args,limit):
# code acquired from
# http://stackoverflow.com/questions/4248399/page-range-for-printing-algorithm
    astr = args.states
    states = set()
    events = set()
    for part in astr.split(','):
        x = part.split('-')
        states.update(range(int(x[0]),int(x[-1])+1))
        events.update(range(int(x[0]),int(x[-1])))
    # prevent state index greater than number of cycles
    while max(states)>limit:
        states.discard(max(states))
    while max(events)>max(states):
        events.discard(max(events))
    return sorted(states), sorted(events)

def instal_trace(args,answersets):
    name,ext = os.path.splitext(args.trace_file)
    for i in range(0,len(answersets)):
        if answersets[i]==[]: continue
        args.trace_file = name+str(i)+ext
        instal_trace_aset(args,observed,answersets[i])

def instal_trace_aset(args,answerset):
    # selective printing of states requires subsantial refactoring... not now (20160405)
    # but one contiguous subset seems safe (20160504)
    labels = {}
    states = {}
    tableWidth = "5cm"
    p = inflect.engine() # to provide translation of numbers to words
    selected_states, selected_events = parse_range(args,len(observed)) if args.states else (set(range(0,len(observed)+1)), set(range(0,len(observed))))
    [observed,occured,holdsat] = answerset
    if not(args.verbose): # cheap test to suppress perm/pow/ipow/gpow/tpow in trace
        for t in selected_states:
            holdsat[t] = filter(lambda x:
                                    not((x.args()[0]).name()
                                        in ["perm","pow","ipow","gpow","tpow"]),
                                holdsat[t])
    with open(args.trace_file,'w') as tfile:
        print(latex_trace_header,file=tfile)
        # define transition labels as macros \Ezero ...
        for t in selected_events:
            if not args.verbose: # to save sorting a sorted list...
                occurred[t] = sorted(occurred[t],
                                     key=lambda x: x.args()[0].name())
            labels[t] = (r"\newcommand{"+'\E{}'.format(p.number_to_words(t).replace('-',''))+
                         r"}{\begin{tabular}{>{\centering}m{\tableWidth}}""\n"
                         + render_observed(observed,t)
                         + r"\\""\n"r"\em "
                         + render_occurred(occurred,t)
                         + "\n"r"\end{tabular}}""\n")
            print(labels[t],file=tfile)
        # define state tables as macros \Szero ...
        for t in selected_states:
            if not args.verbose: # to save sorting a sorted list...
                holdsat[t] = sorted(holdsat[t],
                                    key=lambda x: x.args()[0].name())
            states[t] = (r"\newcommand{"+'\S{}'.format(p.number_to_words(t).replace('-',''))+
                         r"}{\begin{minipage}{\tableWidth}"
                         r"\raggedright"
                         r"\begin{description}[align=left,leftmargin=1em,noitemsep,labelsep=\parindent]""\n"
                         + render_holdsat(holdsat,t,max(selected_states))
                         + r"\end{description}\end{minipage}}""\n")
            print(states[t],file=tfile)
        # output trace as a tikzpicture in resizebox in a longtable
        print(r"\newlength{\tableWidth}""\n"
              + "\\setlength{{\\tableWidth}}{{{tw}}}\n".format(tw=tableWidth)
              + r"\begin{longtable}{@{}l@{}}""\n"
              r"\resizebox{\textwidth}{!}{""\n"
              r"\begin{tikzpicture}""\n"
              "[\nstart chain=trace going right,",file=tfile)
        for t in selected_states:
            print("start chain=state{} going down,".format(t),file=tfile)
        print("node distance=1cm and 5.2cm""\n]"
          "\n{{ [continue chain=trace]",file=tfile)
        for t in selected_states:
            print(r"\node[circle,draw,on chain=trace]"
                  + "(i{i}) {{$S_{{{i}}}$}};".format(i=t),file=tfile)
        for t in selected_states:
            print("{{ [continue chain=state{i} going below]\n"
                  "\\node [on chain=state{i},below=of i{i},"
                  "rectangle,draw,inner frame sep=0pt] (s{i}) {{".format(i=t)
                  + r'\S{i}'.format(i=p.number_to_words(t).replace('-',''))
                  + "};} % end node and chain\n"
                  + r"\draw (i{}) -- (s{});".format(t,t),file=tfile)
        print(r"}}",file=tfile)
        # output lines between states labelled with events observed/occurred
        for t in selected_events:
            print(r"\draw[-latex,thin](i{x}) -- node[above]{{\E{y}}}(i{z});"
                  .format(x=t,y=p.number_to_words(t).replace('-',''),z=t+1),file=tfile)
        # end tikzpicture/resizebox/table
        print(r"\end{tikzpicture}}\\""\n"
              r"\end{longtable}""\n"
              r"\end{document}",file=tfile)

# def instal_text(args,trace):
#     with open(args.text_file,'w') as tfile:
# 	for i in range(1,len(trace)):
# 		t = trace[i]
# 		print(json_dict_to_string(t)+"\n", file=tfile)
        
def instal_text(args,answersets):
    name,ext = os.path.splitext(args.text_file)
    for i in range(0,len(answersets)):
        if answersets[i]==[]: continue
        args.text_file = name+str(i)+ext
        instal_text_aset(args,answersets[i])

def instal_text_aset(args,answerset):
    howmany = answerset[0][0]  
    selected_states, selected_events = parse_range(args,len(howmany)) if args.states else (set(range(0,len(howmany)+1)), set(range(0,len(howmany))))
    with open(args.text_file,'w') as tfile:
        sys.stdout = tfile
        [observed,occurred,holdsat] = answerset
        for t in selected_events:
            # print(observed[t][0])
            for x in occurred[t]: print(x)
            if t in selected_states:
                for x in holdsat[t]: print(x)
    sys.stdout = sys.__stdout__

latex_gannt_header = r"""
\documentclass{article}
\usepackage{graphicx}
\usepackage{tikz}
\usepackage{pgfgantt}
\usepackage{longtable}
\usepackage[margin=1cm]{geometry}
\pagestyle{empty}
\thispagestyle{empty}
\renewcommand*\familydefault{\sfdefault} %% Only if the base font of the document is to be sans serif
\begin{document}
"""

def invert(d):
    result = defaultdict(list)
    for k in d:
        for v in d[k]:
            result[v]=result[v]+[k]
    return result

def instal_gantt(args,observed,occurred,holdsat):
    if not(args.verbose): # cheap test to suppress perm/pow/ipow/gpow in trace
        for t in range(0,len(observed)+1):
            holdsat[t] = filter(lambda x:
                                    not((x.args()[0]).name()
                                        in ["perm","pow","ipow","gpow"]),
                                holdsat[t])
    with open(args.gantt_file,'w') as tfile:
        print(latex_gannt_header,file=tfile)
        print(r"\begin{longtable}{@{}r@{}}""\n",file=tfile)
        # set each chart fragment as a line in longtable to be breakable over page boundaries
        for t in range(1,len(observed)+1):
            if occurred[t]==[]: continue # ought not to happen
            print(r"\begin{ganttchart}[hgrid,vgrid,canvas/.style={draw=none},bar/.append style={fill=gray},x unit=0.5cm,y unit chart=0.5cm]{0}" +
                  "{{{t}}}\n".format(t=len(observed)+1),file=tfile)
            for x in occurred[t][:-1]:
                l = (str(x.args()[0])+": "+str(x.args()[1])).replace('_','\_')
                print("\\ganttmilestone{{{l}}}{{{f}}}\\ganttnewline"
                      .format(l=l,f=t-1),file=tfile)
            # handle last event separately to drop \ganttnewline
            x = occurred[t][-1]
            l = (str(x.args()[0])+": "+str(x.args()[1])).replace('_','\_')
            print("\\ganttmilestone{{{l}}}{{{f}}}"
                  .format(l=l,f=t-1),file=tfile)
            print(r"\end{ganttchart}\\[-0.7em]""\n",file=tfile)
        facts = invert(holdsat)
        keys = sorted(facts,key=lambda x: x.args()[0].name())
        for f in keys:
            print(r"\begin{ganttchart}[hgrid,vgrid,canvas/.style={draw=none},bar/.append style={fill=gray},x unit=0.5cm,y unit chart=0.5cm]{0}" +
                  "{{{t}}}\n".format(t=len(observed)+1),file=tfile)
            i = facts[f][0]
            l = (str(f.args()[0])+": "+str(f.args()[1])).replace('_','\_')
            print("\\ganttbar{{{label}}}{{{start}}}{{{finish}}}"
                  .format(label=l,start=i,finish=i),file=tfile)
            for t in facts[f][1:]:
                print("\\ganttbar{{}}{{{start}}}{{{finish}}}"
                      .format(start=t,finish=t),file=tfile)
            print(r"\end{ganttchart}\\[-0.7em]""\n",file=tfile)
        print(r"\end{longtable}""\n"
              r"\end{document}",file=tfile)

def instal_trace_preprocess_with_args(args,unk):
    if not args.json_file: exit(-1)
    if not(args.trace_file or args.gantt_file or args.text_file): exit(-1)
    trace = []
    with open(args.json_file,'r') as jsonfile:
        for l in jsonfile.readlines():
            trace += [json.loads(l,object_hook=as_Fun)]
    check_trace_integrity(trace)
    observed = {t-1: trace[t]['state']['observed'] for t in range(1,len(trace))}
    occurred = defaultdict(list)
    for t in range(1,len(trace)): occurred[t-1] = trace[t]['state']['occurred']
    holdsat = defaultdict(list)
    for t in range(0,len(trace)): holdsat[t] = trace[t]['state']['holdsat']
    if args.trace_file: instal_trace(args,observed,occurred,holdsat)
    if args.gantt_file: instal_gantt(args,observed,occurred,holdsat)
    if args.text_file: instal_text(args,trace)

def instal_trace_preprocess():
    argparser = buildargparser()
    # got following line from http://stackoverflow.com/questions/1450393/how-do-you-read-from-stdin-in-python
    # which allows fileinput and argparse to co-exist, but might be better to use .REMAINDER
    args,unk = argparser.parse_known_args()
    instal_trace_preprocess_with_args(args,unk)

if __name__=="__main__": 
    instal_trace_preprocess()


