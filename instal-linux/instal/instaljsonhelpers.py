import json

# noinspection
# PyUnresolvedReferences,PyUnresolvedReferences,PyUnresolvedReferences
from .clingo import Function, parse_term, Symbol
from .instalutility import fun_to_asp


def atom_sorter(y: list) -> list:
    """Returns a list of atoms (i.e. holdsat, occurred, etc)"""
    return sorted(y, key=generate_sorted_lambda, reverse=True
                  )


def generate_sorted_lambda(x: Function) -> list:
    criteria = []  # sort by institution name
    if len(x.arguments) > 1:
        criteria.append(x.arguments[1].name)
    fluenttype = x.arguments[0].name
    if fluenttype in ["perm", "pow", "obl", "live", "viol", "tpow", "ipow", "gpow"]:
        criteria.append("")
    else:
        criteria.append(fluenttype)
    criteria.append(fluenttype)
    firstlevel = x.arguments[0].arguments
    if not firstlevel:
        return criteria
    if len(firstlevel) == 0:
        return criteria
    for f in firstlevel:
        criteria.append(f.name)

    secondlevel = firstlevel[0]
    if isinstance(secondlevel, Symbol) or len(secondlevel) == 0:
        return criteria
    for s in secondlevel:
        criteria.append(s.name)
    return criteria


def check_trace_integrity(trace: list) -> bool:
    """Some function that defines and checks whether a json trace is valid """
    return True


def as_Fun(dct: dict) -> Function:
    """Returns a dictionary as a gringo Fun object."""
    if '__Fun__' in dct:
        return Function(dct['name'], dct['args'])
    return dct


def atom_str(atom: Function) -> str:
    """Returns an atom (gringo Fun) as a string."""
    return str(atom)
    # return (atom.name + '(' + ','.join(str(x) for x in atom.arguments + ')'))


def model_atoms_to_lists(model_atoms, from_json: bool=False, verbose: int=0):
    """
    Takes an iterable of model atoms and puts them in appropriate lists
    """
    #TODO: This and atom_sorter is a massive bottleneck.
    occurred = set()
    holdsat = set()
    observed = set()
    rejected = None
    if verbose > 2:
        print("FULL ATOM PRINTING\n---------------")
    for atom in model_atoms:
        if verbose > 2:
            print(atom)  # hook for client processing of atoms
        # if len(atom.arguments)==3: return #this is dummy callback atm from
        # sensor.
        if str(atom.name) == "observed":
            if len(atom.arguments) == 2:
                observed.add(Function(atom.name, [atom.arguments[0]]))
            elif len(atom.arguments) == 1:
                observed.add(Function(atom.name, atom.arguments))
        # observeds get dealt with by sensor in instalsolve.
        # maybe they shouldn't, but for now.
        if ((str(atom.name) == "occurred") and
            (len(atom.arguments) == 3 and int(str(atom.arguments[2])) == 0) or (
                len(atom.arguments) == 2 and from_json)):
            occurred.add(Function(atom.name, atom.arguments[0:2]))
        if ((str(atom.name) == "holdsat") and
            (len(atom.arguments) == 3 and int(str(atom.arguments[2])) == 1) or (
                len(atom.arguments) == 2 and from_json)):
            holdsat.add(Function(atom.name, atom.arguments[0:2]))

            # or(len(atom.arguments) == 2) because json oject is a different form - no instant information. Needs fixing.
            # right now it puts in a set then converts to list.
    if verbose > 2:
        print("--------------------\nFULL ATOM PRINTING ENDS\n---------------\n")
    return atom_sorter(list(observed)), atom_sorter(list(occurred)), atom_sorter(list(holdsat))


def state_dict_from_lists(observed: list, occurred: list, holdsat: list) -> dict:
    """Converts lists of observed, occurred, holdsat to a state dict"""
    j = {"state":
         {
             "observed": observed if observed is not None else [],
             "occurred": occurred,
             "holdsat": holdsat
         }
         }
    return j


def trace_dicts_from_file(json_path: str) -> list:
    """Loads in a json file and turns it into a trace list of dicts"""
    trace = []
    with open(json_path, "rt") as jsonfile:
        for l in jsonfile.readlines():
            line = json.loads(l, object_hook=as_Fun)
            if not isinstance(line, list):
                # Required to allow json files to either be one single list or
                # each line containing one timestep (legacy).
                line = [line]
            trace += line
    return trace


def json_dict_to_string(j: dict) -> str:
    """Returns a string of a state dict"""
    return state_to_string(j["state"]["observed"], j["state"]["occurred"], j["state"]["holdsat"])


def state_to_string(observed: list, occurred: list, holdsat: list) -> str:
    """ Takes an observed, occurred, and holdsat list and returns a string representation.
    """
    out_str = ""
    for h in atom_sorter(holdsat):
        out_str += atom_str(h) + "\n"
    for o in atom_sorter(occurred):
        out_str += atom_str(o) + "\n"
    for o in atom_sorter(observed):
        out_str += atom_str(o)
        # TODO This is a horrible hack; deal with the incorrect output from
        # query first. (The break thing to only get one observed that is.)
        break
    return out_str


def dict_funs_to_asp(dict_predicates: dict, keys: list=None) -> str:
    """Translates a dict of funs into ASP."""
    if not keys:
        keys = ["holdsat", "occurred", "observed"]
    asp = ""
    for key in keys:
        list_predicates = dict_predicates["state"][key]
        for v in list_predicates:
            asp += fun_to_asp(v)
    return asp


def dict_funs_to_list(dict_predicates: dict, keys=None) -> list:
    """Translates a dict of funs into lists"""
    if not keys:
        keys = ["holdsat", "occurred", "observed"]
    l = []
    for key in keys:
        list_predicates = dict_predicates["state"][key]
        for v in list_predicates:
            l.append(v)
    return l


def json_check_conditions(trace: list, conditions: list, verbose: int=0) -> int:
    """A wrapper for check_trace_for that checks if the length of the trace and conditions are the same.
    """
    errors = 0
    if len(trace) == len(conditions):
        offset = 0
    elif len(trace) == len(conditions) + 1:
        offset = 1
    else:
        raise Exception("Trace given not long enough. (Trace: {}, conditions: {})".format(
            len(trace), len(conditions)))
    for i in range(0, len(conditions)):
        errors += check_trace_for(trace[i + offset], conditions[i], verbose)
    return errors


def check_trace_for(answer_set: dict, conditions: dict, verbose: int=0) -> int:
    """Takes an InstAL trace and a set of conditions in the format:
    [
        { "holdsat" : [],
          "occurred" : [],
          "notholdsat" : [],
          "notoccurred" : []
    ,
        { ... }
    ]

    Returns: 0 if the trace fits those conditions, +1 for each condition it doesn't meet.
    """
    errors = 0
    answer_set = answer_set["state"]
    for h in conditions.get("holdsat", []):
        found = False
        t = parse_term(h)
        for a in answer_set["holdsat"]:
            if a == t:
                found = True
                break
        if found:
            if verbose > 1:
                print("Holds (correctly)", h)
        else:
            errors += 1
            if verbose > 0:
                print("Doesn't hold (and should): ", h)

    for h in conditions.get("occurred", []):
        found = False
        t = parse_term(h)
        for a in answer_set["occurred"]:
            if a == t:
                found = True
                break
        if found:
            if verbose > 1:
                print("Occurred (correctly)", h)
        else:
            errors += 1
            if verbose > 0:
                print("Didn't occur (and should have): ", h)

    for h in conditions.get("notholdsat", []):
        found = False
        t = parse_term(h)
        for a in answer_set["holdsat"]:
            if a == t:
                found = True
                break
        if not found:
            if verbose > 1:
                print("Doesn't Hold (correctly)", h)
        else:
            errors += 1
            if verbose > 0:
                print("Holds (and shouldn't): ", h)

    for h in conditions.get("notoccurred", []):
        found = False
        t = parse_term(h)
        for a in answer_set["occurred"]:
            if a == t:
                found = True
                break
        if not found:
            if verbose > 1:
                print("Doesn't occur (correctly)", h)
        else:
            errors += 1
            if verbose > 0:
                print("Occurs (and shouldn't): ", h)
    return errors
