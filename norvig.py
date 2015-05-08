## Solve Every Sudoku Puzzle

## See http://norvig.com/sudoku.html

## Throughout this program we have:
##   r is a row,    e.g. 'A'
##   c is a column, e.g. '3'
##   s is a square, e.g. 'A3'
##   d is a digit,  e.g. '9'
##   u is a unit,   e.g. ['A1','B1','C1','D1','E1','F1','G1','H1','I1']
##   grid is a grid,e.g. 81 non-blank chars, e.g. starting with '.18...7...
##   values is a dict of possible values, e.g. {'A1':'12349', 'A2':'8', ...}

import time, random
from collections import Counter,OrderedDict
import itertools

class Solver():
  def __init__(self,variableHeuristic='Minimum remaining values',valueHeuristic=None):
    self.variableHeuristic = variableHeuristic
    self.valueHeuristic = valueHeuristic
    self.digits   = '123456789'
    self.rows     = 'ABCDEFGHI'
    self.cols     = self.digits
    self.squares  = self.cross(self.rows, self.cols)
    self.unitlist = ([self.cross(self.rows, c) for c in self.cols] +
    [self.cross(r, self.cols) for r in self.rows] +
    [self.cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')])
    self.units = dict((s, [u for u in self.unitlist if s in u])
    for s in self.squares)
    self.peers = dict((s, set(sum(self.units[s],[]))-set([s]))
    for s in self.squares)



  def cross(self,A, B):
      "Cross product of elements in A and elements in B."
      return [a+b for a in A for b in B]

  ################ Parse a Grid ################

  def parse_grid(self,grid):
      """Convert grid to a dict of possible values, {square: digits}, or
      return False if a contradiction is detected."""
      ## To start, every square can be any digit; then assign values from the grid.
      values = dict((s, self.digits) for s in self.squares)
      for s,d in self.grid_values(grid).items():
          if d in self.digits and not self.assign(values, s, d):
              return False ## (Fail if we can't assign d to square s.)
      return values

  def grid_values(self,grid):
      "Convert grid into a dict of {square: char} with '0' or '.' for empties."
      chars = [c for c in grid if c in self.digits or c in '0.']
      assert len(chars) == 81
      return dict(zip(self.squares, chars))

  ################ Constraint Propagation ################

  def assign(self,values, s, d):
      """Eliminate all the other values (except d) from values[s] and propagate.
      Return values, except return False if a contradiction is detected."""
      other_values = values[s].replace(d, '')
      if all(self.eliminate(values, s, d2) for d2 in other_values):
          return values
      else:
          return False

  def eliminate(self,values, s, d):
      """Eliminate d from values[s]; propagate when values or places <= 2.
      Return values, except return False if a contradiction is detected."""
      if d not in values[s]:
          return values ## Already eliminated
      values[s] = values[s].replace(d,'')
      ## (1) If a square s is reduced to one value d2, then eliminate d2 from the peers.
      if len(values[s]) == 0:
          return False ## Contradiction: removed last value
      elif len(values[s]) == 1:
          d2 = values[s]
          if not all(self.eliminate(values, s2, d2) for s2 in self.peers[s]):
              return False
      ## (2) If a unit u is reduced to only one place for a value d, then put it there.
      for u in self.units[s]:
          dplaces = [s for s in u if d in values[s]]
          if len(dplaces) == 0:
              return False ## Contradiction: no place for this value
          elif len(dplaces) == 1:
              # d can only be in one place in unit; assign it there
              if not self.assign(values, dplaces[0], d):
                  return False
      return values

  ################ Display as 2-D grid ################

  def display(self,values):
      "Display these values as a 2-D grid."
      width = 1+max(len(values[s]) for s in self.squares)
      line = '+'.join(['-'*(width*3)]*3)
      for r in self.rows:
          print ''.join(values[r+c].center(width)+('|' if c in '36' else '')
                        for c in self.cols)
          if r in 'CF': print line
      print

  ################ Search ################

  def solve(self,grid): return self.search(self.parse_grid(grid))

  def search(self,values):
      "Using depth-first search and propagation, try all possible values."
      if values is False:
          return False ## Failed earlier
      if all(len(values[s]) == 1 for s in self.squares):
          return values ## Solved!
      ## Chose the unfilled square s with the fewest possibilities
      if self.variableHeuristic == 'Minimum Remaining Values':
          n,s = min((len(values[s]), s) for s in self.squares if len(values[s]) > 1)
      elif self.variableHeuristic == 'Random':
          n,s = random.choice([((values[s]), s) for s in self.squares if len(values[s]) > 1])
      else:
          print(self.variableHeuristic)
          raise ValueError('no supported variable heuristic selected')
      return self.some(self.search(self.assign(values.copy(), s, d))
                  for d in self.sortValues(values[s],values,s))

  def sortValues(self,domain,values,s):
      "sort values based on frequency in given values"
      if self.valueHeuristic == None:
          return domain
      if len(domain)==1:
          return domain
      peers = [values[s2] for s2 in self.peers[s]]
      flat = itertools.chain.from_iterable(peers)
      tally = list(Counter(flat).most_common())
      if self.valueHeuristic == 'Least Constraining Value':
          reverse = tally[::-1]
          return [x[0] for x in reverse if x[0] in domain]
      if self.valueHeuristic == 'Most Constraining Value':
          return [x[0] for x in tally if x[0] in domain]
      else:
          raise ValueError('no supported value heuristic selected')
   ################ Utilities

  def some(self,seq):
      "Return some element of seq that is true."
      for e in seq:
          if e: return e
      return False

  def from_file(self,filename, sep='\n'):
      "Parse a file into a list of strings, separated by sep."
      return file(filename).read().strip().split(sep)

  def shuffled(self,seq):
      "Return a randomly shuffled copy of the input sequence."
      seq = list(seq)
      random.shuffle(seq)
      return seq

  ################ System test ################



  def solve_all(self,grids, name='', showif=None):
      """Attempt to solve a sequence of grids. Report results.
      When showif is a number of seconds, display puzzles that take longer.
      When showif is None, don't display any puzzles."""
      def time_solve(grid):
          start = time.clock()
          values = self.solve(grid)
          t = time.clock()-start
          ## Display puzzles that take long enough
          if showif is not None and t > showif:
              self.display(self.grid_values(grid))
              if values: self.display(values)
              print '(%.2f seconds)\n' % t
          return (t, self.solved(values))
      times, results = zip(*[time_solve(grid) for grid in grids])
      N = len(grids)
      if N > 1:
          print "Solved %d of %d %s puzzles (avg %.4f secs (%d Hz), max %.4f secs)." % (
              sum(results), N, name, sum(times)/N, N/sum(times), max(times))
          return times,results

  def solved(self,values):
      "A puzzle is solved if each unit is a permutation of the digits 1 to 9."
      def unitsolved(unit): return set(values[s] for s in unit) == set(self.digits)
      return values is not False and all(unitsolved(unit) for unit in self.unitlist)

  def random_puzzle(self,N=17):
      """Make a random puzzle with N or more assignments. Restart on contradictions.
      Note the resulting puzzle is not guaranteed to be solvable, but empirically
      about 99.8% of them are solvable. Some have multiple solutions."""
      values = dict((s, self.digits) for s in self.squares)
      for s in self.shuffled(self.squares):
          if not self.assign(values, s, random.choice(values[s])):
              break
          ds = [values[s] for s in self.squares if len(values[s]) == 1]
          if len(ds) >= N and len(set(ds)) >= 8:
              return ''.join(values[s] if len(values[s])==1 else '.' for s in self.squares)
      return random_puzzle(N) ## Give up and make a new puzzle






## References used:
## http://www.scanraid.com/BasicStrategies.htm
## http://www.sudokudragon.com/sudokustrategy.htm
## http://www.krazydad.com/blog/2005/09/29/an-index-of-sudoku-strategies/
## http://www2.warwick.ac.uk/fac/sci/moac/currentstudents/peter_cock/python/sudoku/
