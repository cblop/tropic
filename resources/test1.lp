%
% Domain declarations for starWars
%
agent(lukeSkywalker).
agent(obiWan).
agent(darthVader).
role(hero).
role(villain).
role(dispatcher).
role(friend).
trope(herosJourney).
phase(inactive).
phase(done).
phase(phaseA).
phase(phaseB).
phase(phaseC).
phase(phaseD).
phase(phaseE).
phase(phaseF).
phase(phaseG).
phase(phaseH).
phase(phaseI).
phase(phaseJ).
place(home).
place(away).
placename(tatooine).
placename(space).
quest(destroyTheDeathStar).
object(weapon).
object(friend).
objectname(lightsaber).
objectname(hanSolo).
%
% -------------------------------PART 1-------------------------------
%
%
% Standard prelude for starWars
%
% suppress clingo warnings in absence of inertials, non-inertials or obligations
ifluent(0,0).
nifluent(0,0).
oblfluent(0,0).
% fluent rules
holdsat(P,In,J):- holdsat(P,In,I),not terminated(P,In,I),
    next(I,J),ifluent(P, In),instant(I),instant(J), inst(In).
holdsat(P,In,J):- initiated(P,In,I),next(I,J),
    ifluent(P, In),instant(I),instant(J), inst(In).
holdsat(P,In,J):- initiated(P,In,I),next(I,J),
    oblfluent(P, In),instant(I),instant(J), inst(In).
% all observed events occur
occurred(E,In,I):- evtype(E,In,ex),observed(E,In,I),instant(I), inst(In).
% produces null for unknown events
occurred(null,In,I) :- not evtype(E,In,ex), observed(E,In,I),
    instant(I), inst(In).
% produces gap warning for unknown events
unknown(E, In, I) :- not evtype(E,In,ex), observed(E,In,I),
    instant(I), inst(In).
warninggap(In, I) :- unknown(E,In,I), inst(In), instant(I).
% a violation occurs for each non-permitted action
occurred(viol(E),In,I):-
    occurred(E,In,I),
    evtype(E,In,ex),
    not holdsat(perm(E),In,I),
    holdsat(live(In),In,I),evinst(E,In),
    event(E),instant(I),event(viol(E)),inst(In).
occurred(viol(E),In,I):-
    occurred(E,In,I),
    evtype(E,In,inst),
    not holdsat(perm(E),In,I),
    event(E),instant(I),event(viol(E)), inst(In).
% needed until I tidy up some of the constraint generation
true.
start(0).
instant(0..T) :- final(T).
next(T,T+1) :- instant(T).
final(horizon).
% externals for individual institutions
#external observed(E,I) : event(E), inst(I).
observed(E,I,J) :- observed(E,I), start(J).
#external holdsat(F,I) : fluent(F,I), inst(I).
holdsat(F,I,J) :- holdsat(F,I), start(J).
#external holdsat(perm(E),I) : event(E), inst(I).
holdsat(perm(E),I,J) :- holdsat(perm(E),I), start(J).
#external holdsat(pow(E),I) : event(E), inst(I).
holdsat(pow(I,E),I,J) :- holdsat(pow(E),I), start(J).

%
% Rules for Institution starWars
%
  ifluent(live(starWars), starWars).
  fluent(live(starWars), starWars).
  inst(starWars).
%
% Constraints for observable events depending on mode option
%
%%  mode SINGLE is chosen:
{observed(E,In,J)}:- evtype(E,In,ex),instant(J), not final(J), inst(In).
:- observed(E,In,J),observed(F,In,J),instant(J),evtype(E,In,ex),
evtype(F,In,ex), E!=F,inst(In). 
obs(In,I):- observed(E,In,I),evtype(E,In,ex),instant(I),inst(In).
         :- not obs(In,I), not final(I), instant(I), inst(In).

%
% The following types were declared:
%
% PlaceName
% ObjectName
% Object
% Agent
% Quest
% Place
% Phase
% Role
% Trope
%
% Exogenous events
% Event: go (type: ex)
  event(go(Agent0,PlaceName1)) :- agent(Agent0),placename(PlaceName1).
  evtype(go(Agent0,PlaceName1),starWars,ex) :- agent(Agent0),placename(PlaceName1).
  evinst(go(Agent0,PlaceName1),starWars) :- agent(Agent0),placename(PlaceName1).
  ifluent(perm(go(Agent0,PlaceName1)), starWars) :- agent(Agent0),placename(PlaceName1).
  fluent(perm(go(Agent0,PlaceName1)), starWars) :- agent(Agent0),placename(PlaceName1).
  event(viol(go(Agent0,PlaceName1))) :- agent(Agent0),placename(PlaceName1).
  evtype(viol(go(Agent0,PlaceName1)), starWars, viol) :- agent(Agent0),placename(PlaceName1).
  evinst(viol(go(Agent0,PlaceName1)),starWars) :- agent(Agent0),placename(PlaceName1).
% Event: meet (type: ex)
  event(meet(Agent0,Agent1)) :- agent(Agent0),agent(Agent1).
  evtype(meet(Agent0,Agent1),starWars,ex) :- agent(Agent0),agent(Agent1).
  evinst(meet(Agent0,Agent1),starWars) :- agent(Agent0),agent(Agent1).
  ifluent(perm(meet(Agent0,Agent1)), starWars) :- agent(Agent0),agent(Agent1).
  fluent(perm(meet(Agent0,Agent1)), starWars) :- agent(Agent0),agent(Agent1).
  event(viol(meet(Agent0,Agent1))) :- agent(Agent0),agent(Agent1).
  evtype(viol(meet(Agent0,Agent1)), starWars, viol) :- agent(Agent0),agent(Agent1).
  evinst(viol(meet(Agent0,Agent1)),starWars) :- agent(Agent0),agent(Agent1).
% Event: noDeadline (type: ex)
  event(noDeadline) :- true.
  evtype(noDeadline,starWars,ex) :- true.
  evinst(noDeadline,starWars) :- true.
  ifluent(perm(noDeadline), starWars) :- true.
  fluent(perm(noDeadline), starWars) :- true.
  event(viol(noDeadline)) :- true.
  evtype(viol(noDeadline), starWars, viol) :- true.
  evinst(viol(noDeadline),starWars) :- true.
%
% null event for unknown events
% Event: null (type: ex)
  event(null).
  evtype(null,starWars,ex).
  evinst(null,starWars).
  ifluent(perm(null), starWars).
  fluent(perm(null), starWars).
  event(viol(null)).
  evtype(viol(null),starWars,viol).
  evinst(viol(null),starWars).
% Institutional events
% Event: intHerosJourney (type: in)
  event(intHerosJourney(Agent0,Agent1,PlaceName2,PlaceName3)) :- agent(Agent0),agent(Agent1),placename(PlaceName2),placename(PlaceName3).
  evtype(intHerosJourney(Agent0,Agent1,PlaceName2,PlaceName3),starWars,inst) :- agent(Agent0),agent(Agent1),placename(PlaceName2),placename(PlaceName3).
  evinst(intHerosJourney(Agent0,Agent1,PlaceName2,PlaceName3),starWars) :- agent(Agent0),agent(Agent1),placename(PlaceName2),placename(PlaceName3).
  ifluent(pow(starWars,intHerosJourney(Agent0,Agent1,PlaceName2,PlaceName3)),starWars) :- agent(Agent0),agent(Agent1),placename(PlaceName2),placename(PlaceName3).
  ifluent(perm(intHerosJourney(Agent0,Agent1,PlaceName2,PlaceName3)),starWars) :- agent(Agent0),agent(Agent1),placename(PlaceName2),placename(PlaceName3).
  fluent(pow(starWars,intHerosJourney(Agent0,Agent1,PlaceName2,PlaceName3)),starWars) :- agent(Agent0),agent(Agent1),placename(PlaceName2),placename(PlaceName3).
  fluent(perm(intHerosJourney(Agent0,Agent1,PlaceName2,PlaceName3)),starWars) :- agent(Agent0),agent(Agent1),placename(PlaceName2),placename(PlaceName3).
  event(viol(intHerosJourney(Agent0,Agent1,PlaceName2,PlaceName3))) :- agent(Agent0),agent(Agent1),placename(PlaceName2),placename(PlaceName3).
  evtype(viol(intHerosJourney(Agent0,Agent1,PlaceName2,PlaceName3)),starWars,viol) :- agent(Agent0),agent(Agent1),placename(PlaceName2),placename(PlaceName3).
  evinst(viol(intHerosJourney(Agent0,Agent1,PlaceName2,PlaceName3)),starWars) :- agent(Agent0),agent(Agent1),placename(PlaceName2),placename(PlaceName3).
%
% Violation events
%
% Event: noViolation (type: in)
  event(noViolation) :- true.
  evtype(noViolation,starWars,viol) :- true.
  evinst(noViolation,starWars) :- true.
%
% Creation events
%
%
% Dissolution events
%
%
% dissolve events
%
%
% inertial fluents
%
ifluent(phase(Trope0,Phase1),starWars) :-
  trope(Trope0),phase(Phase1).
fluent(phase(Trope0,Phase1),starWars) :-
  trope(Trope0),phase(Phase1).

ifluent(place(PlaceName0,Place1),starWars) :-
  placename(PlaceName0),place(Place1).
fluent(place(PlaceName0,Place1),starWars) :-
  placename(PlaceName0),place(Place1).

ifluent(object(ObjectName0,Object1),starWars) :-
  objectname(ObjectName0),object(Object1).
fluent(object(ObjectName0,Object1),starWars) :-
  objectname(ObjectName0),object(Object1).

ifluent(role(Agent0,Role1),starWars) :-
  agent(Agent0),role(Role1).
fluent(role(Agent0,Role1),starWars) :-
  agent(Agent0),role(Role1).

ifluent(at(Agent0,Place1),starWars) :-
  agent(Agent0),place(Place1).
fluent(at(Agent0,Place1),starWars) :-
  agent(Agent0),place(Place1).

%
% noninertial fluents
%
%
% violation fluents (to be implemented)

%
% obligation fluents
%
%
% -------------------------------PART 2-------------------------------
%
%
% generate rules
%
%
% Translation of meet(R,S) generates intHerosJourney(R,S,T,U) if ['and', ['role', ['S', 'dispatcher']], ['role', ['R', 'hero']]] in 
occurred(intHerosJourney(R,S,T,U),starWars,I) :- occurred(meet(R,S),starWars,I),
   holdsat(pow(starWars,intHerosJourney(R,S,T,U)),starWars,I),
   holdsat(role(S,dispatcher),starWars,I),
   holdsat(role(R,hero),starWars,I),
   agent(S),
   agent(R),
   placename(U),
   placename(T),
   inst(starWars), instant(I).
%
% Translation of go(R,U) generates intHerosJourney(R,S,T,U) if ['and', ['role', ['R', 'hero']], ['place', ['U', 'home']]] in 
occurred(intHerosJourney(R,S,T,U),starWars,I) :- occurred(go(R,U),starWars,I),
   holdsat(pow(starWars,intHerosJourney(R,S,T,U)),starWars,I),
   holdsat(role(R,hero),starWars,I),
   holdsat(place(U,home),starWars,I),
   agent(R),
   placename(U),
   agent(S),
   placename(T),
   inst(starWars), instant(I).
%
% Translation of go(R,T) generates intHerosJourney(R,S,T,U) if ['and', ['role', ['R', 'hero']], ['place', ['T', 'away']]] in 
occurred(intHerosJourney(R,S,T,U),starWars,I) :- occurred(go(R,T),starWars,I),
   holdsat(pow(starWars,intHerosJourney(R,S,T,U)),starWars,I),
   holdsat(role(R,hero),starWars,I),
   holdsat(place(T,away),starWars,I),
   agent(R),
   placename(T),
   agent(S),
   placename(U),
   inst(starWars), instant(I).
%
% initiate rules
%
%
% Translation of intHerosJourney(R,S,T,U) initiates ['phase', ['herosJourney', 'done']] if ['phase', ['herosJourney', 'phaseD']]
%
initiated(phase(herosJourney,done),starWars,I) :-
   occurred(intHerosJourney(R,S,T,U),starWars,I),
   holdsat(live(starWars),starWars,I), inst(starWars),
   holdsat(phase(herosJourney,phaseD),starWars,I),
   agent(S),
   agent(R),
   placename(U),
   placename(T),
   inst(starWars), instant(I).
%
% Translation of intHerosJourney(R,S,T,U) initiates ['phase', ['herosJourney', 'phaseD']] if ['and', ['and', ['phase', ['herosJourney', 'phaseC']], ['role', ['R', 'hero']]], ['place', ['U', 'home']]]
%
initiated(phase(herosJourney,phaseD),starWars,I) :-
   occurred(intHerosJourney(R,S,T,U),starWars,I),
   holdsat(live(starWars),starWars,I), inst(starWars),
   holdsat(phase(herosJourney,phaseC),starWars,I),
   holdsat(role(R,hero),starWars,I),
   holdsat(place(U,home),starWars,I),
   agent(S),
   agent(R),
   placename(U),
   placename(T),
   inst(starWars), instant(I).
%
% Translation of intHerosJourney(R,S,T,U) initiates ['perm', ['go', ['R', 'U']]] if ['and', ['and', ['phase', ['herosJourney', 'phaseC']], ['role', ['R', 'hero']]], ['place', ['U', 'home']]]
%
initiated(perm(go(R,U)),starWars,I) :-
   occurred(intHerosJourney(R,S,T,U),starWars,I),
   holdsat(live(starWars),starWars,I), inst(starWars),
   holdsat(phase(herosJourney,phaseC),starWars,I),
   holdsat(role(R,hero),starWars,I),
   holdsat(place(U,home),starWars,I),
   agent(S),
   agent(R),
   placename(U),
   placename(T),
   inst(starWars), instant(I).
%
% Translation of intHerosJourney(R,S,T,U) initiates ['phase', ['herosJourney', 'phaseC']] if ['and', ['and', ['phase', ['herosJourney', 'phaseB']], ['role', ['R', 'hero']]], ['place', ['T', 'away']]]
%
initiated(phase(herosJourney,phaseC),starWars,I) :-
   occurred(intHerosJourney(R,S,T,U),starWars,I),
   holdsat(live(starWars),starWars,I), inst(starWars),
   holdsat(phase(herosJourney,phaseB),starWars,I),
   holdsat(role(R,hero),starWars,I),
   holdsat(place(T,away),starWars,I),
   agent(S),
   agent(R),
   placename(U),
   placename(T),
   inst(starWars), instant(I).
%
% Translation of intHerosJourney(R,S,T,U) initiates ['perm', ['go', ['R', 'T']]] if ['and', ['and', ['phase', ['herosJourney', 'phaseB']], ['role', ['R', 'hero']]], ['place', ['T', 'away']]]
%
initiated(perm(go(R,T)),starWars,I) :-
   occurred(intHerosJourney(R,S,T,U),starWars,I),
   holdsat(live(starWars),starWars,I), inst(starWars),
   holdsat(phase(herosJourney,phaseB),starWars,I),
   holdsat(role(R,hero),starWars,I),
   holdsat(place(T,away),starWars,I),
   agent(S),
   agent(R),
   placename(U),
   placename(T),
   inst(starWars), instant(I).
%
% Translation of intHerosJourney(R,S,T,U) initiates ['phase', ['herosJourney', 'phaseB']] if ['and', ['and', ['phase', ['herosJourney', 'phaseA']], ['role', ['S', 'dispatcher']]], ['role', ['R', 'hero']]]
%
initiated(phase(herosJourney,phaseB),starWars,I) :-
   occurred(intHerosJourney(R,S,T,U),starWars,I),
   holdsat(live(starWars),starWars,I), inst(starWars),
   holdsat(phase(herosJourney,phaseA),starWars,I),
   holdsat(role(S,dispatcher),starWars,I),
   holdsat(role(R,hero),starWars,I),
   agent(S),
   agent(R),
   placename(U),
   placename(T),
   inst(starWars), instant(I).
%
% Translation of intHerosJourney(R,S,T,U) initiates ['perm', ['meet', ['R', 'S']]] if ['and', ['and', ['phase', ['herosJourney', 'phaseA']], ['role', ['S', 'dispatcher']]], ['role', ['R', 'hero']]]
%
initiated(perm(meet(R,S)),starWars,I) :-
   occurred(intHerosJourney(R,S,T,U),starWars,I),
   holdsat(live(starWars),starWars,I), inst(starWars),
   holdsat(phase(herosJourney,phaseA),starWars,I),
   holdsat(role(S,dispatcher),starWars,I),
   holdsat(role(R,hero),starWars,I),
   agent(S),
   agent(R),
   placename(U),
   placename(T),
   inst(starWars), instant(I).
%
% Translation of intHerosJourney(R,S,T,U) initiates ['phase', ['herosJourney', 'phaseA']] if ['and', ['and', ['phase', ['herosJourney', 'inactive']], ['role', ['R', 'hero']]], ['place', ['U', 'home']]]
%
initiated(phase(herosJourney,phaseA),starWars,I) :-
   occurred(intHerosJourney(R,S,T,U),starWars,I),
   holdsat(live(starWars),starWars,I), inst(starWars),
   holdsat(phase(herosJourney,inactive),starWars,I),
   holdsat(role(R,hero),starWars,I),
   holdsat(place(U,home),starWars,I),
   agent(S),
   agent(R),
   placename(U),
   placename(T),
   inst(starWars), instant(I).
%
% Translation of intHerosJourney(R,S,T,U) initiates ['perm', ['go', ['R', 'U']]] if ['and', ['and', ['phase', ['herosJourney', 'inactive']], ['role', ['R', 'hero']]], ['place', ['U', 'home']]]
%
initiated(perm(go(R,U)),starWars,I) :-
   occurred(intHerosJourney(R,S,T,U),starWars,I),
   holdsat(live(starWars),starWars,I), inst(starWars),
   holdsat(phase(herosJourney,inactive),starWars,I),
   holdsat(role(R,hero),starWars,I),
   holdsat(place(U,home),starWars,I),
   agent(S),
   agent(R),
   placename(U),
   placename(T),
   inst(starWars), instant(I).
%
% terminate rules
%
%
% Translation of intHerosJourney(R,S,T,U) terminates ['phase', ['herosJourney', 'done']] if ['phase', ['herosJourney', 'done']]
%
terminated(phase(herosJourney,done),starWars,I) :-
   occurred(intHerosJourney(R,S,T,U),starWars,I),
   holdsat(live(starWars),starWars,I),inst(starWars),
   holdsat(phase(herosJourney,done),starWars,I),
   agent(S),
   agent(R),
   placename(U),
   placename(T),
   inst(starWars), instant(I).
%
% Translation of intHerosJourney(R,S,T,U) terminates ['phase', ['herosJourney', 'phaseD']] if ['phase', ['herosJourney', 'phaseD']]
%
terminated(phase(herosJourney,phaseD),starWars,I) :-
   occurred(intHerosJourney(R,S,T,U),starWars,I),
   holdsat(live(starWars),starWars,I),inst(starWars),
   holdsat(phase(herosJourney,phaseD),starWars,I),
   agent(S),
   agent(R),
   placename(U),
   placename(T),
   inst(starWars), instant(I).
%
% Translation of intHerosJourney(R,S,T,U) terminates ['perm', ['go', ['R', 'U']]] if ['phase', ['herosJourney', 'phaseD']]
%
terminated(perm(go(R,U)),starWars,I) :-
   occurred(intHerosJourney(R,S,T,U),starWars,I),
   holdsat(live(starWars),starWars,I),inst(starWars),
   holdsat(phase(herosJourney,phaseD),starWars,I),
   agent(S),
   agent(R),
   placename(U),
   placename(T),
   inst(starWars), instant(I).
%
% Translation of intHerosJourney(R,S,T,U) terminates ['phase', ['herosJourney', 'phaseC']] if ['phase', ['herosJourney', 'phaseC']]
%
terminated(phase(herosJourney,phaseC),starWars,I) :-
   occurred(intHerosJourney(R,S,T,U),starWars,I),
   holdsat(live(starWars),starWars,I),inst(starWars),
   holdsat(phase(herosJourney,phaseC),starWars,I),
   agent(S),
   agent(R),
   placename(U),
   placename(T),
   inst(starWars), instant(I).
%
% Translation of intHerosJourney(R,S,T,U) terminates ['perm', ['go', ['R', 'T']]] if ['phase', ['herosJourney', 'phaseC']]
%
terminated(perm(go(R,T)),starWars,I) :-
   occurred(intHerosJourney(R,S,T,U),starWars,I),
   holdsat(live(starWars),starWars,I),inst(starWars),
   holdsat(phase(herosJourney,phaseC),starWars,I),
   agent(S),
   agent(R),
   placename(U),
   placename(T),
   inst(starWars), instant(I).
%
% Translation of intHerosJourney(R,S,T,U) terminates ['phase', ['herosJourney', 'phaseB']] if ['phase', ['herosJourney', 'phaseB']]
%
terminated(phase(herosJourney,phaseB),starWars,I) :-
   occurred(intHerosJourney(R,S,T,U),starWars,I),
   holdsat(live(starWars),starWars,I),inst(starWars),
   holdsat(phase(herosJourney,phaseB),starWars,I),
   agent(S),
   agent(R),
   placename(U),
   placename(T),
   inst(starWars), instant(I).
%
% Translation of intHerosJourney(R,S,T,U) terminates ['perm', ['meet', ['R', 'S']]] if ['phase', ['herosJourney', 'phaseB']]
%
terminated(perm(meet(R,S)),starWars,I) :-
   occurred(intHerosJourney(R,S,T,U),starWars,I),
   holdsat(live(starWars),starWars,I),inst(starWars),
   holdsat(phase(herosJourney,phaseB),starWars,I),
   agent(S),
   agent(R),
   placename(U),
   placename(T),
   inst(starWars), instant(I).
%
% Translation of intHerosJourney(R,S,T,U) terminates ['phase', ['herosJourney', 'phaseA']] if ['phase', ['herosJourney', 'phaseA']]
%
terminated(phase(herosJourney,phaseA),starWars,I) :-
   occurred(intHerosJourney(R,S,T,U),starWars,I),
   holdsat(live(starWars),starWars,I),inst(starWars),
   holdsat(phase(herosJourney,phaseA),starWars,I),
   agent(S),
   agent(R),
   placename(U),
   placename(T),
   inst(starWars), instant(I).
%
% Translation of intHerosJourney(R,S,T,U) terminates ['perm', ['go', ['R', 'U']]] if ['phase', ['herosJourney', 'phaseA']]
%
terminated(perm(go(R,U)),starWars,I) :-
   occurred(intHerosJourney(R,S,T,U),starWars,I),
   holdsat(live(starWars),starWars,I),inst(starWars),
   holdsat(phase(herosJourney,phaseA),starWars,I),
   agent(S),
   agent(R),
   placename(U),
   placename(T),
   inst(starWars), instant(I).
%
% Translation of intHerosJourney(R,S,T,U) terminates ['phase', ['herosJourney', 'inactive']] if ['phase', ['herosJourney', 'inactive']]
%
terminated(phase(herosJourney,inactive),starWars,I) :-
   occurred(intHerosJourney(R,S,T,U),starWars,I),
   holdsat(live(starWars),starWars,I),inst(starWars),
   holdsat(phase(herosJourney,inactive),starWars,I),
   agent(S),
   agent(R),
   placename(U),
   placename(T),
   inst(starWars), instant(I).
%
% noninertial rules
%
%
% -------------------------------PART 3-------------------------------
%
%
% initially
%
% no creation event
holdsat(live(starWars),starWars,I) :- start(I), inst(starWars).
holdsat(perm(null),starWars,I) :- start(I), inst(starWars).
% initially: pow(starWars,intHerosJourney(R,S,T,U))
% condition: ['and', ['and', ['!=', ['R', 'S']], ['!=', ['S', 'T']]], ['!=', ['T', 'U']]]
holdsat(pow(starWars,intHerosJourney(R,S,T,U)),starWars,I) :-
   agent(S),
   agent(R),
   placename(U),
   placename(T),
   R!=S,
   S!=T,
   T!=U,
   inst(starWars), start(I).
% initially: phase(herosJourney,inactive)
holdsat(phase(herosJourney,inactive),starWars,I) :-
   inst(starWars), start(I).
% initially: role(lukeSkywalker,hero)
holdsat(role(lukeSkywalker,hero),starWars,I) :-
   inst(starWars), start(I).
% initially: role(obiWan,dispatcher)
holdsat(role(obiWan,dispatcher),starWars,I) :-
   inst(starWars), start(I).
% initially: place(tatooine,home)
holdsat(place(tatooine,home),starWars,I) :-
   inst(starWars), start(I).
% initially: place(space,away)
holdsat(place(space,away),starWars,I) :-
   inst(starWars), start(I).
%
% End of file
%
