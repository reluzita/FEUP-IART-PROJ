import copy
import math
import random

from library import Library
from solution import Solution


def generate_solution(libraries_list, libraries, scores):
    day = 0
    n_days = len(libraries_list)
    books2lib = dict()
    books = set()
    while day < n_days:
        lib = libraries_list[day]
        if lib == -1:
            break
        books2lib[lib] = libraries[lib].get_books(n_days - day, books)
        books.update(books2lib[lib])
        day += libraries[lib].signup_days

    return Solution(libraries_list, score(books, scores), books2lib)


def score(books, scores):
    return sum([scores[b] for b in books])


def choose_best_score(days, libraries, scores, scanned_books):
    best_score = 0
    best_books = []
    best_lib = None
    for library in libraries:
        if library.signup_days > days: continue
        books = library.get_books(days, scanned_books)
        s = score(books, scores) / library.signup_days
        if s > best_score:
            best_lib = library.id
            best_score = s
            best_books = books

    if best_lib is None:
        return -1, best_books

    return best_lib, best_books


def read_libraries(lines, n_libraries, scores):
    libraries = []
    for i in range(0, n_libraries):
        info = lines[i * 2].split()
        books = sorted([int(n) for n in lines[i * 2 + 1].split()], key=lambda x: scores[x], reverse=True)
        libraries.append(Library(i, books, int(info[1]), int(info[2])))

    return libraries


def find_best_neighbour(solution, libraries, scores, n_days):
    best_solution = solution
    found_better = False

    n_days = len(solution.libraries_list)

    unique_libraries = set(solution.libraries_list)
    if -1 in unique_libraries: 
        unique_libraries.remove(-1)

    free_slots = solution.libraries_list.count(-1)
    for current_lib in unique_libraries:
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
                day+=1
        
        remaining_days = libraries[current_lib].signup_days + free_slots
        all_libraries = [lib for lib in libraries if lib.id not in solution.libraries_list and lib.signup_days <= remaining_days]
        lib_id, books = choose_best_score(n_days - day, all_libraries, scores, scanned_books)
        new_day = day
        if lib_id != -1:
            books2lib[lib_id] = books
            scanned_books.update(books)
            for _ in range(libraries[lib_id].signup_days):
                new_list.append(lib_id)
                new_day+=1

        day += libraries[current_lib].signup_days
    
        while day < n_days:
            lib = solution.libraries_list[day]
            if lib == -1: break
            books2lib[lib] = libraries[lib].get_books(n_days - new_day, scanned_books)
            scanned_books.update(books2lib[lib])
            for _ in range(libraries[lib].signup_days):
                new_list.append(lib)
                new_day+=1
                day+=1

        while len(new_list) < n_days:
            new_list.append(-1)

        new_score = score(scanned_books, scores)
        if new_score > best_solution.score:
            found_better = True
            best_solution = Solution(new_list, new_score, books2lib)
            print("Found better:", new_score)

    return found_better, best_solution


def find_first_neighbour(solution, libraries, scores, n_days):
    n_days = len(solution.libraries_list)

    unique_libraries = set(solution.libraries_list)
    if -1 in unique_libraries: 
        unique_libraries.remove(-1)

    free_slots = solution.libraries_list.count(-1)
    for current_lib in unique_libraries:
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
                day+=1
        
        remaining_days = libraries[current_lib].signup_days + free_slots
        all_libraries = [lib for lib in libraries if lib.id not in solution.libraries_list and lib.signup_days <= remaining_days]
        lib_id, books = choose_best_score(n_days - day, all_libraries, scores, scanned_books)
        new_day = day
        if lib_id != -1:
            books2lib[lib_id] = books
            scanned_books.update(books)
            for _ in range(libraries[lib_id].signup_days):
                new_list.append(lib_id)
                new_day+=1

        day += libraries[current_lib].signup_days
    
        while day < n_days:
            lib = solution.libraries_list[day]
            if lib == -1: break
            books2lib[lib] = libraries[lib].get_books(n_days - new_day, scanned_books)
            scanned_books.update(books2lib[lib])
            for _ in range(libraries[lib].signup_days):
                new_list.append(lib)
                new_day+=1
                day+=1

        while len(new_list) < n_days:
            new_list.append(-1)

        new_score = score(scanned_books, scores)
        if new_score > solution.score:
            print("Found better:", solution.score)
            return True, Solution(new_list, new_score, books2lib)
    
    return False, solution


def choose_random_neighbour(libraries, libraries_set, n_days):  # returns a random id of a library
    tries = 0

    while tries < 100000:
        rand = random.sample(libraries_set, 1)
        if libraries[rand[0]].signup_days < n_days:
            return rand[0]
    return 0


def random_neighbour(solution, libraries, scores, n_days, heuristic):
    unique_libraries = set(solution.libraries_list)
    if -1 in unique_libraries: 
        unique_libraries.remove(-1)

    current_lib = random.choice(list(unique_libraries))

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
            day+=1

    remaining_days = libraries[current_lib].signup_days + solution.libraries_list.count(-1)
    all_libraries = [lib for lib in libraries if lib.id not in solution.libraries_list and lib.signup_days <= remaining_days]

    if len(all_libraries) == 0: return solution

    if heuristic: # if we want to apply the heuristic
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
            new_day+=1

    day += libraries[current_lib].signup_days

    while day < n_days:
        lib = solution.libraries_list[day]
        if lib == -1: break
        books2lib[lib] = libraries[lib].get_books(n_days - new_day, scanned_books)
        scanned_books.update(books2lib[lib])
        for _ in range(libraries[lib].signup_days):
            new_list.append(lib)
            new_day+=1
            day+=1

    while len(new_list) < n_days: # if the new solution does not occupy n_days we fill it with -1
        new_list.append(-1)

    new_score = score(scanned_books, scores)

    return Solution(new_list, new_score, books2lib)


def greedy(libraries, n_days, scores):  # finding a greedy solution for the problem, at each step, the best current choice is made
    day = 0
    solution = [-1 for i in range(n_days)]
    scanned_books_set = set()
    scanned_books_dict = dict()
    all_libraries = copy.deepcopy(libraries)

    while day < n_days and len(all_libraries) > 0:
        lib_id, books = choose_best_score(n_days - day, all_libraries, scores, scanned_books_set)
        if lib_id == -1:
            break
        lib = libraries[lib_id]
        scanned_books_dict[lib_id] = books
        scanned_books_set.update(books)
        for _ in range(lib.signup_days):
            solution[day] = lib_id
            day += 1
        all_libraries.remove(lib)

    while len(solution) < n_days:
        solution.append(-1)

    return Solution(solution, score(scanned_books_set, scores), scanned_books_dict)


def cooling_function(t):  # stabilizes at 140 iterations
    temp = 500
    return temp / (1 + t*t)
    


# function to calculate the if the solution is accepted with a certain probability
def accept_with_probability(delta, t):
    r = random.randrange(0, 1)
    f = math.exp(delta / t)
    if f >= r:
        return True
    else:
        return False


def simulated_annealing(solution, libraries, scores, n_days):
    not_accepted = 0
    time = 0

    while not_accepted < 200:
        new_solution = random_neighbour(solution, libraries, scores, n_days, False) # gets new solution using random_descendent on previous found solution
        t = cooling_function(time)
        print(t)
        if t < 0.01: break # no need to keep trying to "cool down"
        delta = new_solution.score - solution.score

        if delta <= 0 and not accept_with_probability(delta, t): 
            not_accepted += 1
        else:
            solution = new_solution
            print("Found better:", solution.score)

        time += 1

    print(time)
    return solution
