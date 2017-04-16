

from collections import defaultdict

from instal.clingo import Control, Function
from instal.models.ClingoWrapper import ClingoWrapper


class Oracle(ClingoWrapper):
    """
        Oracle
        The ClingoWrapper for multi shot solves.
        A significant chunk of this code is legacy and thus fragile.
    """

    def __init__(self, initially, model_files, domain_facts, args):
        self.answersets = {}
        self.cycle = 0
        self.args = args
        self.observations = None
        self.holdsat = initially
        self.ctl = Control(['-n', str(args.number), '-c',
                            'horizon={0}'.format(args.length)])
        super(Oracle, self).__init__(
            initially, model_files, domain_facts, args)

    def solve(self, events: list) -> None:
        self.observations = events
        for x in self.observations:
            if self.args.verbose > 1:
                print("assign", x)
            self.ctl.assign_external(x, True)
        for h in self.holdsat:
            self.ctl.assign_external(h, True)
        self.cycle = self.args.length  # len(self.observations)
        answers = 0
        with self.ctl.solve_iter() as it:
            for m in it:
                # if self.args.verbose>0: print("Answer set {}".format(answers))
                if self.args.answer_set > 0 and self.args.answer_set != answers + 1:
                    # may be make this [[],[],[]]??
                    self.answersets[answers] = []
                else:
                    self.answersets[answers] = self.process_answer_set(m)
                # if self.args.verbose>0:
                # print(state_to_string(self.answersets[answers][0], self.answersets[answers][1], self.answersets[answers][2]))
                # print(m.optimization())
                answers += 1
        # print(self.ctl.stats)
        if self.args.verbose > 0:
            if answers == 1:
                print("There is 1 answer set")
            else:
                print("There are {} answer sets".format(answers))
        return

    # Okay, the utility function doesn't work because this is a full trace
    # model.
    def process_answer_set(self, model):
        # TODO: This is a massive bottleneck.
        occurred = defaultdict(list)
        holdsat = defaultdict(list)
        observed = defaultdict(list)
        rejected = None

        if self.args.verbose > 2:
            print("FULL ATOM PRINTING\n---------------")
        for atom in model.symbols(shown=True):
            if self.args.verbose > 2:
                print(atom)
            if atom.name in ["observed", "occurred", "holdsat"]:
                what = Function(atom.name, atom.arguments[:-1])
                when = atom.arguments[-1].number
            if (atom.name == "observed") and (len(atom.arguments) == 2):
                observed[when + 1].append(what)
            if atom.name == "occurred":
                occurred[when + 1].append(what)
            if atom.name == "holdsat":
                holdsat[when].append(what)
        return [observed, occurred, holdsat]
