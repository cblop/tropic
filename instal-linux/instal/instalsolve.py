if __name__ == "__main__":
    raise NotImplementedError(
        "Try running ../instalsolve.py instead, this file is just an interface.")

from .instalargparse import getargs, check_args, buildargparser

from .models.InstalSingleShotModel import InstalSingleShotModel

from .instalexceptions import InstalRuntimeError

def instal_solve():
    args, unk = getargs()
    instal_solve_with_args(args, unk)


def instal_solve_keyword(bridge_file=False, domain_files=None, fact_files=None, input_files=None, json_file=None,
                         output_file=None, verbose=0, query=None):
    if not domain_files:
        domain_files = []
    if not fact_files:
        fact_files = []
    if not input_files:
        input_files = []
    parser = buildargparser()
    args = []
    if bridge_file:
        args += ["-b", bridge_file]

    args += ["-d"] + domain_files

    if len(fact_files) > 0:
        args += ["-f"] + fact_files

    args += ["-i"] + input_files

    if json_file is not None:
        args += ["-j", json_file]

    if output_file is not None:
        args += ["-o", output_file]

    if verbose > 0:
        args += ["-{v}".format(v="v" * verbose)]

    if query is not None:
        args += ["-q", query]

    (a, u) = parser.parse_known_args(args)
    check_args(a, u)
    return instal_solve_with_args(a, u)


def instal_solve_with_args(args, unk):
    instal_model = InstalSingleShotModel(args)
    if not args.query:
        raise InstalRuntimeError("No query file provided for instal solve.")
    with open(args.query, "rt") as query_file:
        query_text = query_file.read()
    instal_model.solve(query_text)
    return instal_model.answersets
