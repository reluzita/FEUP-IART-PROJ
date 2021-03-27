import sys
from library import Library 
from solution import Solution
from utils import find_best_neighbour, calculate_total_score, choose_best_score, find_first_neighbour, random_walk
from io_funcs import scan_file, write_output
import datetime
import copy
from utils import greedy

def getElapsedTime(t):
    return datetime.datetime.now() - t

def bookScanning(inputfile):
    n_books, n_libraries, n_days, scores, libraries, printLibraries = scan_file("input/" + inputfile)

    print("\n***", inputfile, "***")

    # t = datetime.datetime.now()

    all_libraries = copy.deepcopy(libraries)

    solution = greedy(all_libraries, n_days, scores)

    print("\n--------------------------")
    print("Greedy is done, optimizing now!")
    print("-------------------------- ")

    found_better = True
    while found_better: #implementing the decided local search variation
        found_better, solution = find_best_neighbour(solution, libraries, scores, n_days)

    # for _ in range(1000):
    #     solution = random_walk(solution, libraries, scores, n_days)
    #     if solution.score > best_solution.score:
    #         best_solution = solution
    #     print(solution.score)
    
    libraries_list = []
    for lib in solution.sol:
        if lib.id not in libraries_list and lib != -1:
            libraries_list.append(lib.id)
    write_output(inputfile, libraries_list, solution.books2lib)

