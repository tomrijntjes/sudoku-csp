from norvig import Solver
import cProfile
import numpy
import sys



def main(s,files):
    for file in files:
        with open(file) as f:
            times,results = s.solve_all([x for x in f.read().strip().split('\n') if len(x)>1])
            print("Mean runtime: {0}".format(numpy.mean(times)))
            print("Standard Deviation: {0}".format(numpy.std(times)))

if __name__ == '__main__':
    files = sys.argv[1:]
    if len(files)<1:
        files = ['sudoku_training.txt']
    print(files)
    profile = cProfile.Profile()
    solvers = dict()
    solvers['randrand'] = Solver('Random',None)
    solvers['randleastconstr'] = Solver('Random','Least Constraining Value')
    solvers['randmostconstr'] = Solver('Random','Most Constraining Value')
    solvers['minremainrand'] = Solver('Minimum Remaining Values',None)
    solvers['minremainleastconstr'] = Solver('Minimum Remaining Values','Least Constraining Value')
    solvers['minremainmostconstr'] = Solver('Minimum Remaining Values','Most Constraining Value')
    for name,solver in solvers.iteritems():
        print 'Running solver {0}...'.format(name)
        profile.runcall(main,solver,files)
        profile.dump_stats('profiles/'+name+".profile")
