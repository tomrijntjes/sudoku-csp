from norvig import Solver
from collections import Counter,OrderedDict
from itertools import chain

class ValueFirst(Solver):
      def search(self,values):
          "Using depth-first search and propagation, try all possible values."
          if values is False:
              return False ## Failed earlier
          if all(len(values[s]) == 1 for s in self.squares):
              return values ## Solved!
          ## Chose the unfilled square s with the fewest possibilities
          n,s = min((len(values[s]), s) for s in self.squares if len(values[s]) > 1)
          return self.some(self.search(self.assign(values.copy(), s, d))
                      for d in self.sortValues(values[s],values))

      def sortValues(self,domain,values):
          "sort values based on frequency in given values"
          if len(domain)==1:
              return domain
          givens = (values[s] for s in self.squares if len(values[s]) == 1)
          filtered = filter(lambda v: v in domain, givens)
          "sometimes members of the domain never occur in the solved squares ie. in filtered"
          "a bit of a hack: we add the domain to the search space once"
          space = chain(filtered,(char for char in domain))
          return list(x[0] for x in (Counter(space).most_common()))
