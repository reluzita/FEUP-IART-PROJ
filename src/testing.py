import sys
from library import Library 
from solution import Solution
from utils import greedy, score, generate_solution
from io_funcs import scan_file, write_output
import datetime
import copy
import random
from genetic_algorithm import genetic_algorithm, mutate_solution, generate_random, crossover

if __name__ == "__main__":
    inputfile = "f_libraries_of_the_world.txt"

    n_books, n_libraries, n_days, scores, libraries, printLibraries = scan_file("input/" + inputfile)
    
    greedy_solution = greedy(libraries, n_days, scores)
    
    print("done greedy")

    libs = set(greedy_solution.libraries_list)
    if -1 in libs: 
        libs.remove(-1)

    n_books = 0
    scanned_books = set()
    libs2books = dict()
    for lib in libs:
        scanned_books.update(greedy_solution.books2lib[lib])
        for book in libraries[lib].books:
            if book in libs2books:
                libs2books[book].append(lib)
            else:
                libs2books[book] = [lib]
        n_books+=len(greedy_solution.books2lib[lib])
    
    available_books = libs2books.keys()
    best_books = sorted(list(available_books), key=lambda x: scores[x], reverse=True)[:n_books]

    books_to_include = [book for book in best_books if book not in scanned_books]
    books_to_remove = [book for book in scanned_books if book not in best_books]

    for book in books_to_include:
        for lib in libs2books[book]:
            for b in greedy_solution.books2lib[lib]:
                possible_libs = libs2books[b]
                if len(possible_libs) > 1:
                    print("yay?")
                    for lib2 in possible_libs:
                        if lib2 != lib:
                            for b2 in greedy_solution.books2lib[lib2]:
                                if b2 in books_to_remove:
                                    print("yay!")
                    
    
    
    """
    for book in best_books:
        if book not in scanned_books:
            print("book", book, "- score:", scores[book])
            for lib in libs2books[book]:
                if scores[book] > min(scores[x] for x in greedy_solution.books2lib[lib]):
                    print(lib)
    """
