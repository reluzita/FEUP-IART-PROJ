from library import Library
import copy
from solution import Solution
import random
import math

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
    best_score = 0
    best_books = []
    best_lib = None
    for library in libraries:
        if library.signup_days > days: continue
        books = [b for b in library.get_books(days) if b not in scanned_books]
        s = score(books, scores) /library.signup_days
        if s > best_score:
            best_lib = library.id
            best_score = s
            best_books = books 
    
    if best_lib == None:
        return -1, best_books

    return best_lib, best_books


def read_libraries(lines, n_libraries, scores):
    libraries = []
    for i in range(0, n_libraries):
        info = lines[i*2].split()
        books = sorted([int(n) for n in lines[i*2+1].split()], key=lambda x: scores[x], reverse=True)
        libraries.append(Library(i, books, int(info[1]), int(info[2])))
        
    return libraries

def find_best_neighbour(solution, libraries, scores, n_days):
    best_score = solution.score
    best_libraries = copy.deepcopy(solution.libraries_list)
    best_books = copy.deepcopy(solution.books2lib)
    found_better = False

    libraries_set = set(solution.libraries_list)
    if -1 in libraries_set: 
        libraries_set.remove(-1)

    for current_lib in libraries_set:
        day = 0
        new_list = []
        scanned_books_dict = dict()
        scanned_books_set = set()
        all_libraries = copy.deepcopy(libraries)

        while day < len(solution.libraries_list):
            lib = solution.libraries_list[day]
            if lib == -1: 
                break
            elif lib == current_lib:
                all_libraries.remove(libraries[lib])
                break
            else:
                scanned_books_dict[lib] = solution.books2lib[lib]
                scanned_books_set.update(scanned_books_dict[lib])
                for _ in range(libraries[lib].signup_days):
                    new_list.append(lib)
                    day += 1
                all_libraries.remove(libraries[lib])

        
        while day < n_days and len(all_libraries) > 0:
            lib_id, books = choose_best_score(n_days - day, all_libraries, scores, scanned_books_set)
            if lib_id == -1:
                break
            
            scanned_books_dict[lib_id] = books
            scanned_books_set.update(books)
            new_list.append(libraries[lib_id])
            day += libraries[lib_id].signup_days
            all_libraries.remove(libraries[lib_id])

        new_score = score(scanned_books_set, scores)
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
    libraries_set = set(solution.libraries_list)
    if -1 in libraries_set: 
        libraries_set.remove(-1)

    for current_lib in libraries_set:
        day = 0
        new_list = []
        scanned_books_dict = dict()
        scanned_books_set = set()
        all_libraries = copy.deepcopy(libraries)

        while day < len(solution.libraries_list):
            lib = solution.libraries_list[day]
            if libraries == -1: 
                break
            elif lib == current_lib:
                all_libraries.remove(libraries[lib])
                break
            else:
                scanned_books_dict[lib] = solution.books2lib[lib]
                scanned_books_set.update(scanned_books_dict[lib])
                for _ in range(libraries[lib].signup_days):
                    new_list.append(lib)
                    day += 1
                all_libraries.remove(libraries[lib])

        while day < n_days and len(all_libraries) > 0:
            lib_id, books = choose_best_score(n_days - day, all_libraries, scores, scanned_books_set)
            if lib_id == -1:
                break
            
            scanned_books_dict[lib_id] = books
            scanned_books_set.update(books)
            for _ in range(libraries[lib_id].signup_days):
                new_list.append(lib_id)
                day += 1
            all_libraries.remove(libraries[lib_id])

        new_score = score(scanned_books_set, scores)
        if new_score > solution.score:
            print("better!")
            return True, Solution(new_list, new_score, scanned_books_dict)
        else:
            print("not better :(")

    return False, solution

def choose_random_neighbour(libraries, libraries_set, n_days):
    tries = 0

    while(tries < 100000):
        rand = random.sample(libraries_set, 1)
        if libraries[rand[0]].signup_days < n_days:
            return rand[0]
    return 0


def random_neighbour(solution, libraries, scores, n_days):
    libraries_set = set(solution.libraries_list)
    if -1 in libraries_set: 
        libraries_set.remove(-1)

    current_lib = choose_random_neighbour(libraries, libraries_set, n_days)
    day = 0
    new_list = []
    scanned_books_dict = dict()
    scanned_books_set = set()
    all_libraries = copy.deepcopy(libraries)

    while day < len(solution.libraries_list):
            lib = solution.libraries_list[day]
            if libraries == -1: 
                break
            elif lib == current_lib:
                all_libraries.remove(libraries[lib])
                break
            else:
                scanned_books_dict[lib] = solution.books2lib[lib]
                scanned_books_set.update(scanned_books_dict[lib])
                for _ in range(libraries[lib].signup_days):
                    new_list.append(lib)
                    day += 1
                all_libraries.remove(libraries[lib])

    while day < n_days and len(all_libraries) > 0:
        lib_id, books = choose_best_score(n_days - day, all_libraries, scores, scanned_books_set)
        if lib_id == -1:
            break
        
        scanned_books_dict[lib_id] = books
        scanned_books_set.update(books)
        for _ in range(libraries[lib_id].signup_days):
            new_list.append(lib_id)
            day += 1
        all_libraries.remove(libraries[lib_id])

    new_score = score(scanned_books_set, scores)

    return Solution(new_list, new_score, scanned_books_dict)


def greedy(libraries, n_days, scores):
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

    return Solution(solution, score(scanned_books_set, scores), scanned_books_dict)

 
def cooling_function(t):    #30 iteraçoes
    temp = 300
    return temp / (1 + t)
    

def accept_with_probability(delta, t):
    r = random.randrange(0,1)
    f = math.exp( delta / t)
    if f >= r: 
        return True
    else: return False



def simulated_annealing(solution, libraries, scores, n_days):
    best_score = solution.score
    not_accepted = 0

    for time in range(500):
        new_solution = random_neighbour(solution, libraries, scores, n_days)

        t = cooling_function(time)
        if t < 0.01: break
        delta = new_solution.score - best_score

        if delta <= 0 and not accept_with_probability(delta, t): 
            not_accepted += 1
            if not_accepted > 30: break
            continue
        else:
            best_score = new_solution.score
            solution = new_solution
            print(best_score)
 
    return solution