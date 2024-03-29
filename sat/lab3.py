"""
6.1010 Spring '23 Lab 8: SAT Solver
"""

#!/usr/bin/env python3

import sys
import typing
import doctest

sys.setrecursionlimit(10_000)
# NO ADDITIONAL IMPORTS

def satisfying_assignment(formula):
    """
    Find a satisfying assignment for a given CNF formula.
    Returns that assignment if one exists, or None otherwise.

    >>> satisfying_assignment([])
    {}
    >>> x = satisfying_assignment([[('a', True), ('b', False), ('c', True)]])
    >>> x.get('a', None) is True or x.get('b', None) is False or x.get('c', None) is True
    True
    >>> satisfying_assignment([[('a', True)], [('a', False)]])
    """
    assignments = dict() #sets assignments to an empty dictionary
    assignments, formula = unit_clause(formula) #utilizes helper function to simplify unit clauses in formula down 
    print(unit_clause(formula))

    if formula is None: 
        return None

    if len(formula)== 0: #if successfully satisified
        return assignments #returns empty dictionary 

    if [] in formula: #if empty clause (no solution)
        return None
    
    else: 
        var = formula[0][0][0] #sets variable to be the first index in the literal 
        for value in [True, False]: #iterates through True, then False if True doesn't work 
            new_formula = update_expressions(formula, var, value) #utiilizes helper function to get a new formula 
            result = satisfying_assignment(new_formula) #recurses through the new formula to get the result 
            if result is None: 
                continue
            else: 
                return {var: value} | assignments | result #returns a dictionary with the variable bound to a boolean assignment
                
    return None


        


def update_expressions(formula, x, bool): 
    """Helper function that updates the expression to simplify the formula
    Passes in parameters: formula, x (a variable that is a string), and bool (a Boolean)"""
    updated_formula = [] #sets the updated formula to be an empty list 
    for clause in formula: #for every clause in the formula 
        if (x, bool) in clause: #if the object and the bool are a literal in the clause
            continue 
        new_clause = [] #create a new clause that is an empty list 
        for literal in clause: #for every literal in the clause (every tuple in the list)
            if (x, not bool) == literal: #if the object and it's opposite is equal to the literal
                continue 
            new_clause.append(literal) #otherwise, append the literal to the new clause
        updated_formula.append(new_clause) #otherwise, append the new clause to the new formula
    return updated_formula
    #check for what it returns when 
    #successfully solved the formula -> [] *empty formula
    #no solution -> [[]] #empty clause
    #smaller formula 


def unit_clause(formula): 
    """Helper function that simplifies all the unit clauses in a given formula
    Parameters: formula """
    unit_clause = {} #sets a empty dictionary
    while True: #sets it to be True so that it always enters the loop at least once 
        check_unit = False #sets unit clause to be False
        for clause in formula: #for every in the formula
            if len(clause) == 1: #if it's a unit clause
                print(clause)
                check_unit = True #set the check to be True
                formula = update_expressions(formula, clause[0][0], clause[0][1]) #update the formula with the unit clause
                unit_clause[clause[0][0]] = clause[0][1] #add this to the dictionary that was created
                break #break the loop 
        if check_unit == False: #otherwise, set check_unit to be false and break the loop since there are no unit clauses 
            break
    return unit_clause, formula #return both the unit clause dictionary and the formula


if __name__ == "__main__":
    # _doctest_flags = doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS
    # doctest.testmod(optionflags=_doctest_flags)

    formula = [[('a', True), ('a', False)], [('b', True), ('a', True)], [('b', True)], [('b', False), ('b', False), ('a', False)], [('c', True), ('d', True)], [('c', True), ('d', True)]]
    print(update_expressions((formula),'a', True))
    print(satisfying_assignment(formula))