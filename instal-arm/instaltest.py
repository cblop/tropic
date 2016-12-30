#!/usr/bin/python

# 20160421 JAP: initialize ial_files and lp_files attrinutes in InstalTest
#               removed grounding file delete operation
# 20160412 JAP: add call to instal_domain_facts to extract data from domain file
#               delete last file on model_files list (grounding program)
# 20160409 JAP: add initially argument to run_test and code to join to holdsat
#         TODO: extend __init__ method for coordinated and interacting models
# 201603XX JAP: create class

from __future__ import print_function
import instalargparse
from instalcompile import instal_compile, instal_state_facts, instal_domain_facts
from gringo import parse_term
from tempfile import mkstemp, mkdtemp
import os
from sensor import Sensor
import fileinput
import shutil

# In most cases, you want InstalTestFromFile.

def dummy(x,y):
    return

class InstalTest(object):

    def temporary_text_file(self,text):
        (fd,path) = mkstemp() # returns a handle/path pair
        file = open(path,'w')
        print(text,file=file)
        file.close()
        os.close(fd)
        return path

    def __init__(self,instal_texts,domain_texts,fact_text,options=""):
	#instal_texts is a list of strings
	ipath = []
	for i in instal_texts:
		ipath.append(self.temporary_text_file(i))

        dpath = []
	for d in domain_texts:
		dpath.append(self.temporary_text_file(d))
        fpath = self.temporary_text_file(fact_text)
        opath = mkdtemp()

	#-o needs to be a directory if >1 input file and a .lp file otherwise. This is a hack but it crashes otherwise.
	if len(instal_texts) > 1:
		opath_end = "/"
	else:
		opath_end = "/tmp.lp"

	#Construct argument list using temp files
        argparser = instalargparse.buildargparser()
	topass = ['-o',opath+opath_end,'-f',fpath,options]
	topass += ['-i'] + ipath
	topass += ['-d'] + dpath
        (args,unk) = argparser.parse_known_args(topass)
        # assumes input files are .ial not .lp
        args.ial_files = args.input_files
        args.lp_files = []
        model_files = instal_compile(args)
        initial_state = instal_state_facts(args)
        domain_facts = instal_domain_facts(args)
        self.sensor = Sensor(dummy,initial_state,model_files,domain_facts,args)

	# Clean up files. 
	for i in ipath:
        	os.remove(i)
	for d in dpath:
        	os.remove(d)
        os.remove(fpath)
        shutil.rmtree(opath)

    def syntax_check(self,data,terms):
        good = True;
        for d in data:
            t = parse_term(d)
            if not(t.name() in terms):
                print("Warning: unrecognized term",t)
                good = False
        return good;

    def run_test(self,event,initially=[],
                 holds=[],notholds=[],occurs=[],notoccurs=[],name=None):
        if name is None: #Default name to the event if no name set
            name = event
        # check for simple typos in term inputs
        self.syntax_check(initially+holds+notholds+[event]+occurs+notoccurs,
                          ["observed","occurred","holdsat"])
        self.sensor.holdsat += map(parse_term,initially)
        self.sensor.solve(event)
        event_sat = self.sensor.check_events(event,occurs,notoccurs)
        fact_sat = self.sensor.check_facts(event,holds,notholds)
        if (event_sat and fact_sat): # and (present != [] or absent != []):
            print("Satisfied({n}) {name}"
                  .format(name=name,n=self.sensor.cycle))

class InstalTestFromFile(InstalTest):
	def __init__(self, instal_files, domain_files,fact_file,options=""):
		instal_texts = []
		for f in instal_files:
			with open(f,"r") as i_f:
				instal_texts.append(i_f.read())

		domain_texts = []
		for d in domain_files:
			with open(d,"r") as d_f:
				domain_texts.append(d_f.read())

		if not fact_file == "":
			with open(fact_file,"r") as f_f:
				fact_text = f_f.read()
		else:
			fact_text = ""

		super(InstalTestFromFile,self).__init__(instal_texts,domain_texts,fact_text,options)
		
