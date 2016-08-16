from gringo import Fun, parse_term, cmp
import simplejson as json

def atom_sorter(y):
    return sorted(y, key=(
        lambda x: (x.args()[0].name(),
                   x.args()[0].args()[0].name() if len(x.args()[0].args()) > 0 else 0
        )
    )
    )


def check_trace_integrity(trace):
    # check that current and previous timestamps present and consistent
    return True


def as_Fun(dct):
    if '__Fun__' in dct:
        return Fun(dct['name'], dct['args'])
    return dct


def atom_str(atom):
    return (atom.name() + '(' + ','.join(str(x) for x in atom.args()) + ')')


def model_atoms_to_lists(model_atoms, from_json=False, verbose=0):
    occurred = set()
    holdsat = set()
    observed = set()
    rejected = None
    if verbose > 2: print("FULL ATOM PRINTING\n---------------")
    for atom in model_atoms:
	if verbose > 2: print(atom)
        # hook for client processing of atoms

        # if len(atom.args())==3: return #this is dummy callback atm from sensor.
        if ( (atom.name() == "observed") and (len(atom.args()) == 1) ):
            observed.add(Fun(atom.name(), atom.args()))
        #observeds get dealt with by sensor in instalsolve.
        #maybe they shouldn't, but for now.
        if ( (atom.name() == "occurred") and
                 ((len(atom.args()) == 3 and atom.args()[2] == 0) or len(atom.args()) == 2 and from_json) ):
            occurred.add(Fun(atom.name(), atom.args()[0:2]))
        if ( (atom.name() == "holdsat") and
                 ((len(atom.args()) == 3 and atom.args()[2] == 1) or len(atom.args()) == 2 and from_json) ):
            if atom.args()[0].name() == "pow":
                if len(atom.args()[0].args()) != 2:
                    continue
                #this is required because initially statements are
                #called using a weird one-argument pow.
            holdsat.add(Fun(atom.name(), atom.args()[0:2]))

            # or(len(atom.args()) == 2) because json oject is a different form - no instant information. Needs fixing.
            # right now it puts in a set then converts to list.
    if verbose > 2: print("--------------------\nFULL ATOM PRINTING ENDS\n---------------\n")
    return atom_sorter(list(observed)), atom_sorter(list(occurred)), atom_sorter(list(holdsat))


def state_dict_from_lists(observed, occurred, holdsat):
    j = {"state":
             {
                 "observed": observed if observed is not None else [],
                 "occurred": occurred,
                 "holdsat": holdsat
             }
    }
    return j

def trace_dicts_from_file(json_path):
        trace = []
    	with open(json_path,"r") as jsonfile:
		for l in jsonfile.readlines():
			trace += [json.loads(l, object_hook=as_Fun)]
        return trace

def json_dict_to_string(j):
    return state_to_string(j["state"]["observed"], j["state"]["occurred"], j["state"]["holdsat"])


def state_to_string(observed, occurred, holdsat):
    out_str = ""
    for h in atom_sorter(holdsat):
        out_str += atom_str(h) + "\n"
    for o in atom_sorter(occurred):
        out_str += atom_str(o) + "\n"
    for o in observed:
        out_str += atom_str(o)
    return out_str


def dummy_callback(x, y):
    return


def dict_funs_to_asp(dict_predicates,keys=["holdsat", "occurred", "observed"]):
    asp = ""
    for key in keys:
        list_predicates = dict_predicates["state"][key]
        for v in list_predicates:
            asp += fun_to_asp(v)
    return asp


def dict_funs_to_list(dict_predicates,keys=["holdsat", "occurred", "observed"]):
    l = []
    for key in keys:
        list_predicates = dict_predicates["state"][key]
        for v in list_predicates:
            l.append(v)
    return l

def json_check_conditions(trace, conditions,verbose=0):
    errors = 0
    if len(trace) == len(conditions):
        offset = 0
    elif len(trace) == len(conditions) + 1:
        offset = 1
    else:
        exit(-1)
    for i in range(0, len(conditions)):
        errors += check_trace_for(trace[i+offset],conditions[i],verbose)
    return errors

def check_trace_for(answer_set, conditions, verbose=0):
    errors = 0
    answer_set = answer_set["state"]
    for h in conditions.get("holdsat",[]):
        found = False
        t = parse_term(h)
        for a in answer_set["holdsat"]:
            if cmp(a, t) == 0:
                found = True
                break
        if found:
            if verbose > 1: print("Holds (correctly)",h)
        else:
            errors += 1
            if verbose > 0: print("Doesn't hold (and should): ",h)

    for h in conditions.get("occurred",[]):
        found = False
        t = parse_term(h)
        for a in answer_set["occurred"]:
            if cmp(a, t) == 0:
                found = True
                break
        if found:
            if verbose > 1: print("Occurred (correctly)",h)
        else:
            errors += 1
            if verbose > 0: print("Didn't occur (and should have): ",h)

    for h in conditions.get("notoccurred",[]):
        if h == "*": #wait this doesn't work because live(inst) - fix.
            exit(-1)
            if len(answer_set["occurred"]) == len(conditions.get("occurred"),[]):
                if verbose > 1: print("No occurred statements other than the specified.")
            else:
                errors += 1
                if verbose > 0: print("Too many occurred statements")
        else:
            continue
            #todo

    for h in conditions.get("notholdsat",[]):
        if h == "*":
            exit(-1)
            if len(answer_set["holdsat"]) == len(conditions.get("holdsat",[])):
                if verbose > 1: print("No holdsat statements other than the specified.")
            else:
                errors += 1
                if verbose > 0: print("Too many holdsats statements")
        else:
            found = False
            t = parse_term(h)
            for a in answer_set["holdsat"]:
                if cmp(a, t) == 0:
                    found = True
                    break
            if not found:
                if verbose > 1: print("Doesn't Hold (correctly)",h)
            else:
                errors += 1
                if verbose > 0: print("Holds (and shouldn't): ",h)

    for h in conditions.get("notoccurred",[]):
        if h == "*": #this doesn't work lol
            if len(answer_set["occurred"]) == len(conditions.get("occurred",[])):
                if verbose > 1: print("No occurred statements other than the specified.")
            else:
                errors += 1
                if verbose > 0: print("Too many occurred statements")
        else:
            found = False
            t = parse_term(h)
            for a in answer_set["occurred"]:
                if cmp(a, t) == 0:
                    found = True
                    break
            if not found:
                if verbose > 1: print("Doesn't occur (correctly)",h)
            else:
                errors += 1
                if verbose > 0: print("Occurs (and shouldn't): ",h)
    return errors
