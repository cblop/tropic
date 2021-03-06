if __name__ == "__main__":
    raise NotImplementedError("Try running ../instalquery.py instead.")


from .instalargparse import buildqueryargparser, check_args, getqueryargs

from .models.InstalMultiShotModel import InstalMultiShotModel


def instal_query_with_args(args, unk):
    instal_model = InstalMultiShotModel(args)
    if args.query:
        with open(args.query, "rt") as query_file:
            query_text = query_file.read()
    else:
        query_text = ""
    instal_model.solve(query_text)
    return instal_model.answersets


def instal_query_keyword(bridge_file=False, domain_files=None, fact_files=None, input_files=None, json_file=None,
                         output_file=None, verbose=0, query=None, number=1, length=1, answerset=0):
    if not domain_files:
        domain_files = []
    if not fact_files:
        fact_files = []
    if not input_files:
        input_files = []
    parser = buildqueryargparser()
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

    # ...Okay, for some reason this only works if I pass it the str of length. Why?
    args += ["-l", str(length)]
    args += ["-n", str(number)]
    args += ["-a", answerset]
    (a, u) = parser.parse_known_args(args)
    check_args(a, u)
    return instal_query_with_args(a, u)


def instal_query():
    args, unk = getqueryargs()
    instal_query_with_args(args, unk)
