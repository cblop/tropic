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
%
% Rules for Institution starWars
%
  ifluent(live(starWars), starWars).
  fluent(live(starWars), starWars).
  inst(starWars).
%
% Constraints for obserable events depending on mode option
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
  event(noDeadline(Agent0)) :- agent(Agent0).
  evtype(noDeadline(Agent0),starWars,ex) :- agent(Agent0).
  evinst(noDeadline(Agent0),starWars) :- agent(Agent0).
  ifluent(perm(noDeadline(Agent0)), starWars) :- agent(Agent0).
  fluent(perm(noDeadline(Agent0)), starWars) :- agent(Agent0).
  event(viol(noDeadline(Agent0))) :- agent(Agent0).
  evtype(viol(noDeadline(Agent0)), starWars, viol) :- agent(Agent0).
  evinst(viol(noDeadline(Agent0)),starWars) :- agent(Agent0).
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
  event(noViolation(Agent0)) :- agent(Agent0).
  evtype(noViolation(Agent0),starWars,viol) :- agent(Agent0).
  evinst(noViolation(Agent0),starWars) :- agent(Agent0).
%
% Creation events
%
% Event: startShow (type: ex)
  event(startShow) :- true.
  evtype(startShow,starWars,ex) :- true.
  evinst(startShow,starWars) :- true.
  ifluent(perm(startShow),starWars) :- true.
  fluent(perm(startShow),starWars) :- true.
  event(viol(startShow)) :- true.
  evtype(viol(startShow),starWars,viol) :- true.
  evinst(viol(startShow),starWars) :- true.
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
oblfluent(obl(go(Agent0,PlaceName1),noDeadline(Agent2),noViolation(Agent3)), starWars) :-
   event(go(Agent0,PlaceName1)),
   event(noDeadline(Agent2)),
   event(noViolation(Agent3)), agent(Agent0),placename(PlaceName1),agent(Agent2),agent(Agent3),inst(starWars).
ifluent(obl(go(Agent0,PlaceName1),noDeadline(Agent2),noViolation(Agent3)), starWars) :-
   event(go(Agent0,PlaceName1)),
   event(noDeadline(Agent2)),
   event(noViolation(Agent3)), agent(Agent0),placename(PlaceName1),agent(Agent2),agent(Agent3),inst(starWars).
fluent(obl(go(Agent0,PlaceName1),noDeadline(Agent2),noViolation(Agent3)), starWars) :-
   event(go(Agent0,PlaceName1)),
   event(noDeadline(Agent2)),
   event(noViolation(Agent3)), agent(Agent0),placename(PlaceName1),agent(Agent2),agent(Agent3),inst(starWars).
terminated(obl(go(Agent0,PlaceName1),noDeadline(Agent2),noViolation(Agent3)),starWars,I) :-
   event(go(Agent0,PlaceName1)), occurred(go(Agent0,PlaceName1),starWars,I),
   event(noDeadline(Agent2)),
   holdsat(obl(go(Agent0,PlaceName1),noDeadline(Agent2),noViolation(Agent3)),starWars,I),
   event(noViolation(Agent3)), agent(Agent0),placename(PlaceName1),agent(Agent2),agent(Agent3),inst(starWars).
terminated(obl(go(Agent0,PlaceName1),noDeadline(Agent2),noViolation(Agent3)),starWars,I) :-
   event(go(Agent0,PlaceName1)), 
   event(noDeadline(Agent2)), occurred(noDeadline(Agent2),starWars,I),
   holdsat(obl(go(Agent0,PlaceName1),noDeadline(Agent2),noViolation(Agent3)),starWars,I),
   event(noViolation(Agent3)), agent(Agent0),placename(PlaceName1),agent(Agent2),agent(Agent3),inst(starWars).
occurred(noViolation(Agent3),starWars,I) :-
   event(go(Agent0,PlaceName1)), 
   event(noDeadline(Agent2)), occurred(noDeadline(Agent2),starWars,I),
   holdsat(obl(go(Agent0,PlaceName1),noDeadline(Agent2),noViolation(Agent3)),starWars,I),
   event(noViolation(Agent3)), agent(Agent0),placename(PlaceName1),agent(Agent2),agent(Agent3),inst(starWars).
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
% Translation of intHerosJourney(R,S,T,U) initiates ['phase', ['herosJourney', 'phaseC']] if ['and', ['and', ['phase', ['herosJourney', 'phaseB']], ['role', ['S', 'dispatcher']]], ['role', ['R', 'hero']]]
%
initiated(phase(herosJourney,phaseC),starWars,I) :-
   occurred(intHerosJourney(R,S,T,U),starWars,I),
   holdsat(live(starWars),starWars,I), inst(starWars),
   holdsat(phase(herosJourney,phaseB),starWars,I),
   holdsat(role(S,dispatcher),starWars,I),
   holdsat(role(R,hero),starWars,I),
   agent(S),
   agent(R),
   placename(U),
   placename(T),
   inst(starWars), instant(I).
%
% Translation of intHerosJourney(R,S,T,U) initiates ['perm', ['meet', ['R', 'S']]] if ['and', ['and', ['phase', ['herosJourney', 'phaseB']], ['role', ['S', 'dispatcher']]], ['role', ['R', 'hero']]]
%
initiated(perm(meet(R,S)),starWars,I) :-
   occurred(intHerosJourney(R,S,T,U),starWars,I),
   holdsat(live(starWars),starWars,I), inst(starWars),
   holdsat(phase(herosJourney,phaseB),starWars,I),
   holdsat(role(S,dispatcher),starWars,I),
   holdsat(role(R,hero),starWars,I),
   agent(S),
   agent(R),
   placename(U),
   placename(T),
   inst(starWars), instant(I).
%
% Translation of intHerosJourney(R,S,T,U) initiates ['phase', ['herosJourney', 'phaseB']] if ['and', ['phase', ['herosJourney', 'phaseA']], ['role', ['R', 'hero']]]
%
initiated(phase(herosJourney,phaseB),starWars,I) :-
   occurred(intHerosJourney(R,S,T,U),starWars,I),
   holdsat(live(starWars),starWars,I), inst(starWars),
   holdsat(phase(herosJourney,phaseA),starWars,I),
   holdsat(role(R,hero),starWars,I),
   agent(S),
   agent(R),
   placename(U),
   placename(T),
   inst(starWars), instant(I).
%
% Translation of intHerosJourney(R,S,T,U) initiates ['obl', [['go', ['Agent', 'PlaceName']], ['noDeadline', ['Agent']], ['noViolation', ['Agent']]]] if ['and', ['phase', ['herosJourney', 'phaseA']], ['role', ['R', 'hero']]]
%
initiated(obl(go(Agent,PlaceName),noDeadline(Agent),noViolation(Agent)),starWars,I) :-
   occurred(intHerosJourney(R,S,T,U),starWars,I),
   holdsat(live(starWars),starWars,I), inst(starWars),
   holdsat(phase(herosJourney,phaseA),starWars,I),
   holdsat(role(R,hero),starWars,I),
   agent(S),
   agent(R),
   placename(U),
   placename(T),
   placename(PlaceName),
   agent(Agent),
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
% Translation of intHerosJourney(R,S,T,U) terminates ['perm', ['meet', ['R', 'S']]] if ['phase', ['herosJourney', 'phaseC']]
%
terminated(perm(meet(R,S)),starWars,I) :-
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
% Translation of intHerosJourney(R,S,T,U) terminates ['obl', [['go', ['R', 'T']], ['noDeadline', []], ['noViolation', []]]] if ['phase', ['herosJourney', 'phaseB']]
%
terminated(obl(go(R,T),noDeadline,noViolation),starWars,I) :-
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
% at least one create event
%
% clear state to allow for re-creation
%
terminated(F,starWars,I) :-
   occurred(startShow,starWars,I),
   not holdsat(live(starWars),starWars,I),
   holdsat(F,starWars,I),
   instant(I), inst(starWars).
initiated(live(starWars),starWars,I) :-
   occurred(startShow,starWars,I),
   not holdsat(live(starWars),starWars,I),
   instant(I),inst(starWars).
initiated(perm(null),starWars,I) :-
   occurred(startShow,starWars,I),
   not holdsat(live(starWars),starWars,I),
   instant(I),inst(starWars).
%
% set up initial state
%
% initially: pow(starWars,intHerosJourney(R,S,T,U))
initiated(pow(starWars,intHerosJourney(R,S,T,U)),starWars,I) :-
   occurred(startShow,starWars,I),
   not holdsat(live(starWars),starWars,I), inst(starWars),
   agent(S),
   agent(R),
   placename(U),
   placename(T),
   inst(starWars), instant(I).
% initially: phase(herosJourney,inactive)
initiated(phase(herosJourney,inactive),starWars,I) :-
   occurred(startShow,starWars,I),
   not holdsat(live(starWars),starWars,I), inst(starWars),
   inst(starWars), instant(I).
% initially: role(lukeSkywalker,hero)
initiated(role(lukeSkywalker,hero),starWars,I) :-
   occurred(startShow,starWars,I),
   not holdsat(live(starWars),starWars,I), inst(starWars),
   inst(starWars), instant(I).
% initially: role(obiWan,dispatcher)
initiated(role(obiWan,dispatcher),starWars,I) :-
   occurred(startShow,starWars,I),
   not holdsat(live(starWars),starWars,I), inst(starWars),
   inst(starWars), instant(I).
% initially: place(tatooine,home)
initiated(place(tatooine,home),starWars,I) :-
   occurred(startShow,starWars,I),
   not holdsat(live(starWars),starWars,I), inst(starWars),
   inst(starWars), instant(I).
% initially: place(space,away)
initiated(place(space,away),starWars,I) :-
   occurred(startShow,starWars,I),
   not holdsat(live(starWars),starWars,I), inst(starWars),
   inst(starWars), instant(I).
%
% End of file
%
