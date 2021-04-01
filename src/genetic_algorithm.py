import random
from utils import score, generate_solution
from solution import Solution
import copy
from math import ceil

def tournament(population, np):
    g1 = random.sample(population, np)
    parent1 = sorted(g1, key=lambda x: x.score, reverse=True)[0]

    rest = [x for x in population if x not in g1]
    g2 = random.sample(rest, np)
    parent2 = sorted(g2, key=lambda x: x.score, reverse=True)[0]
    return parent1, parent2

def reproduce(p1, p2, libraries):
    total_days = len(p1)
    crossoverpoints = []
    for i in range(total_days-1):
        if p1[i] != p1[i+1] and p2[i] != p2[i+1]:
            crossoverpoints.append(i+1)
    if len(crossoverpoints) == 0: 
        return -1
    point = random.choice(crossoverpoints)

    lib1 = set(p1[:point])
    lib2 = set(p2[point:])

    duplicates = [x for x in lib2 if x in lib1]

    part2 = remove_duplicates(p2[point:], duplicates, libraries)

    child = p1[:point]
    child.extend(part2)

    return child

def crossover(p1, p2):
    #get library ids in parent 1
    libs1 = set(p1)
    if -1 in libs1:
        libs1.remove(-1)

    #get 2 random libraries to delimit linear order portion
    delimiters = random.sample(libs1, 2)
    delimiters = sorted(delimiters, key=lambda x: p1.index(x))

    #get linear order portion from parent 1
    point1 = p1.index(delimiters[0])
    point2 = len(p1) - p1[::-1].index(delimiters[1])
    portion = p1[point1:point2]

    remaining_libs = []
    for lib in p2:
        if lib == -1:
            break
        if lib not in remaining_libs and lib not in portion:
            remaining_libs.append(lib)

    slots_before = point1
    slots_after = len(p1) - point2

    initial_part = []
    while slots_before > 0:
        found = False
        for lib in remaining_libs:
            n = p2.count(lib) 
            if n <= slots_before:
                for _ in range(n): initial_part.append(lib)
                remaining_libs.remove(lib)
                slots_before -= n
                found = True
                break
        if not found:
            break

    slots_after += slots_before
    final_part = []
    while slots_after > 0:
        found = False
        for lib in remaining_libs:
            n = p2.count(lib) 
            if n <= slots_after:
                for _ in range(n): final_part.append(lib)
                remaining_libs.remove(lib)
                slots_after -= n
                found = True
                break
        if not found:
            break
    
    child = initial_part
    child.extend(portion)
    child.extend(final_part)
    while len(child) < len(p1):
        child.append(-1)

    return child
    

    
def remove_duplicates(solution, duplicates, libraries):
    final = copy.deepcopy(solution)
    
    for old_id in duplicates:
        day = solution.index(old_id)
        old_lib = libraries[old_id]

        first_part = solution[:day]
        second_part = list(filter(lambda a: a != -1, solution[day + old_lib.signup_days:]))
        remaining_days = len(solution) - (len(first_part) + len(second_part))

        not_used = [lib for lib in libraries if lib.id not in solution and lib.signup_days < remaining_days]
        new_solution = first_part
        if len(not_used) > 0:
            new_lib = random.choice(not_used)
                    
            for _ in range(new_lib.signup_days):
                new_solution.append(new_lib.id)
                           
        new_solution.extend(second_part)

        while(len(new_solution) < len(solution)):
            new_solution.append(-1)

        final = copy.deepcopy(new_solution)
        
    return final

def calculate_solution_score(sol, libraries, scores):
    books = set()
    day = 0
    n_days = len(sol)
    while day < n_days:
        if sol[day] == -1: break
        lib = libraries[sol[day]]
        books.update(lib.get_books(n_days - day, books))
        day+=lib.signup_days
    return score(books, scores)

def genetic_algorithm(population, libraries, scores, mutation_prob, swap_prob, population_variation):
    new_population = []
    for _ in range(len(population)):
        parent1, parent2 = tournament(population, 3)
        #child = reproduce(parent1.libraries_list, parent2.libraries_list, libraries)
        #while child == -1:
        #    parent1, parent2 = tournament(population, 3)
        #    child = reproduce(parent1.libraries_list, parent2.libraries_list, libraries)
        child = crossover(parent1.libraries_list, parent2.libraries_list)
        new_population.append(generate_solution(child, libraries, scores))
    
    total_population = copy.deepcopy(new_population)
    total_population.extend(population)

    mutate_population(total_population, libraries, scores, mutation_prob, swap_prob, population_variation)

    return sorted(total_population, key=lambda x:x.score, reverse=True)[:len(population)]

def generate_random(n_days, libraries, scores):
    not_used = [i for i in range(len(libraries))]
    libraries_list = [-1 for j in range(n_days)]

    day = 0
    while day < n_days:
        if len(not_used) == 0: break
        lib_id = random.choice(not_used)
        lib = libraries[lib_id]
        while len(not_used) > 1 and lib.signup_days > n_days - day:
            not_used.remove(lib_id)
            lib_id = random.choice(not_used)
            lib = libraries[lib_id]
        if len(not_used) == 1: break
        for _ in range(lib.signup_days):
            libraries_list[day] = lib_id
            day+=1
        not_used.remove(lib_id)
    
    return generate_solution(libraries_list, libraries, scores)

def mutate_population(population, libraries, scores, mutation_prob, swap_prob, population_variation):
    for solution in population:
        lib_list = None
        if random.random() < mutation_prob:
            lib_list = mutate_solution(solution.libraries_list, libraries, population_variation)
        if random.random() < swap_prob:
            lib_list = swap_mutation(solution.libraries_list, libraries)
        if lib_list != None:
            solution = generate_solution(lib_list, libraries, scores)

def mutate_solution(solution, libraries, mutation_no):
    uniques = set(solution)
    old_lib_ids = random.sample(list(uniques), ceil(mutation_no*len(uniques)))

    new_solution = copy.deepcopy(solution)
    for i in old_lib_ids:
        old_lib = libraries[i]

        day = new_solution.index(i)

        first_part = new_solution[:day]
        second_part = list(filter(lambda a: a != -1, new_solution[day + old_lib.signup_days:]))
        remaining_days = len(new_solution) - (len(first_part) + len(second_part))

        not_used = [lib for lib in libraries if lib.id not in new_solution and lib.signup_days < remaining_days]
        new_solution = first_part
        if len(not_used) > 0:
            new_lib = random.choice(not_used)
                    
            for _ in range(new_lib.signup_days):
                new_solution.append(new_lib.id)
                        
        new_solution.extend(second_part)

        while(len(new_solution) < len(solution)):
            new_solution.append(-1)

    return new_solution

def swap_mutation(solution, libraries):
    uniques = set(solution)
    [lib1, lib2] = random.sample(uniques, 2)

    day1 = solution.index(lib1)
    day2 = solution.index(lib2)
    while day1 > day2:
        [lib1, lib2] = random.sample(uniques, 2)
        day1 = solution.index(lib1)
        day2 = solution.index(lib2)

    signup1 = libraries[lib1].signup_days
    signup2 = libraries[lib2].signup_days

    new_solution = solution[:day1]
    new_solution.extend([lib2 for d in range(signup2)])
    new_solution.extend(solution[day1+signup1:day2])
    new_solution.extend([lib1 for d in range(signup1)])
    new_solution.extend(solution[day2+signup2:])

    return new_solution                  

def get_parameters(inputfile):
    if inputfile == "c_incunabula.txt":
        population_size = 10
        generations = 10
        mutation_prob = 0.05
        swap_prob = 0.05
        population_variation = 0.01
    elif inputfile == "d_tough_choices.txt":
        population_size = 10
        generations = 10
        mutation_prob = 0.05
        swap_prob = 0.05
        population_variation = 0.001
    elif inputfile == "e_so_many_books.txt":
        population_size = 50
        generations = 1000
        mutation_prob = 0.2
        swap_prob = 0.2
        population_variation = 0.2
    elif inputfile == "f_libraries_of_the_world.txt":
        population_size = 50
        generations = 1000
        mutation_prob = 0.2
        swap_prob = 0.2
        population_variation = 0.2

    return population_size, generations, mutation_prob, swap_prob, population_variation