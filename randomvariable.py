from norvig import Solver
from random import choice

class RandomVariable(Solver):
      def search(self,values):
          "Using depth-first search and propagation, try all possible values."
          if values is False:
              return False ## Failed earlier
          if all(len(values[s]) == 1 for s in self.squares):
              return values ## Solved!
          ## Randomly pick a square
          n,s = choice([((values[s]), s) for s in self.squares if len(values[s]) > 1])
          return self.some(self.search(self.assign(values.copy(), s, d))
                      for d in values[s])
