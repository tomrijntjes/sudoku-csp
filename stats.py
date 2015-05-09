from norvig import Solver
from scipy.stats import ttest_rel,levene

def main(s):
    with open('sudoku_training.txt') as f:
        times,results = s.solve_all([x for x in f.read().strip().split('\n') if len(x)>1])
        return times

if __name__ == '__main__':
    control = Solver('Minimum Remaining Values',None)
    optimization = Solver('Minimum Remaining Values','Least Constraining Value')
    ctrl,optim = main(control),main(optimization)
    levenes = levene(ctrl,optim)
    print("Levene's metric is %.3f and the p-value is %.3f" % levenes)
    ttest = ttest_rel(ctrl, optim )
    print("The t-statistic is %.3f and the p-value is %.3f." % ttest)
