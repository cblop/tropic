import json
from abc import ABCMeta
from instal.parser.InstalParserNew import InstalParserNew
from instal.compiler.InstalCompilerNew import InstalCompilerNew
from instal.domainparser.DomainParser import DomainParser
from instal.factparser.FactParser import FactParser
from instal.instalutility import encode_Fun, temporary_text_file
import os


INSTAL_STANDARD_PRELUDE = """
% Surpress Clingo warnings
ifluent(0,0).
nifluent(0,0).
oblfluent(0,0).
initiated(0,0,0).
xinitiated(0,0,0,0).
terminated(0,0,0).
xterminated(0,0,0,0).
_typeNotDeclared :- 1 == 2.
bridge(1).

% TIME
start(0).
instant(0..T) :- final(T).
next(T,T+1) :- instant(T).
final(horizon).

% TODO: Remove the need for this in constraint generation
true.

% FLUENT RULES
fluentterminated(P, In, I) :- terminated(P, In, I), instant(I), inst(In).
fluentterminated(P, In, I) :- xterminated(InS, P, In, I), instant(I), inst(In), inst(InS).
fluentinitiated(P, In, I) :- initiated(P, In, I), instant(I), inst(In).
fluentinitiated(P, In, I) :- xinitiated(InSo, P, In, I), inst(InSo), inst(In), instant(I).
holdsat(P,In,J):- holdsat(P,In,I),not fluentterminated(P,In,I),
	next(I,J),ifluent(P, In),instant(I),instant(J), inst(In).
holdsat(P,In,J):- fluentinitiated(P,In,I),next(I,J),
	ifluent(P, In),instant(I),instant(J), inst(In).

holdsat(P,In,J):- holdsat(P,In,I),not fluentterminated(P,In,I),
	next(I,J),ifluent(P, In),instant(I),instant(J), bridge(In).
holdsat(P,In,J):- initiated(P,In,I),next(I,J),
	ifluent(P, In),instant(I),instant(J), bridge(In).

% EXTERNAL FLUENTS
#external holdsat(F,I) : fluent(F,I), inst(I).
holdsat(F,I,J) :- holdsat(F,I), start(J).
#external holdsat(perm(E),I) : event(E), inst(I).
holdsat(perm(E),I,J) :- holdsat(perm(E),I), start(J).
#external holdsat(pow(E),I) : event(E), inst(I).
holdsat(pow(E),I,J) :- holdsat(pow(E),I), start(J).

% EVENTS OCCUR
occurred(E,In,I):- evtype(E,In,ex),observed(E,In,I),instant(I), inst(In).
% produces null for unknown events
occurred(null,In,I) :- not evtype(E,In,ex), observed(E,In,I),
	instant(I), inst(In).

% EXTERNAL EVENTS
% for incremental observations
#external observed(E) : event(E).
compObserved(E,J) :- observed(E), start(J).

% for observation sequences
#external observed(E,I) : event(E), instant(I).
compObserved(E,I) :- observed(E,I).

recEvent(I) :- observed(E), event(E), start(I), not final(I).
recEvent(I) :- observed(E, I), event(E), instant(I), not final(I).
observed(_unrecognisedEvent, I) :- not recEvent(I), _eventSet(I).

%EVENT SET
#external _eventSet(I) : instant(I).

% VIOLATIONS FOR NON-PERMITTED EVENTS
occurred(viol(E),In,I):-
	occurred(E,In,I),
	not holdsat(perm(E),In,I),
	holdsat(live(In),In,I),evinst(E,In),
	event(E),instant(I),event(viol(E)),inst(In).

%%  mode COMPOSITE is chosen:\n
1 {compObserved(E, J) : evtype(E, In, ex), inst(In)} 1:- instant(J), not final(J), not compObserved(_unrecognisedEvent, J).
:- compObserved(E,J),compObserved(F,J),instant(J),evtype(E,InX,ex),
   evtype(F,InY,ex), E!=F,inst(InX;InY). 
obs(I):- compObserved(E,I),evtype(E,In,ex),instant(I),inst(In).
obs(I) :- compObserved(_unrecognisedEvent, I), instant(I).
      :- not obs(I), not final(I), instant(I), inst(In).
observed(E,In,I) :- compObserved(E,I), inst(In), instant(I).

:- _typeNotDeclared. %defends against partially grounded institutions.

_preludeLoaded.

#show observed/1.
#show observed/2.
#show occurred/3.
#show holdsat/3.
"""


class InstalModel(metaclass=ABCMeta):
    """
        InstalModel
        Wrapper for different implementations of InstAL solving.
        See: InstalMultiShotModel and InstalSingleShotModel
    """

    def __init__(self, instal_args):
        self.prelude = temporary_text_file(
            INSTAL_STANDARD_PRELUDE, file_extension=".lp", delete=True)
        self.instal_args = instal_args
        self.model_files = self.get_model_files(self.instal_args.ial_files, self.instal_args.bridge_file) + [
            open(l, "rb") for l in self.instal_args.lp_files]
        self.domain_facts = self.get_domains(instal_args)
        self.initial_facts = self.get_initial(instal_args)
        self.answersets = []

    def get_model_files(self, ial_files, bridge_files):
        parser_wrapper = InstalParserNew()
        compiler_wrapper = InstalCompilerNew()

        instal_dictionary = parser_wrapper.get_instal_dictionary(
            ial_files, bridge_files)
        irs_dictionary = parser_wrapper.parse(instal_dictionary)
        asp_dictionary = compiler_wrapper.compile(irs_dictionary)

        output_files = []
        for a in asp_dictionary["institution_asp"]:
            output_files.append(a["file"])

        for a in asp_dictionary["bridge_asp"]:
            output_files.append(a["file"])

        output_files.append(self.prelude)
        return output_files

    def get_domains(self, solve_args):
        domain_parser = DomainParser()
        domain_facts = domain_parser.get_groundings(solve_args.domain_files)
        return domain_facts

    def get_initial(self, solve_args):
        fact_parser = FactParser()
        facts = fact_parser.get_facts(solve_args.fact_files)
        return facts

    def check_and_output_json(self):
        if self.instal_args.json_file:
            self.output_json(self.instal_args.json_file)

    def output_json(self, json_file):
        if os.path.isdir(json_file):
            self.output_json_dir(json_file)
        else:
            self.output_json_file(json_file)

    def output_json_file(self, json_file):
        base_dir, base_filename = os.path.split(json_file)
        for out_json in self.answersets:
            filename = (base_dir + "/" if base_dir else "") + "{}_".format(out_json[0]["metadata"]["answer_set_n"]) + base_filename if out_json[
                0]["metadata"]["answer_set_of"] > 1 else ((base_dir + "/" if base_dir else "") + base_filename)
            self.dump_json(filename, out_json)

    def output_json_dir(self, json_file):
        for out_json in self.answersets:
            filename = json_file + "/{}_{}_of_{}.json".format(out_json[0]["metadata"]["pid"], out_json[
                                                              0]["metadata"]["answer_set_n"], out_json[0]["metadata"]["answer_set_of"])
            self.dump_json(filename, out_json)

    def dump_json(self, filename, out_json):
        with open(filename, "w") as jf:
            print(json.dumps(out_json,
                             sort_keys=True, separators=(',', ':'), default=encode_Fun), file=jf)
