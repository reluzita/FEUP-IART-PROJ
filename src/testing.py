import sys
from library import Library 
from solution import Solution
from utils import greedy, score
from io_funcs import scan_file, write_output
import datetime
import copy
import random
from genetic_algorithm import genetic_algorithm, mutate_solution, generate_random

if __name__ == "__main__":
    if len(sys.argv[1:]) != 1:
        print("Usage: testing.py <inputfile>")
        sys.exit()
    
    inputfile = sys.argv[1]

    n_books, n_libraries, n_days, scores, libraries, printLibraries = scan_file("input/" + inputfile)

    population_size = 10
    generations = 1000
    mutation_prob = 0.05
    swap_prob = 0.05
    
    greedy_solution = greedy(libraries, n_days, scores)
    print("found greedy")
    population = [greedy_solution]
    for i in range(population_size-1):
        new_solution = mutate_solution(greedy_solution.sol, libraries, 0.1)
        day = 0 
        books2lib = dict()
        books = set()
        while day < n_days:
            lib = new_solution[day]
            books2lib[lib] = libraries[lib].get_books(n_days - day)
            books.update(books2lib[lib])
            day += libraries[lib].signup_days

        population.append(Solution(new_solution, score(books, scores), books2lib))
    
    for solution in population:
        print(solution.score)