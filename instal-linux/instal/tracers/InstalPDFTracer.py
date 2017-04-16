
import string

from collections import defaultdict
import inflect

from .InstalTracer import InstalTracer


class InstalPDFTracer(InstalTracer):
    """
        InstalPDFTracer
        Implementation of ABC InstalTracer for pdf output.
    """
    # TODO: This crashes when there are no fluents to print

    def trace_to_file(self, remove_permpows=True):
        def render_holdsat(holds, time, maximum):
            def prefix(x):
                holdsat_p = r"\item"
                holdsat_p += r"\textbf{" if time == 0 or (
                    not x in holds[time - 1]) else r"{"
                holdsat_p += r"\sout{" if time < maximum and (
                    not x in holds[time + 1]) else r"{"
                return holdsat_p

            suffix = r"}}"
            if not holds[time]:  # 20170301 JAP: not sure if test ever succeeds
                return r"\item"  # to avoid LaTeX "missing item" error
            returnVal = ""
            for x in holds[time]:
                returnVal += (prefix(x) + (str(x.arguments[0]) + ": " + str(x.arguments[1]) + suffix).replace('_', '\_').replace(
                    ',', ', ').replace('(', '(\\allowbreak{}') + "\n")
            return returnVal

        def render_observed(observed_p, time):
            stem = ""
            obs = observed_p[time]
            if len(obs) != 1:
                return
            else:
                obs = obs[0]
            if obs.name == "observed":
                stem = str(obs.arguments[0])
            else:
                print("% Unrecognised observation", observed_p[time])
            return stem.rstrip().replace('_', '\_').replace(',', ', ').replace('(', '(\\allowbreak{}')

        def render_occurred(occurred_p, time):
            returnVal = ""
            for x in occurred_p[time]:
                returnVal += (str(x.arguments[0]) + ": " + str(x.arguments[1]) + r"\\""\n").replace('_', '\_').replace(',',
                                                                                                                       ', ').replace(
                    '(', '(\\allowbreak{}')
            return returnVal

        latex_trace_header = r"""
        \documentclass{article}
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
        \renewcommand*\familydefault{\sfdefault} %% Only if the base font of the document is to be sans serif
        \usepackage[normalem]{ulem}
        \newenvironment{events}
        {\begin{tabular}{>{\centering}m{\tableWidth}}}
        {\end{tabular}}
        \newenvironment{states}
        {\begin{minipage}{\tableWidth}\raggedright\begin{description}[align=left,leftmargin=1em,noitemsep,labelsep=\parindent]}
        {\end{description}\end{minipage}}
        \begin{document}
        """
        observed = {t - 1: self.trace[t]['state']['observed']
                    for t in range(1, len(self.trace))}
        occurred = defaultdict(list)
        for t in range(1, len(self.trace)):
            occurred[t - 1] = self.trace[t]['state']['occurred']
        holdsat = defaultdict(list)
        for t in range(0, len(self.trace)):
            holdsat[t] = self.trace[t]['state']['holdsat']

        labels = {}
        states = {}
        tableWidth = "5cm"
        p = inflect.engine()  # to provide translation of numbers to words
        selected_states, selected_events = (
            set(range(0, len(observed) + 1)), set(range(0, len(observed))))
        if remove_permpows:  # cheap test to suppress perm/pow/ipow/gpow/tpow in trace
            for t in selected_states:
                holdsat[t] = filter(lambda x:
                                    not ((x.arguments[0]).name
                                         in ["perm", "pow", "ipow", "gpow", "tpow"]),
                                    holdsat[t])
        with open(self.output_file_name, 'w') as tfile:
            print(latex_trace_header, file=tfile)
            # define transition labels as macros \Ezero ...
            print("% Event macro definitions",file=tfile)
            print("% ------------------------------------------------------------------------",file=tfile)
            for t in selected_events:
                if not remove_permpows:  # to save sorting a sorted list...
                    occurred[t] = sorted(occurred[t],
                                         key=lambda x: x.arguments[0].name)
                labels[t] = (r"\newcommand{" + '\E{}'.format(p.number_to_words(t).replace('-', '')) +
                             r"}{\begin{events}""\n"
                             + render_observed(observed, t)
                             + r"\\""\n"r"\em "
                             + render_occurred(occurred, t)
                             + r"\end{events}}""\n")
                print(labels[t], file=tfile)
            # define state tables as macros \Szero ...
            print("% State macro definitions",file=tfile)
            print("% ------------------------------------------------------------------------",file=tfile)
            for t in selected_states:
                if not remove_permpows:  # to save sorting a sorted list...
                    holdsat[t] = sorted(holdsat[t],
                                        key=lambda x: x.arguments[0].name)
                fluents = render_holdsat(holdsat, t, max(selected_states))
                states[t] = (r"\newcommand{"
                             + '\S{}'.format(p.number_to_words(t).replace('-', '')))
                if fluents=="":
                    states[t] = states[t] + r"}{$\emptyset$}""\n"
                else:
                    states[t] = (states[t]
                                 + r"}{\begin{states}""\n"
                                 + fluents
                                 + r"\end{states}}""\n")
                print(states[t], file=tfile)
            # output trace as a tikzpicture in resizebox in a longtable
            print("% Institutional trace",file=tfile)
            print("% ------------------------------------------------------------------------",file=tfile)
            print(r"\newlength{\tableWidth}""\n"
                  + "\\setlength{{\\tableWidth}}{{{tw}}}\n\n".format(tw=tableWidth)
                  + r"\begin{longtable}{@{}l@{}}""\n"
                    r"\resizebox{\textwidth}{!}{""\n"
                    r"\begin{tikzpicture}""\n"
                    "[\nstart chain=trace going right,", file=tfile)
            for t in selected_states:
                print("start chain=state{} going down,".format(t), file=tfile)
            print("node distance=1cm and 5.2cm""\n]"
                  "\n{{ [continue chain=trace]", file=tfile)
            for t in selected_states:
                print(r"\node[circle,draw,on chain=trace]"
                      + "(i{i}) {{$S_{{{i}}}$}};".format(i=t), file=tfile)
            for t in selected_states:
                print("{{ [continue chain=state{i} going below]\n"
                      "\\node [on chain=state{i},below=of i{i},"
                      "rectangle,draw,inner frame sep=0pt] (s{i}) {{".format(
                          i=t)
                      + r'\S{i}'.format(i=p.number_to_words(t).replace('-', ''))
                      + "};} % end node and chain\n"
                      + r"\draw (i{}) -- (s{});".format(t, t), file=tfile)
            print(r"}}", file=tfile)
            # output lines between states labelled with events
            # observed/occurred
            for t in selected_events:
                print(r"\draw[-latex,thin](i{x}) -- node[above]{{\E{y}}}(i{z});"
                      .format(x=t, y=p.number_to_words(t).replace('-', ''), z=t + 1), file=tfile)
            # end tikzpicture/resizebox/table
            print(r'\end{tikzpicture}}'"\n"
                  r"\end{longtable}""\n"
                  r"\end{document}", file=tfile)
