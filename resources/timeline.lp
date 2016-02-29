start(0).
instant(0..T) :- final(T).
next(T,T+1) :- instant(T).
final(6).