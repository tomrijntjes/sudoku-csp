from pyeda.inter import *
import time

class Solver:
	def __init__(self):
		"""Sudoku SAT solver. Example usage: s = Solver()
		s.display(s.solve(s.example))
		"""
		self.constraints = 11988
		self.X = exprvars('x', (1, 10), (1, 10), (1, 10))
		self.DIGITS = "123456789"
		self.example = ( ".73|...|8.."
		  "..4|13.|.5."
		  ".85|..6|31."
		 "---+---+---"
		  "5..|.9.|.3."
		  "..8|.1.|5.."
		  ".1.|.6.|..7"
		  "---+---+---"
		  ".51|6..|28."
		  ".4.|.52|9.."
		  "..2|...|64." )
		self.example2 = '4.....8.5.3..........7......2.....6.....8.4......1.......6.3.7.5..2.....1.4......'
			#every square can take only one value
		V = And(*[
			    And(*[
				OneHot(*[ self.X[r, c, v]
				    for v in range(1, 10) ])
				for c in range(1, 10) ])
			    for r in range(1, 10) ])
			#every square in each row is unique
		R = And(*[
			    And(*[
				OneHot(*[ self.X[r, c, v]
				    for c in range(1, 10) ])
				for v in range(1, 10) ])
			    for r in range(1, 10) ])
			#every square in each column is unique
		C = And(*[
			    And(*[
				OneHot(*[ self.X[r, c, v]
				    for r in range(1, 10) ])
				for v in range(1, 10) ])
			    for c in range(1, 10) ])
			#every square in a box is unique
		B = And(*[
		    And(*[
			OneHot(*[ self.X[3*br+r, 3*bc+c, v]
			    for r in range(1, 4) for c in range(1, 4) ])
			for v in range(1, 10) ])
		    for br in range(3) for bc in range(3) ])
		self.S = And(V, R, C, B)
		self.solve(self.example)


	def parse_grid(self,grid):
		chars = [c for c in grid if c.isdigit() or c in "0."]
		assert len(chars) == 9 ** 2
		return And(*[ self.X[i // 9 + 1, i % 9 + 1, int(c)] for i, c in enumerate(chars) if c.isdigit() ])

	def get_val(self,point, r, c):
		for v in range(1, 10):
			if point[self.X[r, c, v]]:
				return self.DIGITS[v-1]
		return "X"

	def display(self,point):
		chars = list()
		for r in range(1, 10):
			for c in range(1, 10):
				if c in (4, 7):
					chars.append("|")
				chars.append(self.get_val(point, r, c))
			if r != 9:
				chars.append("\n")
				if r in (3, 6):
					chars.append("---+---+---\n")
		print("".join(chars))

	def timeit(f):
		def timed(*args, **kw):
			ts = time.clock()
			result = f(*args, **kw)
			te = time.clock()
			#print("Solved one sudoku in {0} seconds".format(te-ts))
			return result,te-ts
		return timed


	@timeit
	def solve(self,grid):
		with self.parse_grid(grid):
			return self.S.satisfy_one()

class DiagonalSolver(Solver):
	def __init__(self):
		self.X = exprvars('x', (1, 10), (1, 10), (1, 10))
		self.DIGITS = "123456789"
		self.example = ( ".73|...|8.."
		  "..4|13.|.5."
		  ".85|..6|31."
		 "---+---+---"
		  "5..|.9.|.3."
		  "..8|.1.|5.."
		  ".1.|.6.|..7"
		  "---+---+---"
		  ".51|6..|28."
		  ".4.|.52|9.."
		  "..2|...|64." )
		#every square can take only one value
		V = And(*[
			And(*[
			OneHot(*[ self.X[r, c, v]
				for v in range(1, 10) ])
			for c in range(1, 10) ])
			for r in range(1, 10) ])
		#every square in each row is unique
		R = And(*[
			And(*[
			OneHot(*[ self.X[r, c, v]
				for c in range(1, 10) ])
			for v in range(1, 10) ])
			for r in range(1, 10) ])
		#every square in each column is unique
		C = And(*[
			And(*[
			OneHot(*[ self.X[r, c, v]
				for r in range(1, 10) ])
			for v in range(1, 10) ])
			for c in range(1, 10) ])
		#every square in a box is unique
		B = And(*[
		And(*[
		OneHot(*[ self.X[3*br+r, 3*bc+c, v]
			for r in range(1, 4) for c in range(1, 4) ])
		for v in range(1, 10) ])
		for br in range(3) for bc in range(3) ])
		#every square in diagonal topleft-bottomright is unique
		D1 = And(*[
		OneHot(*[ self.X[c, c, v]
			for c in range(1, 10) ])
		for v in range(1, 10) ])
		#every square in diagonal topright-bottomleft is unique
		D2 = And(*[
				OneHot(*[ self.X[10-c, c, v]
					for c in range(1, 10) ])
				for v in range(1, 10) ])
		self.S = And(V, R, C, B,D1,D2)
		self.solve(self.example)
