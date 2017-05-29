#show occurred/3.
nullevent :- observed(null, I, T), observed(E, I, T2), T2 > T, event(E), E != null.
:- nullevent.
%% nullevent :- occurred(null, I, T).
%% :- nullevent.
deadEvent :- observed(noDeadline(X), I, T).
:- deadEvent.
hasViol(I, T) :- occurred(viol(E), I, T), instant(T), not final(T), inst(I).
%% hasViol :- occurred(viol(E), I, T), instant(T), inst(I).
%% :- hasViol.
instNoViol(T) :- not hasViol(I, T), inst(I), instant(T).
:- not instNoViol(T), instant(T).
nullInst :- occurred(X, null, T).
:- nullInst.
