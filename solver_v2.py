import time

class Solver:
	def __init__(self):
		self.example = '4.....8.5.3..........7......2.....6.....8.4......1.......6.3.7.5..2.....1.4......'
		self.display(self.example)
		#self.example = '81.2.3.6.29715.3483568......8.621.7474938.126162.7983.638514792921768............'
			#every square can take only one value
			
	def parse_grid(self,grid):
		variables = []
		for c in grid:
			if c.isdigit():
				variables.append([int(c)])
			else:
				variables.append([i for i in range(1,10)])
			
		assert len(variables) == 9 ** 2
		return variables
	
	def construct_constraints(self):
		constraints = []
		
		#rows
		count = 1
		for i in range(1,10):
			sublist = []
			for j in range(1,10):
				sublist.append(count -1)
				count +=1
			constraints.append(sublist)
			
		#columns
		for i in range(1,10):
			count = i
			sublist = []
			for j in range(0,9):
				sublist.append((count + 9 * j) -1)
			constraints.append(sublist)
		return constraints
	
	def check_constraints(self, constraints, variables):
		for element in constraints:
			for value1 in element:
				for value2 in element:
					if variables[value1] != 0 and variables[value2] !=0 and (variables[value1] == variables[value2]) and value1 != value2:
						#return false if constraint is violated
						return False
		
		return True
	
	
	def solve(self, constraints, variables, OLDvariables):
		
		solution = [0] * 81
		depth = 0
		k = 0
		
		
		
		while depth < 81:
			
			while variables[depth] == []:
				
				if depth < 10:
					print depth
				variables[depth] = list(OLDvariables[depth])
				
				solution[depth] = 0
				variables[depth -1] = variables[depth-1][1:]
				#variables[depth -1].remove(variables[depth -1][0])
				depth -=1
				
			
			solution[depth] = variables[depth][0]
			if self.check_constraints(constraints, solution):
				depth +=1
			else:
				variables[depth].remove(variables[depth][0])
			#print solution
		
		self.display(solution)
		
		return solution
		
		
	
	
	def propagate(self, constraints, variables):
		key = 0
		for values in variables:
			if len(values) == 1:
				for constraint in constraints:
					if key in constraint:
						for variable in constraint:
							if values[0] in variables[variable] and values != variables[variable]:
								#print 'removing ' + str(values[0]) + "from " + str(variables[variable] )
								variables[variable].remove(values[0])
			key +=1
		return variables	

	def chunk(self,charlist):
		for i in range(0,81,9):
			yield charlist[i:i+9]

	def print_sudoku(self, sudoku):
		return
		
	def display(self,matrix):
		line = ""
		for c in range(1, 82):
			line += str(matrix[c -1])
			if c % 3 == 0:
				line += "|"
			if c % 9 == 0:
				print line
				line = " "
				print "\n"

	def timeit(f):
		def timed(*args, **kw):
			ts = time.clock()
			result = f(*args, **kw)
			te = time.clock()
			#print("Solved one sudoku in {0} seconds".format(te-ts))
			return result,te-ts
		return timed
