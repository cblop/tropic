#show occurred/3.
validEvent(I, In) :- instant(I), inst(In), event(E), occurred(E, In, I), not occurred(viol(_), In, I), E != null.
validEvent(I) :- validEvent(I, In), inst(In).
:- validEvent(I2), not validEvent(I), I < I2, instant(I), instant(I2).
:- instant(I), not validEvent(I), occurred(viol(_), In, I).
deadEvent :- observed(noDeadline(X), I, T).
:- deadEvent.
nullInst :- occurred(X, null, T).
:- nullInst.
