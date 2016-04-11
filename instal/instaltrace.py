#!/usr/bin/python
#------------------------------------------------------------------------
# REVISION HISTORY:
# 20160325 JAP: created file

from __future__ import print_function
import string
import inflect
import sys

latex_header = r"""
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
\usepackage{pgfgantt}
\renewcommand*\familydefault{\sfdefault} %% Only if the base font of the document is to be sans serif
% \usepackage[T1]{fontenc}
\usepackage[normalem]{ulem}
\begin{document}
"""

def instal_trace(args,sensor,observed,occurred,holdsat):
    labels = {}
    states = {}
    tableWidth = "5cm"
    p = inflect.engine()
    with open(args.trace_file,'w') as tfile:
        sys.stdout = tfile
        print(latex_header)
        # define transition labels as macros \Eone ...
        for t in range(1,sensor.cycle+1): 
            labels[t] = (r"\newcommand{"+'\E{}'.format(p.number_to_words(t).replace('-',''))+r"}{\begin{tabular}{>{\centering}m{\tableWidth}}""\n"
                         + str(observed[t]).rstrip().replace('_','\_').replace(',',', ').replace('(','(\\allowbreak{}')
                         + r"\\""\n"r"\em "
                         + string.join(map(str,occurred[t]),r"\\""\n").replace('_','\_').replace(',',', ').replace('(','(\\allowbreak{}')
                         + "\n"r"\end{tabular}}""\n")
            print(labels[t])
        # define state tables as macros \Sone ...
        for t in range(0,sensor.cycle+1): 
            states[t] = (r"\newcommand{"+'\S{}'.format(p.number_to_words(t).replace('-',''))+r"}{\begin{minipage}{\tableWidth}"
                         r"\raggedright"
                         r"\begin{description}[align=left,leftmargin=1em,noitemsep,labelsep=\parindent]""\n"
                         + string.join([r"\item "+(str(x.args()[0])+": "+str(x.args()[1])).replace('_','\_').replace(',',', ').replace('(','(\\allowbreak{}')+"\n" for x in sorted(holdsat[t])], '')
                         + r"\end{description}\end{minipage}}""\n")
            print(states[t])
        # output trace as a tikzpicture in resizebox in a table
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
