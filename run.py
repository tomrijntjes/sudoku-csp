from solver_v2 import Solver

s = Solver()

#s.display(s.parse_grid(s.example))

constraints = s.construct_constraints()
variables = s.parse_grid(s.example)
propagates_variables = s.propagate(constraints, variables)
#propagates_variablesOLD = list(propagates_variables)

propagates_OLDvariables = []
for element in variables:
    propagates_OLDvariables.append(list(element))
    
#OLDvariables = list(variables)

'''
print id(OLDvariables[0])
print id(variables[0])
'''
'''
print propagates_variables
print propagates_variablesOLD
propagates_variables.remove(propagates_variables[0])
print propagates_variables
print propagates_variablesOLD
'''

#s.solve(constraints, variables, OLDvariables)
s.solve(constraints, propagates_variables, propagates_OLDvariables)
