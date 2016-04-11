import gringo
import sys

terms = []

def print_model(m):
    print "  positive:", ", ".join(map(str, m.atoms(gringo.Model.ATOMS)))

def on_model(m):
    global terms
#    print "atoms"
#    print "  positive:", ", ".join(map(str, m.atoms(gringo.Model.ATOMS)))
    for atom in m.atoms(gringo.Model.ATOMS):
        terms.extend([(atom.name(),atom.args())])
def on_finish(res, canceled):
    print res, canceled

prg1 = gringo.Control()
prg2 = gringo.Control()
# ctl.load("program.lp")
prg1.add("b", ["t"], "a(t).")
prg1.ground([("b", [2])])
prg2.add("a", ["t"], "b(t).")
prg2.ground([("a", [3])])
prg2.ground([("a", [4])])
prg2.solve(on_model=on_model)
# prg1.solve(on_model=on_model)
# prg2.solve(on_model=lambda m: x = m.atoms(Model.ATOMS))
#    x.wait()
#    x = prg.solve_async(on_model,on_finish)
#    x.wait()
# prg.ground([("base", [])])
# ctl.solve(on_model=lambda m: sys.stdout.write(str(m) + "\n"))
print(terms)
prg1.ground(terms)
prg1.solve(on_model=print_model)


