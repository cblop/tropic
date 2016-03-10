#!/usr/bin/python

#------------------------------------------------------------------------
# REVISION HISTORY
# add new entries here at the top tagged by date and initials
# JAP 20140810: add tableWidth parameter to specify width in cm of state
# JAP 20140723: fixed off-by-one error in number of states
# JAP 20140723: rewrote indentation of state tables to use description list
#               from enumitem package after observing problems with everypar
#               + hangindent solution 
# JAP 20140521: revised processing of multi-row display
#               added selection and display of state ranges
# JAP 20140520: revised event/fluent processing to handle institution parameter
#               suppressed printing of null events
#               allow line breaks after left parenthesis in fluents
# JAP 20130801: reorganized fluent table layout: initiated at top
#               terminated at the bottom
# GDB 201305??: added input file argument and consequent changes
# GDB/JAP?????: changed main loop to iterate over occurred not holdsat
# JAP 20130??: first version (approx)

from __future__ import print_function
import re
import sys
import ply.lex as lex
from collections import defaultdict
import string
from itertools import izip
from itertools import count
import argparse
from math import ceil

class myLexer():

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

def pyvizError(s):
    print(s,file=sys.stderr)

observed = defaultdict(list)
holdsat = defaultdict(list)
initiated = defaultdict(list)
terminated = defaultdict(list)
occurred = defaultdict(list)

def chunks(l, n):
    """ Yield successive n-sized chunks from l.
    """
    for i in xrange(0, len(l), n):
        yield l[i:i+n]

# command line arguments

def parse_range(astr):
# code acquired from
# http://stackoverflow.com/questions/4248399/page-range-for-printing-algorithm
    result=set()
    for part in astr.split(','):
        x=part.split('-')
        result.update(range(int(x[0]),int(x[-1])+1))
    return sorted(result)

def invert(d):
    return dict( (v,k) for k in d for v in d[k] )

def arb(s): return s

parser = argparse.ArgumentParser()
parser.add_argument("-a", "--answer-set", type=arb,
                    help="specify answer set (default 1)")
# GDB 20130430  
parser.add_argument("-i", "--answerset-file", type=arb, 
                    help="specify answer set file")
# JAP 20130801
parser.add_argument("-w", "--width", type=int,
                    help="specify number of states per row (default all)")

# JAP 20140520
parser.add_argument("-s", "--states", type=arb,
                    help="specify which states to display (default all)")

# JAP 20140810
parser.add_argument("-tw", "--table-width", type=arb,
                    help="specify width of state table (default 5cm)")

args=parser.parse_args()
displayWidth = 0

answer_set="1"
if args.answer_set:
    answer_set = args.answer_set
# GDB 20130430  
if args.answerset_file:
    f = open(args.answerset_file,'r')
# JAP 20130801
if args.width:
    displayWidth = args.width
    if displayWidth<0: displayWidth = 0
# JAP 20140810
tableWidth = args.table_width if args.table_width else "5cm"

document = ""

if args.answerset_file:
    document = f #document + f.read(-1)
else:
    document = sys.stdin #document + sys.stdin.read(-1)
#debug('line:',document)

global found
found=False
mylex=myLexer()
for line in document:#sys.stdin:
    if re.match("Answer: {n}".format(n=answer_set),line): break
for line in document:#sys.stdin:
    # split line into terms so that process can group output about each
    # mechanism found
    found = True
    for term in re.split(' ',line):
        mylex.lexer.input(term)
        l = [tok.value for tok in mylex.lexer]
        # print("tok.value = ",l)
        if l==[]: continue # skip blanks
        if l[0] in ['holdsat','observed','initiated','terminated','occurred']:
            # some rather tacky dead-reckoning
            # l[0] = term, used as key
            # l[1] = LPAR; skip
            # l[2:-6] = content associated with key
            # l[-5] = COMMA; skip
            # l[-4] = institution name
            # l[-3] = COMMA; skip
            # l[-2] = instant; assumed integer
            # l[-1] = RPAR; matches l[1]; skip
            what = string.join(l[2:-5],'').replace('_','\_').replace(',',', ').replace('(','(\\allowbreak{}') # allows line breaks after a left paren
            where = l[-4]
            when = int(l[-2])
            # print(what,where,when)
            if l[0]=='holdsat':
                # processHoldsat(l)
                holdsat[when].append(what+": "+where)
            elif l[0]=='observed':
                # processObserved(l)
                observed[when].append(what+": "+where)
            elif l[0]=='initiated':
                # processInitiated(l)
                initiated[when].append(what+": "+where)
            elif l[0]=='terminated':
                # processTerminated(l)
                terminated[when].append(what+": "+where)
            elif l[0]=='occurred':
                # processOccurred(l)
                occurred[when].append(what+": "+where) if what!='null' else False
        else:
            print("% skipping \"{term}\""
                  .format(term=string.join(l,'')))
    break # stop after specified answer set
if not found:
    print("Answer set {n} not found\n".format(n=answer_set))
    exit(-1)

# establish how many states there are
event_count=max(len(occurred),len(observed))
inst_count=max(len(holdsat),len(initiated),len(terminated))
# note: default selected states extended by 1 to account for nth event
# leading to n+1th state
selected_states = parse_range(args.states) if args.states else set(range(0,max(event_count,inst_count)))
nstates=len(selected_states)
displayWidth=nstates if displayWidth==0 else displayWidth

prologue = \
"\\documentclass{article}\n"\
"\\usepackage{graphicx}\n"\
"\\usepackage{tikz}\n"\
"\\usepackage{pgfgantt}\n"\
"\\begin{document}\n"

epilogue = \
"\\end{document}\n"

# print(prologue)

print("\\resizebox{!}{\\textwidth}{\n\\begin{tikzpicture}[x=0.5cm, y=0.5cm]\n" +
      "\\begin{ganttchart}[hgrid,vgrid,bar/.append style={fill=gray},x unit=0.5cm,y unit chart=0.5cm]{0}" + "{{{t}}}\n".format(t=max(inst_count,event_count)) +
      "\gantttitlelist{{0,...,{t}}}{{1}} \\\\".format(t=max(inst_count,event_count))
      )

inv_terminated=invert(terminated)
for x in holdsat[0]:
    print("% initially",0,x)
    print("\\ganttbar{{{l}}}{{{f}}}{{{t}}}\\\\"
          .format(l=x,f=0,t=(inv_terminated[x] if x in inv_terminated else max(inst_count,event_count))))

for i in range(0,max(event_count,inst_count)+1):
    for x in occurred[i]:
        print("% observed",i,":",x)
        print("\\ganttmilestone{{{l}}}{{{f}}}\\\\"
              .format(l=x,f=i-1))

for i in range(0,max(event_count,inst_count)+1):
    for x in initiated[i]:
        print("% init",i,":",x)
        print("\\ganttbar{{{l}}}{{{f}}}{{{t}}}\\\\"
              .format(l=x,f=i,t=(inv_terminated[x] if x in inv_terminated else inst_count)))

print("\\end{ganttchart}\n"
      "\\end{tikzpicture}}\n")

# print(epilogue)

exit(0)

#------------------------------------------------------------------------

print("% events = {e}\n% states = {s}\n% nstates = {n}\n% display width = {w}"
      .format(e=event_count,s=inst_count,n=nstates,w=displayWidth))
print(  "\\newlength{\\tableWidth}\n"
      + "\\setlength{{\\tableWidth}}{{{tw}}}\n"
      .format(tw=tableWidth))
print("\\newlength{\\dummyOffset}\n"
      "\\setlength{\\dummyOffset}{\\tableWidth+0.6cm}\n"
      "\\newlength{\\horizontalOffset}\n"
      "\\setlength{\\horizontalOffset}{\\tableWidth+0.2cm}\n"
      "\\newlength{\\labelOffset}\n"
      "\\setlength{\\labelOffset}{\\tableWidth/2+1cm}\n")

labels = {}
states = {}

# set up transition labels and state tables

# note: loop extended by 1 to account for nth event leading to n+1th state
for t in range(0,max(event_count,inst_count)+1): 
    # events for each transition
    labels[t] = ("{\\begin{tabular}{>{\centering}m{\\tableWidth}}\n"
                 + string.join(observed[t-1],"\\\\\n")
                 + "\\\\\n\\em "
                 + string.join(occurred[t-1],"\\\\\n ")
                 + "\n\\end{tabular}}")
    # fluents for each state
    states[t] = ("\\begin{minipage}{\\tableWidth}"
                 "\\raggedright"
                 # "\everypar={\hangindent=1em\hangafter=1}\n"
                 "\\begin{description}[align=left,leftmargin=1em,noitemsep,labelsep=\\parindent]"
                 # do initiated fluents first
                 + string.join(
            ["" if (t>0) and
             ((x in holdsat[t-1]) or (x in initiated[t-1])) else
             "\\item \\textbf{"+x+"}\n" # bold new fluents
             for x in sorted(holdsat[t]) if x not in terminated[t]],'')
                 + string.join(
            ["\\item \\textbf{"+x+"}\n" for x in sorted(initiated[t])],'')
                 # then inertial ones
                 + string.join(
            ["\\item "+x+"\n" if (t>0) and
             ((x in holdsat[t-1]) or (x in initiated[t-1])) else
             "" #\\textbf{"+x+"}\\\\\n" # bold new fluents
             for x in sorted(holdsat[t]) if x not in terminated[t]],'')
                 # finally terminated ones
                 + string.join(
            ["\\item \\sout{"+x+"}\n" for x in sorted(terminated[t])],'')
                 + "\\end{description}\n\\end{minipage}\n};")

states_by_row = list(chunks(list(selected_states),displayWidth))
print("% states_by_row = {n}\n".format(n=states_by_row))
print("\\begin{longtable}{@{}l@{}}")
for r in states_by_row:
    print("% start row={r} of {m}\n".format(r=r,m=states_by_row))
    print("\\resizebox{\\textwidth}{!}{\n")
    print("\\begin{tikzpicture}\n"
          "[\nstart chain=trace going right,")
    # set up state chains
    print("% state chains for {i} through {j}"
          .format(i=r[0],j=r[-1]))
    for t in r:
        print("start chain=state{i} going down,"
              .format(i=t))
    print("node distance=1cm and \\horizontalOffset\n]")
    for (k,t) in enumerate(r): 
        print("% start row={r}, state={t}"
              .format(r=r,t=t))
        print("{{{{ [continue chain=trace]\n"
              "\\node[circle,draw,on chain=trace]"
              "(i{i}) {{$S_{{{i}}}$}};"
              .format(i=t))
        if (t==r[0]): # first element of row
            if (r==states_by_row[0]): # first element of first row
                # dummy node to left of S0
                print("\draw[color=white](i{i})+(180:\\dummyOffset) --"
                      "node[above]{{}}(i{i});"
                      .format(i=t))
                # provenance of trace
                print("\\draw(i{i})+(-\\labelOffset,0)node[rotate=90,anchor=south]"
                      "{{Answer set={a}, source={f}}};"
                      .format(
                        i=t,
                        a=answer_set,
                        f=args.answerset_file.replace('_','\_') if args.answerset_file
                        else 'stdin'))
            else:
                print("\draw[-latex,dashed](i{i})+(180:\\horizontalOffset) --"
                      "node[above]{l}(i{i});"
                      .format(i=t,l=labels[t]))
        else:
            # transitions + event labels
            print("% label for s_{i} -- s_{j}\n"
                  "\draw[-latex,{style}](i{i}) -- % t={j}\n"
                  "node[above]{l}\n(i{j});"
                  # r[k-1] is index of preceding node in chain
                  .format(i=r[k-1],j=t,l=labels[t],
                          # highlight the discontinuity
                          style='thin' if t-1==r[k-1] else 'dotted')) 
        print("}") # close first brace of continue chain
        # check there is some state to display
        if max(len(holdsat[t]),len(initiated[t]),len(terminated[t]))>0:
            print("{{ [continue chain=state{i} going below]\n"
                  "\\node [on chain=state{i},below=of i{i},"
                  "rectangle,draw,inner frame sep=0pt] (s{i}) {{\n"
                  "% instant {i}\n".format(i=t)
                  + states[t] # insert state table
                  + "\n} % end node and chain\n"
                  + "\draw (i{i}) -- (s{i});\n".format(i=t))
        print("}") # close second brace of continue chain
        print("% \pause % uncomment here to animate\n")
        # last element, intermediate row
        if ((t==r[-1]) and (r!=states_by_row[-1])):
            print("{{ [continue chain=trace]\n"
                  "\\node[on chain=trace] (i{j}) {{}};\n"
                  "\\draw[-latex,dashed](i{i}) -- \n".format(i=t,j=t+1)
                  + "node[above]"
                  + "{}" # labels[t+1]
                  + "(i{j});\n}}".format(i=t,j=t+1))
        # last element, last row
        if ((t==r[-1]) and (r==states_by_row[-1])):
            # prints nodes and final arc in white so final line scaling
            # matches preceding lines
            print("% fill nodes {a} to {b}\n"
                  .format(a=t+1,b=t+(displayWidth-len(r))))
            for x in range(t+1,t+(displayWidth-len(r))+1):
                print("% dummy node {x} to complete row".format(x=x))
                print("{{{{ [continue chain=trace]\n"
                      "\\node[color=white,circle,draw,on chain=trace]"
                      "(i{i}) {{$S_{{{i}}}$}};}}}}"
                      .format(i=x))
            x = t+(displayWidth-len(r))
            print("% dummy arc to complete row")
            print("{{ [continue chain=trace]\n"
                  "\\node[on chain=trace] (i{j}) {{}};\n"
                  "\\draw[color=white,-latex,dashed](i{i}) -- (i{j});\n}}"
                  .format(i=x,j=x+1))
    # bottom of row loop
    print("% end row={r} of {m}\n".format(r=r,m=states_by_row))
    print("\\end{tikzpicture}\n"
          "% close resizebox\n}\\\\\n")
print("\\end{longtable}\n")

if args.answerset_file: f.close()
    
