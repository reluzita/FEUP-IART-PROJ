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
    total_days = len(p1.sol)
    crossoverpoints = []
    for i in range(total_days-1):
        if p1.sol[i] != p1.sol[i+1] and p2.sol[i] != p2.sol[i+1]:
            crossoverpoints.append(i+1)
    if len(crossoverpoints) == 0: 
        return -1
    point = random.choice(crossoverpoints)

    lib1 = set(p1.sol[:point])
    lib2 = set(p2.sol[point:])

    duplicates = [x for x in lib2 if x in lib1]

    part2 = remove_duplicates(p2.sol[point:], duplicates, libraries)

    child = p1.sol[:point]
    child.extend(part2)

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
        books.update(lib.get_books(n_days - day))
        day+=lib.signup_days
    return score(books, scores)

def genetic_algorithm(population, libraries, scores, mutation_prob, swap_prob):
    new_population = []
    for _ in range(len(population)):
        
        parent1, parent2 = tournament(population, 3)
        child = reproduce(parent1, parent2, libraries)
        while child == -1:
            parent1, parent2 = tournament(population, 3)
            child = reproduce(parent1, parent2, libraries)
        new_population.append(generate_solution(child, libraries, scores))
    
    total_population = copy.deepcopy(new_population)
    total_population.extend(population)

    mutate_population(total_population, libraries, scores, mutation_prob, swap_prob)

    return sorted(total_population, key=lambda x:x.score, reverse=True)[:len(population)]

def generate_random(n_days, libraries, scores):
    not_used = [i for i in range(len(libraries))]
    sol = [-1 for j in range(n_days)]
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
            sol[day] = lib_id
            day+=1
        not_used.remove(lib_id)
    #calcular score
    books = set()
    day = 0
    while day < n_days:
        if sol[day] == -1: break
        lib = libraries[sol[day]]
        books.update(lib.get_books(n_days - day))
        day += lib.signup_days
    return generate_solution(sol, libraries, scores)

def mutate_population(population, libraries, scores, mutation_prob, swap_prob):
    for solution in population:
        lib_list = None
        if random.random() < mutation_prob:
            lib_list = mutate_solution(solution.sol, libraries, 0.1)
        if random.random() < swap_prob:
            lib_list = swap_mutation(solution.sol, libraries)
        if lib_list != None:
            day = 0 
            n_days = len(lib_list)
            books2lib = dict()
            books = set()
            while day < n_days:
                lib = lib_list[day]
                books2lib[lib] = libraries[lib].get_books(n_days - day)
                books.update(books2lib[lib])
                day += libraries[lib].signup_days
            solution = Solution(lib_list, score(books, scores), books2lib)

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
