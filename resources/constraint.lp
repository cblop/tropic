#show occurred/3.
nullevent :- observed(null, I, T), observed(E, I, T2), T2 > T, event(E), E != null.
:- nullevent.
deadEvent :- observed(noDeadline(X), I, T).
:- deadEvent.
hasViol(I, T) :- occurred(viol(E), I, T), instant(T), not final(T), inst(I).
instNoViol(T) :- not hasViol(I, T), inst(I), instant(T).
:- not instNoViol(T), instant(T), not final(T).
nullInst :- occurred(X, null, T).
:- nullInst.
