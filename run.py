from solver import Solver,DiagonalSolver
from scipy.stats import ttest_rel
from numpy import std,mean
import sys

d = DiagonalSolver()
s = Solver()

try:
	limit = int(sys.argv[1])
except IndexError:
	limit = 200

print("The length of the constraints formula of the normal solver is " + str(len(s.S.xs)))
print("The length of the constraints formula of the solver with added diagonal rule is " +str(len(d.S.xs)))

diagonal,normal = list(),list()
n=0
with open('diagonal.txt') as puzzles:
		print("Running tests on {0} puzzles...".format(limit))
		for puzzle in puzzles:
			if n < limit:
				diagonal.append(d.solve(puzzle)[1])
				normal.append(s.solve(puzzle)[1])
				n +=1
			else:
				break


print("...done testing {0} puzzles".format(len(normal)))
print("Normal sudoku. Mean: {0} Standard deviation: {1}".format(mean(normal),std(normal)))
print("Diagonal sudoku. Mean: {0} Standard deviation: {1}".format(mean(diagonal),std(diagonal)))
related = ttest_rel(diagonal, normal)
print("The t-statistic is %.3f and the p-value is %.3f." % related)
