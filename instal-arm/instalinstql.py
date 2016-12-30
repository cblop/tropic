from __future__ import print_function
from gringo import Control, Model, Fun, parse_term
import json
import sys

from instaljsonhelpers import as_Fun, check_trace_integrity, model_atoms_to_lists, state_dict_from_lists, dict_funs_to_asp, dict_funs_to_list, trace_dicts_from_file

from tempfile import mkstemp, mkdtemp
import os

def temporary_text_file(text):
	(fd,path) = mkstemp() # returns a handle/path pair
	file = open(path,'w')
	print(text,file=file)
	file.close()
	os.close(fd)
	return path


def fun_to_asp(fun):
	if isinstance(fun,Fun):
		return str(fun) + ".\n"
	return ""

class instql_querier(object):
	def __init__(self):
		json_out = None

	def instql_show(self,dict_predicates, instql_asp):
	    self.ctl = Control()
	    self.ctl.load(temporary_text_file(instql_asp))
	    fact_asp = dict_funs_to_asp(dict_predicates)
	    self.ctl.load(temporary_text_file(fact_asp))
	    parts = []


	    self.ctl.ground(parts+[("base", [])])

	    self.ctl.solve(on_model=self.on_model)

	    out = state_dict_from_lists(self.observed,self.occurred,self.holdsat)
	    return out

	def on_model(self,model):
		last_solution = model.atoms()
		self.observed, self.occurred, self.holdsat = model_atoms_to_lists(model.atoms(Model.SHOWN),from_json=True)
		

def instql_trace_from_file(json_path, instql_asp):
	trace = trace_dicts_from_file(json_path)
	return instql_trace(trace, instql_asp)
	
def instql_trace(trace, instql_asp):
	querier = instql_querier()
	out_jsons = []
	for t in trace:
		metadata = t["metadata"]
		q = metadata.get("queries",[])
		q.append(instql_asp)
		metadata["queries"] = q
		
		out_json = querier.instql_show(t, instql_asp)
		out_json.update({"metadata" : metadata})
		out_jsons.append(out_json)

	return out_jsons
			

#for n in range(0, len(trace)):
#    print("TIMESTEP {}".format(n))
#    instalinstql.instql_show(trace[n],"#show. #show observed/1. #show occurred/2. #show holdsat(X,basic) : holdsat(X, basic), occurred(viol(Y), basic).")
#    print("\n")

