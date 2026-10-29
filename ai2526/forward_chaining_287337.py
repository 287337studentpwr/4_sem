"""
zalozenia:
1) w zasadach po implikacji moze wystepowac tylko jeden predykat
2) kazdy argument w predykatach jest istotnym argumentem! ( nie mogą występować parametry, cos czego nie mozemy zmapowac)
3) zakladam ze jezeli A(x) i A(y) => B(x, y) to nie musi byc spelniony warunek x !=y zatem w takich przypadkach dla kazdego A(x) A(x) => B(x, x) czyli na moim przypadku Dziecko_1 może być własnym rodzeństwem co teoretycznie jest prawda
"""

def check_for_requirements(requirements, facts):
    dictionary_final = [{}]

    for req in requirements:
        predicate_req, arguments_req = req

        new_dictionary_final = []

        for dictionary in dictionary_final:
            for fact in facts:
                predicate_facts, arguments_facts = fact

                if predicate_facts != predicate_req:
                    continue

                dictionary_potential = dictionary.copy()
                satisfied = True

                for i in range(len(arguments_req)):
                    variable = arguments_req[i]
                    value = arguments_facts[i]

                    if variable in dictionary_potential:
                        if dictionary_potential[variable] != value:
                            satisfied = False
                            break
                    else:
                        dictionary_potential[variable] = value

                if satisfied:
                    new_dictionary_final.append(dictionary_potential)

        dictionary_final = new_dictionary_final

        if dictionary_final == []:
            return []

    return dictionary_final

def map_arguments(argument_mapping, conclusions):
    predicate_concl = conclusions[0]
    arguments_concl = conclusions[1]
    argumnets_final = []
    for argument in arguments_concl:
        argument_mapped = argument_mapping[argument]
        argumnets_final.append(argument_mapped)
    return (predicate_concl, tuple(argumnets_final))
        
    
    
    
def forward_chaining_final(facts, rules, goal=None):
    changed = True
    while changed:
        changed = False
        for rule in rules:
            requirements = rule[0]
            conclusions = rule[1]
            argument_mappings = check_for_requirements(requirements, facts)
            if argument_mappings:
                for mapping in argument_mappings:
                    new_fact = map_arguments(mapping, conclusions)
                    if new_fact not in facts:
                        facts.add(new_fact)
                        changed = True
                    if goal is not None and new_fact == goal:
                        return True, facts
    if goal is None:
        return facts
    return goal in facts, facts               
                    
def check():
    facts = {("Child", ("Dziecko_1","Rodzic")), ("Child", ("Dziecko_2","Rodzic"))}
    rules = [
    (
        [("Child", ("x","y")), (("Child"), ("z","y"))],
        ("Siblings", ("x","z"))
    )
]
    print(forward_chaining_final(facts, rules))

check()