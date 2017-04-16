from instal.clingo import parse_term
from abc import ABCMeta


class ClingoWrapper(metaclass=ABCMeta):
    ctl = None

    def __init__(self, initially: list, model_files: list, domain_facts: "defaultdict(set)", args):
        if not self.ctl:  # Requires self.ctl to be set by subclass
            raise NotImplementedError
        for x in model_files:
            x.seek(0)
            if args.verbose > 2:
                print("loading: ", x.name)
            self.ctl.load(x.name)

        parts = []
        for typename, literals in domain_facts.items():
            for l in literals:
                parts += [(typename, [parse_term(l)])]
        if args.verbose > 2:
            print("grounding: ", parts + [("base", [])])
        self.ctl.ground(parts + [("base", [])])
        if args.verbose > 2:
            print("grounded")

        signature_types = [s[0] for s in self.ctl.symbolic_atoms.signatures]
        from_domain_types = [d for d in domain_facts]
        # Testing for type names in domain file not in grounded file
        for d in from_domain_types:
            if d not in signature_types:
                print(
                    "WARNING: Type {} in domain file is not in grounded model.".format(d))
        if args.verbose > 2:
            print("initialization complete")

    def solve(self, events: list) -> None:
        raise NotImplementedError
