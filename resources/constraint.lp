#show occurred/3.
#show pow/2.
nullevent :- observed(null, I, T).
:- nullevent.
deadEvent :- observed(noDeadline(X), I, T).
:- deadEvent.
violEvent :- occurred(viol(X), I, T).
:- violEvent.
