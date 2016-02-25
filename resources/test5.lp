%
% Domain declarations for noname
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
% Standard prelude for noname
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
% Rules for Institution noname
%
  ifluent(live(noname), noname).
  fluent(live(noname), noname).
  inst(noname).
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
  evtype(go(Agent0,PlaceName1),noname,ex) :- agent(Agent0),placename(PlaceName1).
  evinst(go(Agent0,PlaceName1),noname) :- agent(Agent0),placename(PlaceName1).
  ifluent(perm(go(Agent0,PlaceName1)), noname) :- agent(Agent0),placename(PlaceName1).
  fluent(perm(go(Agent0,PlaceName1)), noname) :- agent(Agent0),placename(PlaceName1).
  event(viol(go(Agent0,PlaceName1))) :- agent(Agent0),placename(PlaceName1).
  evtype(viol(go(Agent0,PlaceName1)), noname, viol) :- agent(Agent0),placename(PlaceName1).
  evinst(viol(go(Agent0,PlaceName1)),noname) :- agent(Agent0),placename(PlaceName1).
% Event: meet (type: ex)
  event(meet(Agent0,Agent1)) :- agent(Agent0),agent(Agent1).
  evtype(meet(Agent0,Agent1),noname,ex) :- agent(Agent0),agent(Agent1).
  evinst(meet(Agent0,Agent1),noname) :- agent(Agent0),agent(Agent1).
  ifluent(perm(meet(Agent0,Agent1)), noname) :- agent(Agent0),agent(Agent1).
  fluent(perm(meet(Agent0,Agent1)), noname) :- agent(Agent0),agent(Agent1).
  event(viol(meet(Agent0,Agent1))) :- agent(Agent0),agent(Agent1).
  evtype(viol(meet(Agent0,Agent1)), noname, viol) :- agent(Agent0),agent(Agent1).
  evinst(viol(meet(Agent0,Agent1)),noname) :- agent(Agent0),agent(Agent1).
%
% null event for unknown events
% Event: null (type: ex)
  event(null).
  evtype(null,noname,ex).
  evinst(null,noname).
  ifluent(perm(null), noname).
  fluent(perm(null), noname).
  event(viol(null)).
  evtype(viol(null),noname,viol).
  evinst(viol(null),noname).
% Institutional events
% Event: intGo (type: in)
  event(intGo(Agent0,PlaceName1)) :- agent(Agent0),placename(PlaceName1).
  evtype(intGo(Agent0,PlaceName1),noname,inst) :- agent(Agent0),placename(PlaceName1).
  evinst(intGo(Agent0,PlaceName1),noname) :- agent(Agent0),placename(PlaceName1).
  ifluent(pow(noname,intGo(Agent0,PlaceName1)),noname) :- agent(Agent0),placename(PlaceName1).
  ifluent(perm(intGo(Agent0,PlaceName1)),noname) :- agent(Agent0),placename(PlaceName1).
  fluent(pow(noname,intGo(Agent0,PlaceName1)),noname) :- agent(Agent0),placename(PlaceName1).
  fluent(perm(intGo(Agent0,PlaceName1)),noname) :- agent(Agent0),placename(PlaceName1).
  event(viol(intGo(Agent0,PlaceName1))) :- agent(Agent0),placename(PlaceName1).
  evtype(viol(intGo(Agent0,PlaceName1)),noname,viol) :- agent(Agent0),placename(PlaceName1).
  evinst(viol(intGo(Agent0,PlaceName1)),noname) :- agent(Agent0),placename(PlaceName1).
% Event: intHerosJourney (type: in)
  event(intHerosJourney(Agent0,Agent1,PlaceName2,PlaceName3)) :- agent(Agent0),agent(Agent1),placename(PlaceName2),placename(PlaceName3).
  evtype(intHerosJourney(Agent0,Agent1,PlaceName2,PlaceName3),noname,inst) :- agent(Agent0),agent(Agent1),placename(PlaceName2),placename(PlaceName3).
  evinst(intHerosJourney(Agent0,Agent1,PlaceName2,PlaceName3),noname) :- agent(Agent0),agent(Agent1),placename(PlaceName2),placename(PlaceName3).
  ifluent(pow(noname,intHerosJourney(Agent0,Agent1,PlaceName2,PlaceName3)),noname) :- agent(Agent0),agent(Agent1),placename(PlaceName2),placename(PlaceName3).
  ifluent(perm(intHerosJourney(Agent0,Agent1,PlaceName2,PlaceName3)),noname) :- agent(Agent0),agent(Agent1),placename(PlaceName2),placename(PlaceName3).
  fluent(pow(noname,intHerosJourney(Agent0,Agent1,PlaceName2,PlaceName3)),noname) :- agent(Agent0),agent(Agent1),placename(PlaceName2),placename(PlaceName3).
  fluent(perm(intHerosJourney(Agent0,Agent1,PlaceName2,PlaceName3)),noname) :- agent(Agent0),agent(Agent1),placename(PlaceName2),placename(PlaceName3).
  event(viol(intHerosJourney(Agent0,Agent1,PlaceName2,PlaceName3))) :- agent(Agent0),agent(Agent1),placename(PlaceName2),placename(PlaceName3).
  evtype(viol(intHerosJourney(Agent0,Agent1,PlaceName2,PlaceName3)),noname,viol) :- agent(Agent0),agent(Agent1),placename(PlaceName2),placename(PlaceName3).
  evinst(viol(intHerosJourney(Agent0,Agent1,PlaceName2,PlaceName3)),noname) :- agent(Agent0),agent(Agent1),placename(PlaceName2),placename(PlaceName3).
%
% Violation events
%
%
% Creation events
%
% Event: startShow (type: ex)
  event(startShow) :- true.
  evtype(startShow,noname,ex) :- true.
  evinst(startShow,noname) :- true.
  ifluent(perm(startShow),noname) :- true.
  fluent(perm(startShow),noname) :- true.
  event(viol(startShow)) :- true.
  evtype(viol(startShow),noname,viol) :- true.
  evinst(viol(startShow),noname) :- true.
%
% Dissolution events
%
%
% dissolve events
%
%
% inertial fluents
%
ifluent(phase(Trope0,Phase1),noname) :-
  trope(Trope0),phase(Phase1).
fluent(phase(Trope0,Phase1),noname) :-
  trope(Trope0),phase(Phase1).

ifluent(place(PlaceName0,Place1),noname) :-
  placename(PlaceName0),place(Place1).
fluent(place(PlaceName0,Place1),noname) :-
  placename(PlaceName0),place(Place1).

ifluent(object(ObjectName0,Object1),noname) :-
  objectname(ObjectName0),object(Object1).
fluent(object(ObjectName0,Object1),noname) :-
  objectname(ObjectName0),object(Object1).

ifluent(role(Agent0,Role1),noname) :-
  agent(Agent0),role(Role1).
fluent(role(Agent0,Role1),noname) :-
  agent(Agent0),role(Role1).

ifluent(at(Agent0,Place1),noname) :-
  agent(Agent0),place(Place1).
fluent(at(Agent0,Place1),noname) :-
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
% initiate rules
%
%
% Translation of intHerosJourney(R,S,T,U) initiates ['phase', ['herosJourney', 'phaseC']] if ['and', ['and', ['phase', ['herosJourney', 'phaseB']], ['role', ['R', 'hero']]], ['place', ['U', 'home']]]
%
initiated(phase(herosJourney,phaseC),noname,I) :-
   occurred(intHerosJourney(R,S,T,U),noname,I),
   holdsat(live(noname),noname,I), inst(noname),
   holdsat(phase(herosJourney,phaseB),noname,I),
   holdsat(role(R,hero),noname,I),
   holdsat(place(U,home),noname,I),
   agent(S),
   agent(R),
   placename(U),
   placename(T),
   inst(noname), instant(I).
%
% Translation of intHerosJourney(R,S,T,U) initiates ['perm', ['go', ['R', 'U']]] if ['and', ['and', ['phase', ['herosJourney', 'phaseB']], ['role', ['R', 'hero']]], ['place', ['U', 'home']]]
%
initiated(perm(go(R,U)),noname,I) :-
   occurred(intHerosJourney(R,S,T,U),noname,I),
   holdsat(live(noname),noname,I), inst(noname),
   holdsat(phase(herosJourney,phaseB),noname,I),
   holdsat(role(R,hero),noname,I),
   holdsat(place(U,home),noname,I),
   agent(S),
   agent(R),
   placename(U),
   placename(T),
   inst(noname), instant(I).
%
% Translation of intHerosJourney(R,S,T,U) initiates ['phase', ['herosJourney', 'phaseB']] if ['and', ['and', ['phase', ['herosJourney', 'phaseA']], ['role', ['S', 'dispatcher']]], ['role', ['R', 'hero']]]
%
initiated(phase(herosJourney,phaseB),noname,I) :-
   occurred(intHerosJourney(R,S,T,U),noname,I),
   holdsat(live(noname),noname,I), inst(noname),
   holdsat(phase(herosJourney,phaseA),noname,I),
   holdsat(role(S,dispatcher),noname,I),
   holdsat(role(R,hero),noname,I),
   agent(S),
   agent(R),
   placename(U),
   placename(T),
   inst(noname), instant(I).
%
% Translation of intHerosJourney(R,S,T,U) initiates ['perm', ['meet', ['R', 'S']]] if ['and', ['and', ['phase', ['herosJourney', 'phaseA']], ['role', ['S', 'dispatcher']]], ['role', ['R', 'hero']]]
%
initiated(perm(meet(R,S)),noname,I) :-
   occurred(intHerosJourney(R,S,T,U),noname,I),
   holdsat(live(noname),noname,I), inst(noname),
   holdsat(phase(herosJourney,phaseA),noname,I),
   holdsat(role(S,dispatcher),noname,I),
   holdsat(role(R,hero),noname,I),
   agent(S),
   agent(R),
   placename(U),
   placename(T),
   inst(noname), instant(I).
%
% Translation of intHerosJourney(R,S,T,U) initiates ['phase', ['herosJourney', 'phaseA']] if ['and', ['and', ['phase', ['herosJourney', 'inactive']], ['role', ['R', 'hero']]], ['place', ['U', 'home']]]
%
initiated(phase(herosJourney,phaseA),noname,I) :-
   occurred(intHerosJourney(R,S,T,U),noname,I),
   holdsat(live(noname),noname,I), inst(noname),
   holdsat(phase(herosJourney,inactive),noname,I),
   holdsat(role(R,hero),noname,I),
   holdsat(place(U,home),noname,I),
   agent(S),
   agent(R),
   placename(U),
   placename(T),
   inst(noname), instant(I).
%
% Translation of intHerosJourney(R,S,T,U) initiates ['perm', ['go', ['R', 'U']]] if ['and', ['and', ['phase', ['herosJourney', 'inactive']], ['role', ['R', 'hero']]], ['place', ['U', 'home']]]
%
initiated(perm(go(R,U)),noname,I) :-
   occurred(intHerosJourney(R,S,T,U),noname,I),
   holdsat(live(noname),noname,I), inst(noname),
   holdsat(phase(herosJourney,inactive),noname,I),
   holdsat(role(R,hero),noname,I),
   holdsat(place(U,home),noname,I),
   agent(S),
   agent(R),
   placename(U),
   placename(T),
   inst(noname), instant(I).
%
% terminate rules
%
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
terminated(F,noname,I) :-
   occurred(startShow,noname,I),
   not holdsat(live(noname),noname,I),
   holdsat(F,noname,I),
   instant(I), inst(noname).
initiated(live(noname),noname,I) :-
   occurred(startShow,noname,I),
   not holdsat(live(noname),noname,I),
   instant(I),inst(noname).
initiated(perm(null),noname,I) :-
   occurred(startShow,noname,I),
   not holdsat(live(noname),noname,I),
   instant(I),inst(noname).
%
% set up initial state
%
%
% End of file
%
