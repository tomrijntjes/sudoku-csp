import time

class Solver:
	def __init__(self):
		self.example = '4.....8.5.3..........7......2.....6.....8.4......1.......6.3.7.5..2.....1.4......'
			#every square can take only one value


	def create_constraints(self):

		#rows
		constraints = []
		var = 1;
		for i in range(0,9):
			sublist = []
			for j in range(0,9):
				sublist.append(var)
				var +=1
			constraints.append(sublist)

		print(constraints)
		#columns

	def parse_grid(self,grid):
		chars = list()
		for c in grid:
			if c.isdigit():
				chars.append([int(c)])
			if c == ".":
				chars.append([x for x in range(1,10)])
		assert len(chars) == 9 ** 2
		return chars

		matrix = list(self.chunk(chars))
		return matrix

	def constraints(self):
		pass

	def check_constraints(self):
		for sublist in self.constraints:

			for variable in sublist:
					for variable2 in sublist:
						if chars(variable) == chars(variable2):
							return false


			return OneHot()

		return violation

	def OneHot(self):
		return len(set(a)) == len(a)




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
