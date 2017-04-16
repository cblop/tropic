from collections import defaultdict

from .InstalTracer import InstalTracer


class InstalGanttTracer(InstalTracer):
    """
        InstalGanttTracer
        Implementation of ABC InstalTracer for gantt output.
    """

    def trace_to_file(self, remove_permpows=True):
        def invert(d):
            result = defaultdict(list)
            for k in d:
                for v in d[k]:
                    result[v] = result[v] + [k]
            return result

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
        observed = {t - 1: self.trace[t]['state']['observed']
                    for t in range(1, len(self.trace))}
        occurred = defaultdict(list)
        for t in range(1, len(self.trace)):
            occurred[t - 1] = self.trace[t]['state']['occurred']
        holdsat = defaultdict(list)
        for t in range(0, len(self.trace)):
            holdsat[t] = self.trace[t]['state']['holdsat']
        if remove_permpows:
            for t in range(0, len(observed) + 1):
                holdsat[t] = filter(lambda atom:
                                    not ((atom.arguments[0]).name
                                         in ["perm", "pow", "ipow", "gpow"]),
                                    holdsat[t])
        with open(self.output_file_name, 'w') as tfile:
            print(latex_gannt_header, file=tfile)
            print(r"\begin{longtable}{@{}r@{}}""\n", file=tfile)
            # set each chart fragment as a line in longtable to be breakable
            # over page boundaries
            for t in range(1, len(observed)):
                if not occurred[t]:
                    continue  # ought not to happen
                print(
                    r"\begin{ganttchart}[hgrid,vgrid,canvas/.style={draw=none},bar/.append style={fill=gray},x unit=0.5cm,y unit chart=0.5cm]{0}" +
                    "{{{t}}}\n".format(t=len(observed) + 1), file=tfile)
                for x in occurred[t][:-1]:
                    l = (str(x.arguments[0]) + ": " +
                         str(x.arguments[1])).replace('_', '\_')
                    print("\\ganttmilestone{{{l}}}{{{f}}}\\ganttnewline"
                          .format(l=l, f=t - 1), file=tfile)
                # handle last event separately to drop \ganttnewline
                x = occurred[t][-1]
                l = (str(x.arguments[0]) + ": " +
                     str(x.arguments[1])).replace('_', '\_')
                print("\\ganttmilestone{{{l}}}{{{f}}}"
                      .format(l=l, f=t - 1), file=tfile)
                print(r"\end{ganttchart}\\[-0.7em]""\n", file=tfile)
            facts = invert(holdsat)
            keys = sorted(facts, key=lambda atom: atom.arguments[0].name)
            for f in keys:
                print(
                    r"\begin{ganttchart}[hgrid,vgrid,canvas/.style={draw=none},bar/.append style={fill=gray},x unit=0.5cm,y unit chart=0.5cm]{0}" +
                    "{{{t}}}\n".format(t=len(observed) + 1), file=tfile)
                i = facts[f][0]
                l = (str(f.arguments[0]) + ": " +
                     str(f.arguments[1])).replace('_', '\_')
                print("\\ganttbar{{{label}}}{{{start}}}{{{finish}}}"
                      .format(label=l, start=i, finish=i), file=tfile)
                for t in facts[f][1:]:
                    print("\\ganttbar{{}}{{{start}}}{{{finish}}}"
                          .format(start=t, finish=t), file=tfile)
                print(r"\end{ganttchart}\\[-0.7em]""\n", file=tfile)
            print(r"\end{longtable}""\n"
                  r"\end{document}", file=tfile)
