nullevent :- observed(null, I, T).
:- nullevent.
deadEvent :- observed(noDeadline(X), I, T).
:- deadEvent.
violEvent :- occurred(viol(X), I, T).
:- violEvent.
subleaseEvent :- occurred(sublease(X, Y, Z), I, T), holdsat(role(X, lessee), I, T).
:- subleaseEvent.
