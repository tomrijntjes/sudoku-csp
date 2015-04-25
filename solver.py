import time

class Solver:
	def __init__(self):
		self.example = '4.....8.5.3..........7......2.....6.....8.4......1.......6.3.7.5..2.....1.4......'
			#every square can take only one value


	def parse_grid(self,grid):
		chars = [c for c in grid if c.isdigit() or c in "0."]
		assert len(chars) == 9 ** 2
		matrix = list(self.chunk(chars))
		return matrix

	def chunk(self,charlist):
		for i in range(0,81,9):
			yield charlist[i:i+9]

	def display(self,matrix):
		chars = [""]
		for r in range(0, 9):
			for c in range(0, 9):
				if c in (3, 6):
					chars.append("|")
				chars.append(matrix[r][c])
			if r != 8:
				chars.append("\n")
				if r in (2, 5):
					chars.append("------+-------+------\n")
		print(" ".join(chars))

	def timeit(f):
		def timed(*args, **kw):
			ts = time.clock()
			result = f(*args, **kw)
			te = time.clock()
			#print("Solved one sudoku in {0} seconds".format(te-ts))
			return result,te-ts
		return timed
