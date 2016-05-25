#!/usr/bin/python
#------------------------------------------------------------------------
# REVISION HISTORY:

# 20160415 JAP: changed render_observed to account for observed/compObserved unification
# 20160405 JAP: add render_observed and differentiate observed/compObserved
#               add Gantt-style trace output, suppressed overprint in ganntbar
# 20160330 JAP: bold for new fluents, sout for deleted
# 20160325 JAP: created file

from __future__ import print_function
import string
import inflect
import sys
from gringo import Fun
from collections import defaultdict

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

def render_observed(observed,t):
    stem = ""
    if observed[t].name()=="observed":
        stem = str(observed[t].args()[0])
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

def parse_range(args,sensor):
# code acquired from
# http://stackoverflow.com/questions/4248399/page-range-for-printing-algorithm
    astr = args.states
    result=set()
    for part in astr.split(','):
        x=part.split('-')
        result.update(range(int(x[0]),int(x[-1])+1))
    # prevent state index greater than number of cycles
    while max(result)>sensor.cycle:
        result.discard(max(result))
    return sorted(result)

def instal_trace(args,sensor,observed,occurred,holdsat):
    # selective printing of states requires subsantial refactoring... not now (20160405)
    # selected_states = parse_range(args,sensor) if args.states else set(range(0,sensor.cycle+1))
    labels = {}
    states = {}
    tableWidth = "5cm"
    p = inflect.engine() # to provide translation of numbers to words
    if not(args.verbose): # cheap test to suppress perm/pow/ipow/gpow in trace
        for t in range(0,sensor.cycle+1):
            holdsat[t] = filter(lambda x:
                                    not((x.args()[0]).name()
                                        in ["perm","pow","ipow","gpow"]),
                                holdsat[t])
    with open(args.trace_file,'w') as tfile:
        sys.stdout = tfile
        print(latex_trace_header)
        # define transition labels as macros \Eone ...
        for t in range(1,sensor.cycle+1): 
            if t<1: continue
            if not args.verbose: # to save sorting a sorted list...
                occurred[t] = sorted(occurred[t],
                                     key=lambda x: x.args()[0].name())
            labels[t] = (r"\newcommand{"+'\E{}'.format(p.number_to_words(t).replace('-',''))+r"}{\begin{tabular}{>{\centering}m{\tableWidth}}""\n"
                         + render_observed(observed,t)
                         + r"\\""\n"r"\em "
                         + render_occurred(occurred,t)
                         + "\n"r"\end{tabular}}""\n")
            print(labels[t])
        # define state tables as macros \Sone ...
        for t in range(0,sensor.cycle+1): 
            if not args.verbose: # to save sorting a sorted list...
                holdsat[t] = sorted(holdsat[t],
                                    key=lambda x: x.args()[0].name())
            states[t] = (r"\newcommand{"+'\S{}'.format(p.number_to_words(t).replace('-',''))+r"}{\begin{minipage}{\tableWidth}"
                         r"\raggedright"
                         r"\begin{description}[align=left,leftmargin=1em,noitemsep,labelsep=\parindent]""\n"
                         + render_holdsat(holdsat,t,sensor.cycle)
                         + r"\end{description}\end{minipage}}""\n")
            print(states[t])
        # output trace as a tikzpicture in resizebox in a longtable
        print(r"\newlength{\tableWidth}""\n"
              + "\\setlength{{\\tableWidth}}{{{tw}}}\n".format(tw=tableWidth)
              + r"\begin{longtable}{@{}l@{}}""\n"
              r"\resizebox{\textwidth}{!}{""\n"
              r"\begin{tikzpicture}""\n"
              "[\nstart chain=trace going right,")
        for t in range(0,sensor.cycle+1):
            print("start chain=state{} going down,".format(t))
        print("node distance=1cm and 5.2cm""\n]"
          "\n{{ [continue chain=trace]")
        for t in range(0,sensor.cycle+1):
            print(r"\node[circle,draw,on chain=trace]"
                  + "(i{i}) {{$S_{{{i}}}$}};".format(i=t))
        for t in range(0,sensor.cycle+1):
            print("{{ [continue chain=state{i} going below]\n"
                  "\\node [on chain=state{i},below=of i{i},"
                  "rectangle,draw,inner frame sep=0pt] (s{i}) {{".format(i=t)
                  + r'\S{i}'.format(i=p.number_to_words(t))
                  + "};} % end node and chain\n"
                  + r"\draw (i{}) -- (s{});".format(t,t))
        print(r"}}")
        # output lines between states labelled with events observed/occurred
        for t in range(1,sensor.cycle+1):
            print(r"\draw[-latex,thin](i{x}) -- node[above]{{\E{y}}}(i{z});"
                  .format(x=t-1,y=p.number_to_words(t),z=t))
        # end tikzpicture/resizebox/table
        print(r"\end{tikzpicture}}\\""\n"
              r"\end{longtable}""\n"
              r"\end{document}")
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

def instal_gantt(args,sensor,observed,occurred,holdsat):
    if not(args.verbose): # cheap test to suppress perm/pow/ipow/gpow in trace
        for t in range(0,sensor.cycle+1):
            holdsat[t] = filter(lambda x:
                                    not((x.args()[0]).name()
                                        in ["perm","pow","ipow","gpow"]),
                                holdsat[t])
    with open(args.gantt_file,'w') as tfile:
        sys.stdout = tfile
        print(latex_gannt_header)
        print(r"\begin{longtable}{@{}r@{}}""\n")
        # set each chart fragment as a line in longtable to be breakable over page boundaries
        for t in range(1,sensor.cycle+1):
            if occurred[t]==[]: continue # ought not to happen
            print(r"\begin{ganttchart}[hgrid,vgrid,canvas/.style={draw=none},bar/.append style={fill=gray},x unit=0.5cm,y unit chart=0.5cm]{0}" +
                  "{{{t}}}\n".format(t=sensor.cycle+1))
            for x in occurred[t][:-1]:
                l = (str(x.args()[0])+": "+str(x.args()[1])).replace('_','\_')
                print("\\ganttmilestone{{{l}}}{{{f}}}\\ganttnewline"
                      .format(l=l,f=t-1))
            # handle last event separately to drop \ganttnewline
            x = occurred[t][-1]
            l = (str(x.args()[0])+": "+str(x.args()[1])).replace('_','\_')
            print("\\ganttmilestone{{{l}}}{{{f}}}"
                  .format(l=l,f=t-1))
            print(r"\end{ganttchart}\\[-0.7em]""\n")
        facts = invert(holdsat)
        keys = sorted(facts,key=lambda x: x.args()[0].name())
        for f in keys:
            print(r"\begin{ganttchart}[hgrid,vgrid,canvas/.style={draw=none},bar/.append style={fill=gray},x unit=0.5cm,y unit chart=0.5cm]{0}" +
                  "{{{t}}}\n".format(t=sensor.cycle+1))
            i = facts[f][0]
            l = (str(f.args()[0])+": "+str(f.args()[1])).replace('_','\_')
            print("\\ganttbar{{{label}}}{{{start}}}{{{finish}}}"
                  .format(label=l,start=i,finish=i))
            for t in facts[f][1:]:
                print("\\ganttbar{{}}{{{start}}}{{{finish}}}"
                      .format(start=t,finish=t))
            print(r"\end{ganttchart}\\[-0.7em]""\n")
        print(r"\end{longtable}""\n"
              r"\end{document}")
    sys.stdout = sys.__stdout__
