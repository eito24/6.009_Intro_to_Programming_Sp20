#!/usr/bin/env python3
"""6.009 Lab 5 -- Boolean satisfiability solving"""

import sys
sys.setrecursionlimit(10000)
# NO ADDITIONAL IMPORTS

#given a 'candidate' and its assignment, removes all irrelevant from a formula
def removingx(formula,candidate,boolean):
    newformula=[]
    for rule in formula:
        #automatically ignores all rules with (candidate,boolean)
        if (candidate,not boolean) in rule:
            #adds the rule without (candidate,not boolean)
            newrule=[clause for clause in rule if clause!=(candidate,not boolean)]
            if newrule==[]:
                #reached contradiction bc it's only (candidate,not boolean)
                return None
            newformula.append(newrule)
        elif (candidate,boolean) not in rule:
            #if candidate not relevant just add whole rule
            newformula.append(rule)
    return newformula

#finds the 'unit case' in a formula
def unitcase(formula):
    for rule in formula:
        if len(rule)==1:
            return rule[0]
    return None

def satisfying_assignment(formula):
    assignment={}
    #no new assignments to make; all rules satisfied
    if formula==[]:
        return assignment
    if formula==None:
        return None
    #unitclauses
    while True:
        unit_clause=unitcase(formula)
        if unit_clause is None:
            break
        candidate=unit_clause[0]
        boolean=unit_clause[1]
        newformula=removingx(formula,candidate,boolean)
        #unit clause causes contradiction
        if newformula is None:
            return None
        assignment[candidate]=boolean
        formula=newformula

    if formula==[]:
        return assignment

    #random assignment
    candidate=formula[0][0][0]
    for value in (True,False):
        newformula=removingx(formula,candidate,value)
        if newformula is not None:
            newassignment=satisfying_assignment(newformula)
            if newassignment is not None:
                assignment[candidate]=value
                assignment.update(newassignment)
                return assignment
    #neither True nor False work
    return None  
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


#from 'Bob','basement' makes 'Bob_basement'
"""works"""
def nameplacify(name,place):
    return str(name+'_'+place)

#makes list of all keys
""""works"""
def allof(dict):
    return list(dict.keys())

#makes list of all possible groups of size n (in tuples) of given list of objects (places)
#allcombos(places,n) should result in [['basement','kitchen'],['kitchen','penthouse'],['basement','penthouse']]
"""works"""
def allcombos(places,n):
    combos=set()
    #basecase
    if n==1:
        for place in places:
            combos.add(frozenset([place]))
    else:
        current_combos=allcombos(places,n-1)
        for combo in current_combos:
            for place in places:
                if place not in combo:
                    newcombo=frozenset([place]+list(combo))
                    combos.add(newcombo)
    return combos

def boolify_scheduling_problem(student_preferences, session_capacities):
    formula=[]
    places=allof(session_capacities)
    students=allof(student_preferences)
    placepairs=allcombos(places,2)
    for student in student_preferences.keys():
        rule=[]
        #students only in desired rooms
        for place in student_preferences[student]:
            rule.append((nameplacify(student,place),True))
        formula.append(rule)
        #each student only in one session
        for placepair in placepairs:
            rule2=[]
            for place in placepair:
                rule2.append((nameplacify(student,place),False))
            formula.append(rule2)
    #no oversubscribed sessions
    for place in places:
        if len(students)>session_capacities[place]:
            #makes all combinations of students of size=cap+1
            givencombo=allcombos(students,session_capacities[place]+1)
            for combo in givencombo:
                rule=[]
                for student in combo:
                    rule.append((nameplacify(student,place),False))
                formula.append(rule)
    return formula
    """
    Convert a quiz-room-scheduling problem into a Boolean formula.

    student_preferences: a dictionary mapping a student name (string) to a set
                         of session names (strings) that work for that student
    session_capacities: a dictionary mapping each session name to a positive
                        integer for how many students can fit in that session

    Returns: a CNF formula encoding the scheduling problem, as per the
             lab write-up
    We assume no student or session names contain underscores.
    """

def makenametofood(result):
    nametofood={}
    if result is None:
        return None
    for personfood in result.keys():
        if result[personfood] is True:
            personfoodlist=personfood.split("_")
            nametofood[personfoodlist[0]]=personfoodlist[1]
    return nametofood

def feed(people,foods):
    return makenametofood(satisfying_assignment(boolify_scheduling_problem(people,foods)))
if __name__ == '__main__':
    import doctest
    _doctest_flags = doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS
    doctest.testmod(optionflags=_doctest_flags)
    people4={'alex': ['pie', 'casserole', 'crackers', 'candy', 'toast', 'coconut', 'cookies', 'tofu', 'oranges'], 'landry': ['oranges', 'cookies', 'crackers', 'pie', 'casserole', 'broccoli', 'tofu', 'toast', 'coconut', 'candy'], 'chris': ['cookies', 'pie', 'toast', 'casserole', 'oranges', 'candy'], 'jordan': ['pie', 'cookies', 'candy', 'casserole'], 'ana': ['pie', 'cookies', 'casserole'], 'max': ['toast', 'cookies', 'pie', 'candy', 'crackers', 'casserole', 'oranges'], 'charlie': ['cookies', 'tofu', 'oranges', 'casserole', 'candy', 'french fries', 'toast', 'broccoli', 'pie', 'coconut', 'crackers'], 'taylor': ['candy', 'casserole', 'crackers', 'tofu', 'oranges', 'pie', 'cookies', 'toast'], 'pat': ['cookies', 'casserole', 'pie'], 'casey': ['cookies', 'pie', 'casserole'], 'dana': ['cookies', 'pie', 'casserole', 'toast', 'candy'], 'duane': ['french fries', 'cookies'], 'valerie': ['pie', 'candy'], 'drew': ['candy', 'oranges', 'pie']}
    food4={'casserole': 1, 'pie': 1, 'cookies': 2, 'candy': 3, 'toast': 1, 'oranges': 1, 'crackers': 1, 'tofu': 0, 'coconut': 1, 'broccoli': 1, 'french fries': 1}
    
    print(makenametofood(satisfying_assignment(boolify_scheduling_problem(people4,food4))))
    #print((res['alice'], res['bob'])==('sandwiches', 'pie'))
    #print(sorted((res['candace'], res['dave'], res['emery']))==['cake', 'cake', 'cheese'])