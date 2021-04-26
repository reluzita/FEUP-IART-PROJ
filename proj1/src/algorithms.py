import copy
import random

from solution import Solution
from utils import choose_best_score, score, accept_with_probability


# finds the best list of libraries for a given number of remaining days
def auxiliar_neighbour(solution, current_lib, libraries, free_slots, n_days, scores):
    day = 0
    books2lib = dict()
    scanned_books = set()
    new_list = []

    while day < solution.libraries_list.index(current_lib):
        lib = solution.libraries_list[day]
        books2lib[lib] = solution.books2lib[lib]
        scanned_books.update(books2lib[lib])
        for _ in range(libraries[lib].signup_days):
            new_list.append(lib)
            day += 1

    remaining_days = libraries[current_lib].signup_days + free_slots
    all_libraries = [lib for lib in libraries if
                     lib.id not in solution.libraries_list and lib.signup_days <= remaining_days]  # gets all the libraries that can sign up and are not in the solution
    lib_id, books = choose_best_score(n_days - day, all_libraries, scores, scanned_books)  # finds the best library to sign up (compares scores)
    new_day = day

    if lib_id != -1:
        books2lib[lib_id] = books
        scanned_books.update(books)
        for _ in range(libraries[lib_id].signup_days):
            new_list.append(lib_id)
            new_day += 1

    day += libraries[current_lib].signup_days

    while day < n_days:
        lib = solution.libraries_list[day]
        if lib == -1:
            break
        books2lib[lib] = libraries[lib].get_books(n_days - new_day, scanned_books)
        scanned_books.update(books2lib[lib])
        for _ in range(libraries[lib].signup_days):
            new_list.append(lib)
            new_day += 1
            day += 1

    while len(new_list) < n_days:
        new_list.append(-1)

    new_score = score(scanned_books, scores)

    return new_list, new_score, books2lib


# function that optimizes the given solution with the best neighbour algorithm
def find_best_neighbour(solution, libraries, scores):
    best_solution = solution
    found_better = False

    n_days = len(solution.libraries_list)

    unique_libraries = set(solution.libraries_list)  # gets all the libraries ids
    if -1 in unique_libraries:
        unique_libraries.remove(-1)

    free_slots = solution.libraries_list.count(-1)
    for current_lib in unique_libraries:
        new_list, new_score, books2lib = auxiliar_neighbour(solution, current_lib, libraries, free_slots, n_days,
                                                            scores)  # gets a new solution
        if new_score > best_solution.score: # if the new solution has a higher score, the algorithm continues with this new solution as reference
            found_better = True
            best_solution = Solution(new_list, new_score, books2lib)  # creates a new solution to be used in the next iteration
            print("Found better:", new_score)

    return found_better, best_solution


# function that optimizes the given solution with the first neighbour algorithm
def find_first_neighbour(solution, libraries, scores):
    n_days = len(solution.libraries_list)

    unique_libraries = set(solution.libraries_list)  # gets all the libraries ids
    if -1 in unique_libraries:
        unique_libraries.remove(-1)

    free_slots = solution.libraries_list.count(-1)
    for current_lib in unique_libraries:
        new_list, new_score, books2lib = auxiliar_neighbour(solution, current_lib, libraries, free_slots, n_days,
                                                            scores)  # gets a new solution
        if new_score > solution.score:  # if the new solution has a higher score, the algorithm ends
            print("Found better:", solution.score)
            return True, Solution(new_list, new_score, books2lib)  # creates a new solution and returns it

    return False, solution


# function that optimizes the given solution with the random neighbour algorithm
def random_neighbour(solution, libraries, scores, n_days, heuristic):
    unique_libraries = set(solution.libraries_list)  # gets all the libraries ids
    if -1 in unique_libraries:
        unique_libraries.remove(-1)

    current_lib = random.choice(list(unique_libraries))  # choose a random library

    day = 0
    books2lib = dict()
    scanned_books = set()
    new_list = []

    while day < solution.libraries_list.index(current_lib):
        lib = solution.libraries_list[day]
        books2lib[lib] = solution.books2lib[lib]
        scanned_books.update(books2lib[lib])
        for _ in range(libraries[lib].signup_days):
            new_list.append(lib)
            day += 1

    remaining_days = libraries[current_lib].signup_days + solution.libraries_list.count(-1)
    all_libraries = [lib for lib in libraries if
                     lib.id not in solution.libraries_list and lib.signup_days <= remaining_days]

    if len(all_libraries) == 0:
        return solution

    if heuristic:  # if we want to apply the heuristic
        lib_id, books = choose_best_score(n_days - day, all_libraries, scores, scanned_books)
    else:
        lib_id = random.choice(all_libraries).id
        books = libraries[lib_id].get_books(remaining_days, scanned_books)
    new_day = day
    if lib_id != -1:
        books2lib[lib_id] = books
        scanned_books.update(books)
        for _ in range(libraries[lib_id].signup_days):
            new_list.append(lib_id)
            new_day += 1

    day += libraries[current_lib].signup_days

    while day < n_days:
        lib = solution.libraries_list[day]
        if lib == -1:
            break
        books2lib[lib] = libraries[lib].get_books(n_days - new_day, scanned_books)
        scanned_books.update(books2lib[lib])
        for _ in range(libraries[lib].signup_days):
            new_list.append(lib)
            new_day += 1
            day += 1

    while len(new_list) < n_days:  # if the new solution does not occupy n_days we fill it with -1
        new_list.append(-1)

    new_score = score(scanned_books, scores)

    return Solution(new_list, new_score, books2lib)


# finding a greedy solution for the problem, at each step, the best current choice is made
def greedy(libraries, n_days, scores):
    day = 0
    solution = [-1 for i in range(n_days)]
    scanned_books_set = set()
    scanned_books_dict = dict()
    all_libraries = copy.deepcopy(libraries)

    while day < n_days and len(all_libraries) > 0:
        lib_id, books = choose_best_score(n_days - day, all_libraries, scores, scanned_books_set)  # gets the best library to sign up
        if lib_id == -1:
            break
        lib = libraries[lib_id]
        scanned_books_dict[lib_id] = books
        scanned_books_set.update(books)
        for _ in range(lib.signup_days):  # stores in the solution the chosen library
            solution[day] = lib_id
            day += 1
        all_libraries.remove(lib)  # removes chosen library from the list of available libraries

    while len(solution) < n_days:
        solution.append(-1)

    return Solution(solution, score(scanned_books_set, scores), scanned_books_dict)


# stabilizes at 140 iterations
def cooling_function(t):
    temp = 300
    return temp / (1 + t * t)


# function that optimizes the given solution with the simulated annealing algorithm
def simulated_annealing(solution, libraries, scores, n_days):
    not_accepted = 0
    time = 0
    best_solution = solution

    while not_accepted < 200:
        new_solution = random_neighbour(solution, libraries, scores, n_days, True)  # gets new solution using random_descendent on previous found solution
        t = cooling_function(time)
        if t < 0.001:
            break  # no need to keep trying to "cool down"
        delta = new_solution.score - solution.score

        if delta <= 0 and not accept_with_probability(delta, t):
            not_accepted += 1
        else:
            solution = new_solution
            if solution.score > best_solution.score:
                best_solution = solution
            print("Accepted:", solution.score)

        time += 1

    return best_solution
