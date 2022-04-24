def allof(dict):
    return list(dict.keys())
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
def nameplacify(name,place):
    return str(name+'_'+place)
student_preferences={'Alice': {'basement', 'penthouse'},
                            'Bob': {'kitchen'},
                            'Charles': {'basement', 'kitchen'},
                            'Dana': {'kitchen', 'penthouse', 'basement'}}
session_capacities={'basement': 1,'kitchen': 2,'penthouse': 4}
places=allof(session_capacities)
students=allof(student_preferences)
formula=[]

for place in places:
    if len(students)>session_capacities[place]:
        givencombo=allcombos(students,session_capacities[place]+1) #this part is wrong
        for combo in givencombo:
            rule=[]
            for student in combo:
                rule.append((nameplacify(student,place),False))
            formula.append(rule)
print(formula)
