from library import Library
import copy
from solution import Solution
import random

def generate_solution(libraries_list, libraries, scores):
    day = 0 
    n_days = len(libraries_list)
    books2lib = dict()
    books = set()
    while day < n_days:
        lib = libraries_list[day]
        if lib == -1:
            break
        books2lib[lib] = libraries[lib].get_books(n_days - day)
        books.update(books2lib[lib])
        day += libraries[lib].signup_days

    return Solution(libraries_list, score(books, scores), books2lib)

def score(books, scores):
    return sum([scores[b] for b in books])

def choose_best_score(days, libraries, scores, scanned_books):
    lib_scores = dict()
    for library in libraries:
        if library.signup_days > days: continue
        books = [b for b in library.get_books(days) if b not in scanned_books]
        lib_scores[library.id] = score(books, scores)/library.signup_days
    
    if len(lib_scores) == 0:
        return -1
    maximum = max(lib_scores.values())

    return list(lib_scores.keys())[list(lib_scores.values()).index(maximum)]


def read_libraries(lines, n_libraries, scores):
    libraries = []
    for i in range(0, n_libraries):
        info = lines[i*2].split()
        books = sorted([int(n) for n in lines[i*2+1].split()], key=lambda x: scores[x], reverse=True)
        libraries.append(Library(i, books, int(info[1]), int(info[2])))
        
    return libraries

def calculate_total_score(books_dict, scores):
    all_books = set()
    for id in books_dict:
        all_books.update(books_dict[id])
    return score(list(all_books), scores)


def find_best_neighbour(solution, libraries, scores, n_days):
    best_score = calculate_total_score(solution.books2lib, scores) 
    best_libraries = copy.deepcopy(solution.sol)
    best_books = copy.deepcopy(solution.books2lib)
    found_better = False

    for current_lib in best_libraries:
        day = 0
        new_list = []
        scanned_books_dict = dict()
        scanned_books_set = set()
        all_libraries = copy.deepcopy(libraries)
        for lib in solution.sol:
            if lib == -1: 
                break
            elif lib == current_lib:
                try:
                    all_libraries.remove(libraries[lib])
                except ValueError:
                    pass
                break
            else:
                new_list.append(libraries[lib])
                scanned_books_dict[lib] = libraries[lib].get_books(n_days-day)
                scanned_books_set.update(scanned_books_dict[lib])
                try:
                    all_libraries.remove(libraries[lib])
                except ValueError:
                    pass
                day += libraries[lib].signup_days

        
        while day < n_days and len(all_libraries) > 0:
            id = choose_best_score(n_days - day, all_libraries, scores, scanned_books_set)
            if id == -1:
                break
            for lib in all_libraries:
                if lib.id == id:
                    scanned_books_dict[lib.id] = lib.get_books(n_days-day)
                    scanned_books_set.update(scanned_books_dict[lib.id])
                    new_list.append(lib)
                    day += lib.signup_days
                    all_libraries.remove(lib)

        new_score = calculate_total_score(scanned_books_dict, scores)
        if new_score > best_score:
            found_better = True
            best_libraries = copy.deepcopy(new_list)
            best_books = copy.deepcopy(scanned_books_dict)
            best_score = new_score
            print("better!")
        else:
            print("not better :(")

    return found_better, Solution(best_libraries, best_score, best_books)

def find_first_neighbour(solution, libraries, scores, n_days):
    best_score = calculate_total_score(solution.books2lib, scores) 
    best_libraries = copy.deepcopy(solution.sol)
    best_books = copy.deepcopy(solution.books2lib)
    found_better = False
   

    for current_lib in solution.sol:
        day = 0
        new_list = []
        scanned_books_dict = dict()
        scanned_books_set = set()
        all_libraries = copy.deepcopy(libraries)

        for lib in solution.sol:
            if lib == -1: 
                break
            elif lib == current_lib:
                try:
                    all_libraries.remove(libraries[lib])
                except ValueError:
                    pass
                break
            else:
                new_list.append(lib)
                scanned_books_dict[lib] = libraries[lib].get_books(n_days-day)
                scanned_books_set.update(scanned_books_dict[lib])
                try:
                    all_libraries.remove(libraries[lib])
                except ValueError:
                    pass
                break
                day += libraries[lib].signup_days

        
        while day < n_days and len(all_libraries) > 0:
            id = choose_best_score(n_days - day, all_libraries, scores, scanned_books_set)
            if id == -1:
                break
            for lib in all_libraries:
                if lib.id == id:
                    scanned_books_dict[lib.id] = lib.get_books(n_days-day)
                    scanned_books_set.update(scanned_books_dict[lib.id])
                    new_list.append(lib)
                    day += lib.signup_days
                    all_libraries.remove(lib)

        new_score = calculate_total_score(scanned_books_dict, scores)
        if new_score > best_score:
            found_better = True
            best_libraries = copy.deepcopy(new_list)
            best_books = copy.deepcopy(scanned_books_dict)
            best_score = new_score
            print("better!")
            return found_better, Solution(best_libraries,best_score, best_books)
        else:
            print("not better :(")

    return found_better, Solution(best_libraries, best_score, best_books)

def random_descendent(choosen_libraries, choosen_books, libraries, scores, n_days):
    return True

def random_walk(solution, libraries, scores, n_days):
    uniques = set(solution.sol)
    current_lib = random.choice(list(uniques))
    day = 0
    
    scanned_books_dict = dict()
    scanned_books_set = set()
    all_libraries = copy.deepcopy(libraries)
    all_libraries.remove(libraries[current_lib])

    new_day = solution.sol.index(current_lib)
    new_list = solution.sol[:new_day]
    while day < new_day:
        lib = libraries[solution.sol[day]]
        scanned_books_dict[lib.id] = lib.get_books(n_days-day)
        scanned_books_set.update(scanned_books_dict[lib.id])
        all_libraries.remove(lib)
        day += lib.signup_days

        
    while day < n_days and len(all_libraries) > 0:
        id = choose_best_score(n_days - day, all_libraries, scores, scanned_books_set)
        if id == -1:
            break
        lib = libraries[id]
        scanned_books_dict[lib.id] = lib.get_books(n_days-day)
        scanned_books_set.update(scanned_books_dict[lib.id])
        new_list.extend([lib.id for _ in range(lib.signup_days)])
        day += lib.signup_days
        all_libraries.remove(lib)

    new_score = calculate_total_score(scanned_books_dict, scores)

    return Solution(new_list, new_score, scanned_books_dict)




def greedy(libraries, n_days, scores):
    day = 0
    solution = [-1 for i in range(n_days)]
    scanned_books_set = set()
    scanned_books_dict = dict()
    all_libraries = copy.deepcopy(libraries)

    while day < n_days and len(all_libraries)>0:
        lib_id = choose_best_score(n_days - day, all_libraries, scores, scanned_books_set)
        if lib_id == -1:
            break
        lib = libraries[lib_id]
        scanned_books_dict[lib_id] = lib.get_books(n_days-day)
        scanned_books_set.update(scanned_books_dict[lib_id])
        for _ in range(lib.signup_days):
            solution[day] = lib_id
            day += 1
        all_libraries.remove(lib)

    return Solution(solution, score(scanned_books_set, scores), scanned_books_dict)


# T/(1+t) , funçao de cooling t é a iteraçao , funçao probabilidade do enunciado T = 100 inicial
# TabuSearch simulated annealing 