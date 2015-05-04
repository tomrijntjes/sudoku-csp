from norvig import Solver
import cProfile

def main():
    s = Solver()
    with open('sudoku_training.txt') as f:
        s.solve_all([x for x in f.read().strip().split('\n') if len(x)>1])

if __name__ == '__main__':
    profile = cProfile.Profile()
    profile.runcall(main)
    profile.dump_stats("testrun.profile")
