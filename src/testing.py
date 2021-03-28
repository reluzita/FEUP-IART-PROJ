import sys
from library import Library 
from solution import Solution
from utils import greedy
from io_funcs import scan_file, write_output
import datetime
import copy
import random
from genetic_algorithm import genetic_algorithm, generate_random

def genetic(inputfile):
        
    n_books, n_libraries, n_days, scores, libraries, printLibraries = scan_file("input/" + inputfile)
    population_size = 50
    generations = 1000
    mutation_prob = 0.05
    swap_prob = 0.05


    print("\n***", inputfile, "***")
    t = datetime.datetime.now()

    population = [greedy(libraries, n_days, scores)]
    #population = []
    for i in range(population_size-1):
        population.append(generate_random(n_days, libraries, scores))

    for i in range(generations):
        new_population = genetic_algorithm(population, libraries, scores, mutation_prob, swap_prob)
        population = []
        for s in new_population:
            if s in population:
                population.append(generate_random(n_days, libraries, scores))
            else:
                population.append(s)

        best = sorted(population, key=lambda x: x.score, reverse=True)[0]
        mean = sum([x.score for x in population])/len(population)
        #print(i, "-", mean)
        print(i, "-", best.score)

    elapsed_time = datetime.datetime.now() - t
    print("Elapsed time: " + str(elapsed_time))