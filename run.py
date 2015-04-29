from solver_v2 import Solver

s = Solver()

#s.display(s.parse_grid(s.example))

constraints = s.construct_constraints()
variables = s.parse_grid(s.example)
propagates_variables = s.propagate(constraints, variables)
propagates_variablesOLD = s.propagate(constraints, variables)

s.solve(constraints, propagates_variables, propagates_variablesOLD)
