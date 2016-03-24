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
instant(0).
next(0,1).
instant(1).
next(1,2).
instant(2).
next(2,3).
instant(3).
next(3,4).
instant(4).
final(4).
start(0).
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
% Event: intGo (type: in)
  event(intGo(Agent0,PlaceName1)) :- agent(Agent0),placename(PlaceName1).
  evtype(intGo(Agent0,PlaceName1),starWars,inst) :- agent(Agent0),placename(PlaceName1).
  evinst(intGo(Agent0,PlaceName1),starWars) :- agent(Agent0),placename(PlaceName1).
  ifluent(pow(starWars,intGo(Agent0,PlaceName1)),starWars) :- agent(Agent0),placename(PlaceName1).
  ifluent(perm(intGo(Agent0,PlaceName1)),starWars) :- agent(Agent0),placename(PlaceName1).
  fluent(pow(starWars,intGo(Agent0,PlaceName1)),starWars) :- agent(Agent0),placename(PlaceName1).
  fluent(perm(intGo(Agent0,PlaceName1)),starWars) :- agent(Agent0),placename(PlaceName1).
  event(viol(intGo(Agent0,PlaceName1))) :- agent(Agent0),placename(PlaceName1).
  evtype(viol(intGo(Agent0,PlaceName1)),starWars,viol) :- agent(Agent0),placename(PlaceName1).
  evinst(viol(intGo(Agent0,PlaceName1)),starWars) :- agent(Agent0),placename(PlaceName1).
% Event: intHerosJourney (type: in)
  event(intHerosJourney(Agent0,Agent1,Agent2,PlaceName3,PlaceName4)) :- agent(Agent0),agent(Agent1),agent(Agent2),placename(PlaceName3),placename(PlaceName4).
  evtype(intHerosJourney(Agent0,Agent1,Agent2,PlaceName3,PlaceName4),starWars,inst) :- agent(Agent0),agent(Agent1),agent(Agent2),placename(PlaceName3),placename(PlaceName4).
  evinst(intHerosJourney(Agent0,Agent1,Agent2,PlaceName3,PlaceName4),starWars) :- agent(Agent0),agent(Agent1),agent(Agent2),placename(PlaceName3),placename(PlaceName4).
  ifluent(pow(starWars,intHerosJourney(Agent0,Agent1,Agent2,PlaceName3,PlaceName4)),starWars) :- agent(Agent0),agent(Agent1),agent(Agent2),placename(PlaceName3),placename(PlaceName4).
  ifluent(perm(intHerosJourney(Agent0,Agent1,Agent2,PlaceName3,PlaceName4)),starWars) :- agent(Agent0),agent(Agent1),agent(Agent2),placename(PlaceName3),placename(PlaceName4).
  fluent(pow(starWars,intHerosJourney(Agent0,Agent1,Agent2,PlaceName3,PlaceName4)),starWars) :- agent(Agent0),agent(Agent1),agent(Agent2),placename(PlaceName3),placename(PlaceName4).
  fluent(perm(intHerosJourney(Agent0,Agent1,Agent2,PlaceName3,PlaceName4)),starWars) :- agent(Agent0),agent(Agent1),agent(Agent2),placename(PlaceName3),placename(PlaceName4).
  event(viol(intHerosJourney(Agent0,Agent1,Agent2,PlaceName3,PlaceName4))) :- agent(Agent0),agent(Agent1),agent(Agent2),placename(PlaceName3),placename(PlaceName4).
  evtype(viol(intHerosJourney(Agent0,Agent1,Agent2,PlaceName3,PlaceName4)),starWars,viol) :- agent(Agent0),agent(Agent1),agent(Agent2),placename(PlaceName3),placename(PlaceName4).
  evinst(viol(intHerosJourney(Agent0,Agent1,Agent2,PlaceName3,PlaceName4)),starWars) :- agent(Agent0),agent(Agent1),agent(Agent2),placename(PlaceName3),placename(PlaceName4).
%
% Violation events
%
% Event: violHeroGoAway (type: in)
  event(violHeroGoAway) :- true.
  evtype(violHeroGoAway,starWars,viol) :- true.
  evinst(violHeroGoAway,starWars) :- true.
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
oblfluent(obl(go(Agent0,PlaceName1),go(Agent2,PlaceName3),violHeroGoAway), starWars) :-
   event(go(Agent0,PlaceName1)),
   event(go(Agent2,PlaceName3)),
   event(violHeroGoAway), agent(Agent0),placename(PlaceName1),agent(Agent2),placename(PlaceName3),true,inst(starWars).
ifluent(obl(go(Agent0,PlaceName1),go(Agent2,PlaceName3),violHeroGoAway), starWars) :-
   event(go(Agent0,PlaceName1)),
   event(go(Agent2,PlaceName3)),
   event(violHeroGoAway), agent(Agent0),placename(PlaceName1),agent(Agent2),placename(PlaceName3),true,inst(starWars).
fluent(obl(go(Agent0,PlaceName1),go(Agent2,PlaceName3),violHeroGoAway), starWars) :-
   event(go(Agent0,PlaceName1)),
   event(go(Agent2,PlaceName3)),
   event(violHeroGoAway), agent(Agent0),placename(PlaceName1),agent(Agent2),placename(PlaceName3),true,inst(starWars).
terminated(obl(go(Agent0,PlaceName1),go(Agent2,PlaceName3),violHeroGoAway),starWars,I) :-
   event(go(Agent0,PlaceName1)), occurred(go(Agent0,PlaceName1),starWars,I),
   event(go(Agent2,PlaceName3)),
   holdsat(obl(go(Agent0,PlaceName1),go(Agent2,PlaceName3),violHeroGoAway),starWars,I),
   event(violHeroGoAway), agent(Agent0),placename(PlaceName1),agent(Agent2),placename(PlaceName3),true,inst(starWars).
terminated(obl(go(Agent0,PlaceName1),go(Agent2,PlaceName3),violHeroGoAway),starWars,I) :-
   event(go(Agent0,PlaceName1)), 
   event(go(Agent2,PlaceName3)), occurred(go(Agent2,PlaceName3),starWars,I),
   holdsat(obl(go(Agent0,PlaceName1),go(Agent2,PlaceName3),violHeroGoAway),starWars,I),
   event(violHeroGoAway), agent(Agent0),placename(PlaceName1),agent(Agent2),placename(PlaceName3),true,inst(starWars).
occurred(violHeroGoAway,starWars,I) :-
   event(go(Agent0,PlaceName1)), 
   event(go(Agent2,PlaceName3)), occurred(go(Agent2,PlaceName3),starWars,I),
   holdsat(obl(go(Agent0,PlaceName1),go(Agent2,PlaceName3),violHeroGoAway),starWars,I),
   event(violHeroGoAway), agent(Agent0),placename(PlaceName1),agent(Agent2),placename(PlaceName3),true,inst(starWars).
%
% -------------------------------PART 2-------------------------------
%
%
% generate rules
%
%
% Translation of go(R,T) generates intGo(R,T) if ['and', ['role', ['R', 'hero']], ['place', ['T', 'away']]] in 
occurred(intGo(R,T),starWars,I) :- occurred(go(R,T),starWars,I),
   holdsat(pow(starWars,intGo(R,T)),starWars,I),
   holdsat(role(R,hero),starWars,I),
   holdsat(place(T,away),starWars,I),
   agent(R),
   placename(T),
   inst(starWars), instant(I).
%
% Translation of meet(R,T) generates intHerosJourney(R,S,T,U,V) if ['and', ['role', ['T', 'dispatcher']], ['role', ['R', 'hero']]] in 
occurred(intHerosJourney(R,S,T,U,V),starWars,I) :- occurred(meet(R,T),starWars,I),
   holdsat(pow(starWars,intHerosJourney(R,S,T,U,V)),starWars,I),
   holdsat(role(T,dispatcher),starWars,I),
   holdsat(role(R,hero),starWars,I),
   agent(R),
   agent(T),
   agent(S),
   placename(U),
   placename(V),
   inst(starWars), instant(I).
%
% Translation of go(R,V) generates intHerosJourney(R,S,T,U,V) if ['and', ['role', ['R', 'hero']], ['place', ['V', 'home']]] in 
occurred(intHerosJourney(R,S,T,U,V),starWars,I) :- occurred(go(R,V),starWars,I),
   holdsat(pow(starWars,intHerosJourney(R,S,T,U,V)),starWars,I),
   holdsat(role(R,hero),starWars,I),
   holdsat(place(V,home),starWars,I),
   agent(R),
   placename(V),
   agent(S),
   placename(U),
   agent(T),
   inst(starWars), instant(I).
%
% initiate rules
%
%
% Translation of violHeroGoAway initiates ['perm', ['kill', ['R', 'S']]] if ['and', ['role', ['R', 'hero']], ['role', ['S', 'villain']]]
%
initiated(perm(kill(R,S)),starWars,I) :-
   occurred(violHeroGoAway,starWars,I),
   holdsat(live(starWars),starWars,I), inst(starWars),
   holdsat(role(R,hero),starWars,I),
   holdsat(role(S,villain),starWars,I),
   agent(S),
   agent(R),
   inst(starWars), instant(I).
%
% Translation of intHerosJourney(R,S,T,U,V) initiates ['phase', ['herosJourney', 'done']] if ['phase', ['herosJourney', 'phaseD']]
%
initiated(phase(herosJourney,done),starWars,I) :-
   occurred(intHerosJourney(R,S,T,U,V),starWars,I),
   holdsat(live(starWars),starWars,I), inst(starWars),
   holdsat(phase(herosJourney,phaseD),starWars,I),
   agent(S),
   agent(R),
   placename(U),
   agent(T),
   placename(V),
   inst(starWars), instant(I).
%
% Translation of intHerosJourney(R,S,T,U,V) initiates ['phase', ['herosJourney', 'phaseD']] if ['and', ['and', ['phase', ['herosJourney', 'phaseC']], ['role', ['R', 'hero']]], ['place', ['V', 'home']]]
%
initiated(phase(herosJourney,phaseD),starWars,I) :-
   occurred(intHerosJourney(R,S,T,U,V),starWars,I),
   holdsat(live(starWars),starWars,I), inst(starWars),
   holdsat(phase(herosJourney,phaseC),starWars,I),
   holdsat(role(R,hero),starWars,I),
   holdsat(place(V,home),starWars,I),
   agent(S),
   agent(R),
   placename(U),
   agent(T),
   placename(V),
   inst(starWars), instant(I).
%
% Translation of intHerosJourney(R,S,T,U,V) initiates ['perm', ['go', ['R', 'V']]] if ['and', ['and', ['phase', ['herosJourney', 'phaseC']], ['role', ['R', 'hero']]], ['place', ['V', 'home']]]
%
initiated(perm(go(R,V)),starWars,I) :-
   occurred(intHerosJourney(R,S,T,U,V),starWars,I),
   holdsat(live(starWars),starWars,I), inst(starWars),
   holdsat(phase(herosJourney,phaseC),starWars,I),
   holdsat(role(R,hero),starWars,I),
   holdsat(place(V,home),starWars,I),
   agent(S),
   agent(R),
   placename(U),
   agent(T),
   placename(V),
   inst(starWars), instant(I).
%
% Translation of intHerosJourney(R,S,T,U,V) initiates ['phase', ['herosJourney', 'phaseC']] if ['and', ['and', ['phase', ['herosJourney', 'phaseB']], ['role', ['T', 'dispatcher']]], ['role', ['R', 'hero']]]
%
initiated(phase(herosJourney,phaseC),starWars,I) :-
   occurred(intHerosJourney(R,S,T,U,V),starWars,I),
   holdsat(live(starWars),starWars,I), inst(starWars),
   holdsat(phase(herosJourney,phaseB),starWars,I),
   holdsat(role(T,dispatcher),starWars,I),
   holdsat(role(R,hero),starWars,I),
   agent(S),
   agent(R),
   placename(U),
   agent(T),
   placename(V),
   inst(starWars), instant(I).
%
% Translation of intHerosJourney(R,S,T,U,V) initiates ['perm', ['meet', ['R', 'T']]] if ['and', ['and', ['phase', ['herosJourney', 'phaseB']], ['role', ['T', 'dispatcher']]], ['role', ['R', 'hero']]]
%
initiated(perm(meet(R,T)),starWars,I) :-
   occurred(intHerosJourney(R,S,T,U,V),starWars,I),
   holdsat(live(starWars),starWars,I), inst(starWars),
   holdsat(phase(herosJourney,phaseB),starWars,I),
   holdsat(role(T,dispatcher),starWars,I),
   holdsat(role(R,hero),starWars,I),
   agent(S),
   agent(R),
   placename(U),
   agent(T),
   placename(V),
   inst(starWars), instant(I).
%
% Translation of intHerosJourney(R,S,T,U,V) initiates ['phase', ['herosJourney', 'phaseB']] if ['and', ['and', ['and', ['and', ['phase', ['herosJourney', 'phaseA']], ['role', ['R', 'hero']]], ['place', ['U', 'away']]], ['role', ['S', 'villain']]], ['place', ['V', 'home']]]
%
initiated(phase(herosJourney,phaseB),starWars,I) :-
   occurred(intHerosJourney(R,S,T,U,V),starWars,I),
   holdsat(live(starWars),starWars,I), inst(starWars),
   holdsat(phase(herosJourney,phaseA),starWars,I),
   holdsat(role(R,hero),starWars,I),
   holdsat(place(U,away),starWars,I),
   holdsat(role(S,villain),starWars,I),
   holdsat(place(V,home),starWars,I),
   agent(S),
   agent(R),
   placename(U),
   agent(T),
   placename(V),
   inst(starWars), instant(I).
%
% Translation of intHerosJourney(R,S,T,U,V) initiates ['obl', [['go', ['R', 'U']], ['go', ['S', 'V']], ['violHeroGoAway', []]]] if ['and', ['and', ['and', ['and', ['phase', ['herosJourney', 'phaseA']], ['role', ['R', 'hero']]], ['place', ['U', 'away']]], ['role', ['S', 'villain']]], ['place', ['V', 'home']]]
%
initiated(obl(go(R,U),go(S,V),violHeroGoAway),starWars,I) :-
   occurred(intHerosJourney(R,S,T,U,V),starWars,I),
   holdsat(live(starWars),starWars,I), inst(starWars),
   holdsat(phase(herosJourney,phaseA),starWars,I),
   holdsat(role(R,hero),starWars,I),
   holdsat(place(U,away),starWars,I),
   holdsat(role(S,villain),starWars,I),
   holdsat(place(V,home),starWars,I),
   agent(S),
   agent(R),
   placename(U),
   agent(T),
   placename(V),
   inst(starWars), instant(I).
%
% Translation of intHerosJourney(R,S,T,U,V) initiates ['phase', ['herosJourney', 'phaseA']] if ['and', ['and', ['phase', ['herosJourney', 'inactive']], ['role', ['R', 'hero']]], ['place', ['V', 'home']]]
%
initiated(phase(herosJourney,phaseA),starWars,I) :-
   occurred(intHerosJourney(R,S,T,U,V),starWars,I),
   holdsat(live(starWars),starWars,I), inst(starWars),
   holdsat(phase(herosJourney,inactive),starWars,I),
   holdsat(role(R,hero),starWars,I),
   holdsat(place(V,home),starWars,I),
   agent(S),
   agent(R),
   placename(U),
   agent(T),
   placename(V),
   inst(starWars), instant(I).
%
% Translation of intHerosJourney(R,S,T,U,V) initiates ['perm', ['go', ['R', 'V']]] if ['and', ['and', ['phase', ['herosJourney', 'inactive']], ['role', ['R', 'hero']]], ['place', ['V', 'home']]]
%
initiated(perm(go(R,V)),starWars,I) :-
   occurred(intHerosJourney(R,S,T,U,V),starWars,I),
   holdsat(live(starWars),starWars,I), inst(starWars),
   holdsat(phase(herosJourney,inactive),starWars,I),
   holdsat(role(R,hero),starWars,I),
   holdsat(place(V,home),starWars,I),
   agent(S),
   agent(R),
   placename(U),
   agent(T),
   placename(V),
   inst(starWars), instant(I).
%
% terminate rules
%
%
% Translation of intGo(S,U) terminates ['obl', [['go', ['R', 'T']], ['go', ['S', 'U']], ['violHeroGoAway', []]]] if ['and', ['and', ['and', ['role', ['R', 'hero']], ['place', ['T', 'away']]], ['role', ['S', 'villain']]], ['place', ['U', 'home']]]
%
terminated(obl(go(R,T),go(S,U),violHeroGoAway),starWars,I) :-
   occurred(intGo(S,U),starWars,I),
   holdsat(live(starWars),starWars,I),inst(starWars),
   holdsat(role(R,hero),starWars,I),
   holdsat(place(T,away),starWars,I),
   holdsat(role(S,villain),starWars,I),
   holdsat(place(U,home),starWars,I),
   agent(S),
   agent(R),
   placename(U),
   placename(T),
   inst(starWars), instant(I).
%
% Translation of intHerosJourney(R,S,T,U,V) terminates ['phase', ['herosJourney', 'done']] if ['phase', ['herosJourney', 'done']]
%
terminated(phase(herosJourney,done),starWars,I) :-
   occurred(intHerosJourney(R,S,T,U,V),starWars,I),
   holdsat(live(starWars),starWars,I),inst(starWars),
   holdsat(phase(herosJourney,done),starWars,I),
   agent(S),
   agent(R),
   placename(U),
   agent(T),
   placename(V),
   inst(starWars), instant(I).
%
% Translation of intHerosJourney(R,S,T,U,V) terminates ['phase', ['herosJourney', 'phaseD']] if ['phase', ['herosJourney', 'phaseD']]
%
terminated(phase(herosJourney,phaseD),starWars,I) :-
   occurred(intHerosJourney(R,S,T,U,V),starWars,I),
   holdsat(live(starWars),starWars,I),inst(starWars),
   holdsat(phase(herosJourney,phaseD),starWars,I),
   agent(S),
   agent(R),
   placename(U),
   agent(T),
   placename(V),
   inst(starWars), instant(I).
%
% Translation of intHerosJourney(R,S,T,U,V) terminates ['perm', ['go', ['R', 'V']]] if ['phase', ['herosJourney', 'phaseD']]
%
terminated(perm(go(R,V)),starWars,I) :-
   occurred(intHerosJourney(R,S,T,U,V),starWars,I),
   holdsat(live(starWars),starWars,I),inst(starWars),
   holdsat(phase(herosJourney,phaseD),starWars,I),
   agent(S),
   agent(R),
   placename(U),
   agent(T),
   placename(V),
   inst(starWars), instant(I).
%
% Translation of intHerosJourney(R,S,T,U,V) terminates ['phase', ['herosJourney', 'phaseC']] if ['phase', ['herosJourney', 'phaseC']]
%
terminated(phase(herosJourney,phaseC),starWars,I) :-
   occurred(intHerosJourney(R,S,T,U,V),starWars,I),
   holdsat(live(starWars),starWars,I),inst(starWars),
   holdsat(phase(herosJourney,phaseC),starWars,I),
   agent(S),
   agent(R),
   placename(U),
   agent(T),
   placename(V),
   inst(starWars), instant(I).
%
% Translation of intHerosJourney(R,S,T,U,V) terminates ['perm', ['meet', ['R', 'T']]] if ['phase', ['herosJourney', 'phaseC']]
%
terminated(perm(meet(R,T)),starWars,I) :-
   occurred(intHerosJourney(R,S,T,U,V),starWars,I),
   holdsat(live(starWars),starWars,I),inst(starWars),
   holdsat(phase(herosJourney,phaseC),starWars,I),
   agent(S),
   agent(R),
   placename(U),
   agent(T),
   placename(V),
   inst(starWars), instant(I).
%
% Translation of intHerosJourney(R,S,T,U,V) terminates ['phase', ['herosJourney', 'phaseB']] if ['phase', ['herosJourney', 'phaseB']]
%
terminated(phase(herosJourney,phaseB),starWars,I) :-
   occurred(intHerosJourney(R,S,T,U,V),starWars,I),
   holdsat(live(starWars),starWars,I),inst(starWars),
   holdsat(phase(herosJourney,phaseB),starWars,I),
   agent(S),
   agent(R),
   placename(U),
   agent(T),
   placename(V),
   inst(starWars), instant(I).
%
% Translation of intHerosJourney(R,S,T,U,V) terminates ['obl', [['go', ['R', 'U']], ['go', ['S', 'V']], ['violHeroGoAway', []]]] if ['phase', ['herosJourney', 'phaseB']]
%
terminated(obl(go(R,U),go(S,V),violHeroGoAway),starWars,I) :-
   occurred(intHerosJourney(R,S,T,U,V),starWars,I),
   holdsat(live(starWars),starWars,I),inst(starWars),
   holdsat(phase(herosJourney,phaseB),starWars,I),
   agent(S),
   agent(R),
   placename(U),
   agent(T),
   placename(V),
   inst(starWars), instant(I).
%
% Translation of intHerosJourney(R,S,T,U,V) terminates ['phase', ['herosJourney', 'phaseA']] if ['phase', ['herosJourney', 'phaseA']]
%
terminated(phase(herosJourney,phaseA),starWars,I) :-
   occurred(intHerosJourney(R,S,T,U,V),starWars,I),
   holdsat(live(starWars),starWars,I),inst(starWars),
   holdsat(phase(herosJourney,phaseA),starWars,I),
   agent(S),
   agent(R),
   placename(U),
   agent(T),
   placename(V),
   inst(starWars), instant(I).
%
% Translation of intHerosJourney(R,S,T,U,V) terminates ['perm', ['go', ['R', 'V']]] if ['phase', ['herosJourney', 'phaseA']]
%
terminated(perm(go(R,V)),starWars,I) :-
   occurred(intHerosJourney(R,S,T,U,V),starWars,I),
   holdsat(live(starWars),starWars,I),inst(starWars),
   holdsat(phase(herosJourney,phaseA),starWars,I),
   agent(S),
   agent(R),
   placename(U),
   agent(T),
   placename(V),
   inst(starWars), instant(I).
%
% Translation of intHerosJourney(R,S,T,U,V) terminates ['phase', ['herosJourney', 'inactive']] if ['phase', ['herosJourney', 'inactive']]
%
terminated(phase(herosJourney,inactive),starWars,I) :-
   occurred(intHerosJourney(R,S,T,U,V),starWars,I),
   holdsat(live(starWars),starWars,I),inst(starWars),
   holdsat(phase(herosJourney,inactive),starWars,I),
   agent(S),
   agent(R),
   placename(U),
   agent(T),
   placename(V),
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
% initially: pow(starWars,intHerosJourney(R,S,T,U,V))
% condition: ['and', ['and', ['and', ['!=', ['R', 'S']], ['!=', ['S', 'T']]], ['!=', ['T', 'U']]], ['!=', ['U', 'V']]]
holdsat(pow(starWars,intHerosJourney(R,S,T,U,V)),starWars,I) :-
   agent(S),
   agent(R),
   placename(U),
   agent(T),
   placename(V),
   R!=S,
   S!=T,
   T!=U,
   U!=V,
   inst(starWars), start(I).
% initially: pow(starWars,intGo(S,U))
holdsat(pow(starWars,intGo(S,U)),starWars,I) :-
   agent(S),
   placename(U),
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
% initially: role(darthVader,villain)
holdsat(role(darthVader,villain),starWars,I) :-
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
