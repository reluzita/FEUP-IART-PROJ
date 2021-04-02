import copy
import random
from math import ceil

from utils import score, generate_solution

# tournament function, choosing the two parents to use for reproduction
def tournament(population, np):
    # get a random sample of size np from the population and choose the one with higher score
    g1 = random.sample(population, np)
    parent1 = sorted(g1, key=lambda x: x.score, reverse=True)[0]

    # get a random sample of size np from the remaining population and choose the one with higher score
    rest = [x for x in population if x not in g1]
    g2 = random.sample(rest, np)
    parent2 = sorted(g2, key=lambda x: x.score, reverse=True)[0]

    # return the two "winners"
    return parent1, parent2

# function that performs single point crossover on two given solutions
def single_point_crossover(p1, p2, libraries):
    total_days = len(p1)
    crossoverpoints = []

    # find possible crossover points (array indeces where the library changes on both solutions)
    for i in range(total_days - 1):
        if p1[i] != p1[i + 1] and p2[i] != p2[i + 1]:
            crossoverpoints.append(i + 1)
    if len(crossoverpoints) == 0:
        # no possibilities to do the crossover 
        return -1
    # choose a random point from the found ones
    point = random.choice(crossoverpoints)

    # get first part of one parent and second part of the other
    lib1 = set(p1[:point])
    lib2 = set(p2[point:])

    # find duplicates and remove them
    duplicates = [x for x in lib2 if x in lib1]

    part2 = remove_duplicates(p2[point:], duplicates, libraries)

    # return result of concatenating the two list 
    child = p1[:point]
    child.extend(part2)

    return child

# function that performs linear order crossover on two given solutions
def crossover(p1, p2, libraries):
    # get library ids in parent 1
    libs1 = set(p1)
    if -1 in libs1:
        libs1.remove(-1)

    # get 2 random libraries to delimit linear order portion
    delimiters = random.sample(libs1, 2)
    delimiters = sorted(delimiters, key=lambda x: p1.index(x))

    # get linear order portion from parent 1
    point1 = p1.index(delimiters[0])
    point2 = len(p1) - p1[::-1].index(delimiters[1])
    portion = p1[point1:point2]

    # get libraries from parent 2 that aren't already part of the chosen portion
    libs2 = set(p2)
    if -1 in libs2:
        libs2.remove(-1)
    remaining_libs = list(filter(lambda x: x not in portion, list(libs2)))

    #calculate remaining days to fill with libraries
    slots_before = point1
    slots_after = len(p1) - point2

    # fill days before portion with libraries from parent 2
    initial_part = []
    while slots_before > 0:
        found = False
        for lib in remaining_libs:
            n = libraries[lib].signup_days
            if n <= slots_before:
                for _ in range(n):
                    initial_part.append(lib)
                remaining_libs.remove(lib)
                slots_before -= n
                found = True
                break
        if not found:
            break

    # fill days after portion with libraries from parent 2
    slots_after += slots_before
    final_part = []
    while slots_after > 0:
        found = False
        for lib in remaining_libs:
            n = libraries[lib].signup_days
            if n <= slots_after:
                for _ in range(n):
                    final_part.append(lib)
                remaining_libs.remove(lib)
                slots_after -= n
                found = True
                break
        if not found:
            break
    
    # concatenate all parts and return resulting solution
    child = initial_part
    child.extend(portion)
    child.extend(final_part)
    while len(child) < len(p1):
        child.append(-1)

    return child

# function that removes duplicate libraries in solution
def remove_duplicates(solution, duplicates, libraries):
    final = copy.deepcopy(solution)

    # iterate over each duplicated library, replacing it with a random one that keeps the solution valid
    for old_id in duplicates:
        day = solution.index(old_id)
        old_lib = libraries[old_id]

        # separate first and last part of the list on the library to replace and calculate maximum signup_days for the new one
        first_part = solution[:day]
        second_part = list(filter(lambda a: a != -1, solution[day + old_lib.signup_days:]))
        remaining_days = len(solution) - (len(first_part) + len(second_part))

        # find all libraries that keep the solution valid and choose a random one, simply removing the old one if no other library is valid
        not_used = [lib for lib in libraries if lib.id not in solution and lib.signup_days < remaining_days]
        new_solution = first_part
        if len(not_used) > 0:
            new_lib = random.choice(not_used)

            for _ in range(new_lib.signup_days):
                new_solution.append(new_lib.id)

        new_solution.extend(second_part)

        # fill the remaining days with -1 to keep the solution valid
        while len(new_solution) < len(solution):
            new_solution.append(-1)

        final = copy.deepcopy(new_solution)

    return final

# function that given the libraries signup list for each day, calculates the total score of this solution
def calculate_solution_score(sol, libraries, scores):
    books = set()
    day = 0
    n_days = len(sol)
    # iterates over the list, in which each position has the id of the library being signup up in the day corresponding to that index 
    while day < n_days:
        if sol[day] == -1:
            # already signed up all libraries
            break
        lib = libraries[sol[day]]
        # get all books that the current library can send, given the remaining days and already scanned books
        books.update(lib.get_books(n_days - day, books))
        # skip to next library's index
        day += lib.signup_days
    # return total score of the scanned books
    return score(books, scores)

# function that simulates one generation of the genetic algorithm, generating the new generation given the current population
def genetic_algorithm(population, libraries, scores, mutation_prob, swap_prob, population_variation):
    new_population = []
    # generate as many new solutions as the population size
    for _ in range(len(population)):
        parent1, parent2 = tournament(population, 3) # choose two solutions to reproduce
        child = crossover(parent1.libraries_list, parent2.libraries_list, libraries) # perform linear order crossover on chosen parents
        new_population.append(generate_solution(child, libraries, scores)) # add generated solution to the new population

    total_population = copy.deepcopy(new_population)
    total_population.extend(population)

    mutate_population(total_population, libraries, scores, mutation_prob, swap_prob, population_variation) # perform mutations on the population, according to given propabilities

    return sorted(total_population, key=lambda x: x.score, reverse=True)[:len(population)] # return new population containing the top n individuals, n being the initial population size

# function that generates a random valid solution, given the number of days, libraries to scan and book scores
def generate_random(n_days, libraries, scores):
    not_used = [i for i in range(len(libraries))] # no library has been used yet
    libraries_list = [-1 for j in range(n_days)] # fill solution with -1 to mark all days as "empty"

    day = 0
    # fill solution while there are still days left
    while day < n_days:
        if len(not_used) == 0:
            break # stop if all libraries have been used
        lib_id = random.choice(not_used) # get a random library that hasn't been used
        lib = libraries[lib_id]
        # if the library has a signup time too large for he remaining days, remove it from possible choices and pick a new one
        while len(not_used) > 1 and lib.signup_days > n_days - day:
            not_used.remove(lib_id)
            lib_id = random.choice(not_used)
            lib = libraries[lib_id]
        if len(not_used) == 1:
            break # stop if all libraries have been used
        # fill chosen library's days in the solution list and skip to the next library's signup day
        for _ in range(lib.signup_days):
            libraries_list[day] = lib_id
            day += 1
        not_used.remove(lib_id) # remove library from the not used list

    return generate_solution(libraries_list, libraries, scores) # return solution object generated from the created list

# function that applies mutations on the population based on given probabilities
def mutate_population(population, libraries, scores, mutation_prob, swap_prob, population_variation):
    # iterate over all individuals
    for solution in population:
        lib_list = None
        if random.random() < mutation_prob: # mutate part of the genes of the solution with a mutation_prob probability
            lib_list = mutate_solution(solution.libraries_list, libraries, population_variation)
        if random.random() < swap_prob: # swap two genes of the solution with a swap_prob probability
            lib_list = swap_mutation(solution.libraries_list, libraries)
        if lib_list is not None: # replace current solution with new solution object if any mutations occured
            solution = generate_solution(lib_list, libraries, scores)

# function that mutates mutation_no percentage of the genes of a given solution 
def mutate_solution(solution, libraries, mutation_no):
    # get all libraries (genes) of the solution
    uniques = set(solution)
    if -1 in uniques:
        uniques.remove(-1)
    old_lib_ids = random.sample(list(uniques), ceil(mutation_no * len(uniques))) # calculate number of genes to mutate and ramdomly select them

    new_solution = copy.deepcopy(solution)
    # iterate over genes to mutate them by replacing them with a random library
    for i in old_lib_ids:
        old_lib = libraries[i]

        day = new_solution.index(i)

        # split solution and calculate maximum days available for the new library to signup
        first_part = new_solution[:day]
        second_part = list(filter(lambda a: a != -1, new_solution[day + old_lib.signup_days:]))
        remaining_days = len(new_solution) - (len(first_part) + len(second_part))

        # get a random library until finding a valid one
        new_lib = random.choice(libraries) 
        checked = {new_lib}
        n = len(libraries)
        while (new_lib.id in new_solution or new_lib.signup_days > remaining_days) and len(checked) < n:
            new_lib = random.choice(libraries)
            checked.add(new_lib)

        # build the first part of the new solution list
        new_solution = first_part

        # add the new library, if a valid one was found 
        if new_lib.id not in new_solution and new_lib.signup_days <= remaining_days:
            for _ in range(new_lib.signup_days):
                new_solution.append(new_lib.id)

        # add the last part of the solution and fill remaining days with -1
        new_solution.extend(second_part)

        while len(new_solution) < len(solution):
            new_solution.append(-1)

    return new_solution # return mutated solution

# function that swaps two genes of a given solution
def swap_mutation(solution, libraries):
    # select two random genes (libraries) to swap
    uniques = set(solution)
    [lib1, lib2] = random.sample(uniques, 2)

    day1 = solution.index(lib1)
    day2 = solution.index(lib2)
    while day1 > day2: # if lib1 is scanned after lib2, select a new pair
        [lib1, lib2] = random.sample(uniques, 2)
        day1 = solution.index(lib1)
        day2 = solution.index(lib2)

    # get signup days of both libraries
    signup1 = libraries[lib1].signup_days
    signup2 = libraries[lib2].signup_days

    # create new list by concatenating the original solution's parts, switching the chosen libraries' positions
    new_solution = solution[:day1]
    new_solution.extend([lib2 for _ in range(signup2)])
    new_solution.extend(solution[day1 + signup1:day2])
    new_solution.extend([lib1 for _ in range(signup1)])
    new_solution.extend(solution[day2 + signup2:])

    return new_solution


# function that given an input file returns the values for population size, number of generations, mutation and swap
# probabilities and population variation
def get_parameters(inputfile):
    population_size = 50
    generations = 1000
    mutation_prob = 0.2
    swap_prob = 0.2
    population_variation = 0.2

    # all the below values were chosen after a battery of tests
    if inputfile == "b_read_on.txt":
        population_size = 50
        generations = 1000
        mutation_prob = 0.2
        swap_prob = 0.2
        population_variation = 0.2
    elif inputfile == "c_incunabula.txt":
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
        population_size = 20
        generations = 500
        mutation_prob = 0.2
        swap_prob = 0.2
        population_variation = 0.2
    elif inputfile == "f_libraries_of_the_world.txt":
        population_size = 20
        generations = 100
        mutation_prob = 0.2
        swap_prob = 0.2
        population_variation = 0.2

    return population_size, generations, mutation_prob, swap_prob, population_variation
