from typing import Any, Dict, List, Optional
from CSP import Assignment, BinaryConstraint, Problem, UnaryConstraint
from helpers.utils import NotImplemented

# This function applies 1-Consistency to the problem.
# In other words, it modifies the domains to only include values that satisfy their variables' unary constraints.
# Then all unary constraints are removed from the problem (they are no longer needed).
# The function returns False if any domain becomes empty. Otherwise, it returns True.
def one_consistency(problem: Problem) -> bool:
    remaining_constraints = []
    solvable = True
    for constraint in problem.constraints:
        if not isinstance(constraint, UnaryConstraint):
            remaining_constraints.append(constraint)
            continue
        variable = constraint.variable
        new_domain = {value for value in problem.domains[variable] if constraint.condition(value)}
        if not new_domain:
            solvable = False
        problem.domains[variable] = new_domain
    problem.constraints = remaining_constraints
    return solvable

# This function returns the variable that should be picked based on the MRV heuristic.
# NOTE: We don't use the domains inside the problem, we use the ones given by the "domains" argument 
#       since they contain the current domains of unassigned variables only.
# NOTE: If multiple variables have the same priority given the MRV heuristic, 
#       we order them in the same order in which they appear in "problem.variables".
def minimum_remaining_values(problem: Problem, domains: Dict[str, set]) -> str:
    _, _, variable = min((len(domains[variable]), index, variable) for index, variable in enumerate(problem.variables) if variable in domains)
    return variable

# This function should implement forward checking
# The function is given the problem, the variable that has been assigned and its assigned value and the domains of the unassigned values
# The function should return False if it is impossible to solve the problem after the given assignment, and True otherwise.
# In general, the function should do the following:
#   - For each binary constraints that involve the assigned variable:
#       - Get the other involved variable.
#       - If the other variable has no domain (in other words, it is already assigned), skip this constraint.
#       - Update the other variable's domain to only include the values that satisfy the binary constraint with the assigned variable.
#   - If any variable's domain becomes empty, return False. Otherwise, return True.
# IMPORTANT: Don't use the domains inside the problem, use and modify the ones given by the "domains" argument 
#            since they contain the current domains of unassigned variables only.
def forward_checking(problem: Problem, assigned_variable: str, assigned_value: Any, domains: Dict[str, set]) -> bool:
    #TODO: Write this function

    for constraint in problem.constraints: 
        if isinstance(constraint , BinaryConstraint): 
            if assigned_variable in constraint.variables:
                other_variable = constraint.get_other(assigned_variable) 
                if domains.get(other_variable) is not None:
                    new_domain = {value for value in domains[other_variable] if constraint.condition(assigned_value, value)} 
                    if len(new_domain)== 0:
                        return False  
                    domains[other_variable] = new_domain
    # domains.pop(assigned_variable)
    # problem.domains = domains
    return True

    #NotImplemented()

# This function should return the domain of the given variable order based on the "least restraining value" heuristic.
# IMPORTANT: This function should not modify any of the given arguments.
# Generally, this function is very similar to the forward checking function, but it differs as follows:
#   - You are not given a value for the given variable, since you should do the process for every value in the variable's
#     domain to see how much it will restrain the neigbors domain
#   - Here, you do not modify the given domains. But you can create and modify a copy.
# IMPORTANT: If multiple values have the same priority given the "least restraining value" heuristic, 
#            order them in ascending order (from the lowest to the highest value).
# IMPORTANT: Don't use the domains inside the problem, use and modify the ones given by the "domains" argument 
#            since they contain the current domains of unassigned variables only.
def least_restraining_values(problem: Problem, variable_to_assign: str, domains: Dict[str, set]) -> List[Any]:
    #TODO: Write this function
    values = {} 
    for value in domains[variable_to_assign]:
        domain2 = domains.copy()
        valuescount =0 
        if forward_checking(problem, variable_to_assign, value, domain2):
            for constraint in problem.constraints:
                if isinstance(constraint , BinaryConstraint):
                    if variable_to_assign in constraint.variables:
                        other_variable = constraint.get_other(variable_to_assign)
                        if domain2.get(other_variable) is not None:
                            valuescount += len(domain2[other_variable])

        values[value] = valuescount            
    
    # print(values)
    test = sorted(values.items(), key=lambda x: x[1] , reverse=True)
    # print(test) 
    returned = [value for value,count in test]
    # print(returned)
    return returned

# This function should solve CSP problems using backtracking search with forward checking.
# The variable ordering should be decided by the MRV heuristic.
# The value ordering should be decided by the "least restraining value" heurisitc.
# Unary constraints should be handled using 1-Consistency before starting the backtracking search.
# This function should return the first solution it finds (a complete assignment that satisfies the problem constraints).
# If no solution was found, it should return None.
# IMPORTANT: To get the correct result for the explored nodes, you should check if the assignment is complete only once using "problem.is_complete"
#            for every assignment including the initial empty assignment, EXCEPT for the assignments pruned by the forward checking.
#            Also, if 1-Consistency deems the whole problem unsolvable, you shouldn't call "problem.is_complete" at all.
def solve(problem: Problem) -> Optional[Assignment]:
    if not one_consistency(problem):
        return None
    # for constraint in problem.constraints:
    #     print(constraint)

    # for var in problem.variables:
    #     print(var , problem.domains[var])   
    return backtracking_search({} , problem) 
    

def is_assignment_consistent(assignment: Assignment, problem: Problem) -> bool:
    for constraint in problem.constraints:
        if isinstance(constraint, BinaryConstraint):
            variable1, variable2 = constraint.variables
            if variable1 in assignment and variable2 in assignment:
                if not constraint.is_satisfied(assignment):
                    return False
    return True


def backtracking_search(assignments : Assignment , problem : Problem) -> Optional[Assignment]:
    # print(assignments)
    if problem.is_complete(assignments):
        return assignments 
    variable_selected = minimum_remaining_values(problem, problem.domains)  
    # print("selceted variable :", variable_selected)
    LRV =least_restraining_values(problem , variable_selected , problem.domains)
    # print("selceted values :", LRV)
    for value in LRV: 
        # check if value is consistent with assignment 
        # print("selceted value :", value)

        # new_assignments =  assignments.copy() 
        # new_assignments[variable_selected] = value
        # print("old :", assignments)
        # print("new assignment :", new_assignments)  
        # print("problem assignment satisfaction : " , problem.satisfies_constraints(new_assignments) ) 
        prev_assignments = assignments.copy()
        new_assignments =  assignments.copy()
        new_assignments[variable_selected] = value
        if is_assignment_consistent(assignments , problem): # assignment is consistend 
            # print("")
            # forward checking [inference ] 
            # new_domain = problem.domains.copy()  
            # print(forward_checking(problem, variable_selected, value, new_domain))
            previous_domain = problem.domains.copy()
            new_domain = problem.domains.copy() 
            if forward_checking(problem, variable_selected, value, new_domain):
                assignments[variable_selected] = value
                problem.domains = new_domain
                temp_var = problem.domains[variable_selected]
                if variable_selected in problem.domains:
                    problem.domains.pop(variable_selected)
                # print("new domains :" , problem.domains)
                # print(problem.domains[variable_selected])
                result = backtracking_search(assignments , problem)
                if result is not None:
                    return result 
                
                problem.domains=previous_domain
                assignments = prev_assignments 
        else : 
            assignments.pop(variable_selected)            

    return None
#NotImplemented()
    