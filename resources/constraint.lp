#show occurred/3.
nullevent :- observed(null, I, T), observed(E, I, T2), T2 > T, event(E), E != null.
:- nullevent.
deadEvent :- observed(noDeadline(X), I, T).
:- deadEvent.
violEvent :- occurred(viol(X), I, T).
:- violEvent.
