import math
import random

from library import Library
from solution import Solution


# creates solution with the given libraries and scores
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


# calculates the total score of the libraries
def score(books, scores):
    return sum([scores[b] for b in books])


# given a list of libraries, number of remaining days and the books already scanned, finds the best library to sign up (compares scores)
def choose_best_score(days, libraries, scores, scanned_books):
    best_score = 0
    best_books = []
    best_lib = None
    for library in libraries:
        if library.signup_days > days:
            continue
        books = library.get_books(days, scanned_books)
        s = score(books, scores) / library.signup_days
        if s > best_score:
            best_lib = library.id
            best_score = s
            best_books = books

    if best_lib is None:
        return -1, best_books

    return best_lib, best_books


# function to calculate the if the solution is accepted with a certain probability
def accept_with_probability(delta, t):
    r = random.randrange(0, 1)
    f = math.exp(delta / t)
    if f >= r:
        return True
    else:
        return False


# function that creates the list of libraries with the file information
def read_libraries(lines, n_libraries, scores):
    libraries = []
    for i in range(0, n_libraries):
        info = lines[i * 2].split()
        books = sorted([int(n) for n in lines[i * 2 + 1].split()], key=lambda x: scores[x], reverse=True)
        libraries.append(Library(i, books, int(info[1]), int(info[2])))

    return libraries
