"""
instal

InstAL (Institutional Action Language) is a suite of tools for evaluating and simulating electronic institutions.

Institutions in InstAL are compiled to an Answer Set Programming (ASP) problem, which is then solved using clingo.

instalsolve is an interface allowing single-shot solving of institutions based on providing exogenous events that occur.
instalquery is an interface allowing multi-shot solving, which generates all possible traces within constraints.

To get started:
- Read ../README.md
- Try the examples in ../examples
- Read the InstAL papers (see below)
- Look at the InstAL website (http://www.cs.bath.ac.uk/instal/)

See papers:
Padget, J., Elakehal, E., Li, T. and De Vos, M., 2016. InstAL: An Institutional Action Language. In: Social Coordination Frameworks for Social Technical Systems.Vol. 30. Springer Verlag, p. 101. (Law, Governance and Technology Series)
Cliffe, O., De Vos, M. and Padget, J., 2006. Specifying and analysing agent-based social institutions using answer set programming. In: Coordination, Organizations, Institutions, and Norms in Multi-Agent Systems. Vol. 3913. , pp. 99-113. (Lecture Notes in Artificial Intelligence)
Cliffe, O., 2007. Specifying and analysing institutions in multi-agent systems using answer set programming. PhD thesis. Department of Computer Science, University of Bath. (Computer Science Technical Reports; CSBU-2007-04).
"""