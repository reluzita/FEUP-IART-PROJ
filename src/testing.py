import sys
from library import Library 
from solution import Solution
from utils import greedy, score, generate_solution
from io_funcs import scan_file, write_output, read_output
import datetime
import copy
import random
from genetic_algorithm import genetic_algorithm, mutate_solution, generate_random, crossover

if __name__ == "__main__":
    n_books, n_libraries, n_days, scores, libraries = scan_file("input/d_tough_choices.txt")

    t = datetime.datetime.now()

    solution = greedy(libraries, n_days, scores)

    elapsed_time = datetime.datetime.now() - t
    print("Elapsed time: " + str(elapsed_time))
    print("Score: ", solution.score)
    write_output("d_tough_choices.txt", solution)
    
                    
    
    
