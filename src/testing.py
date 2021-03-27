import sys
from library import Library 
from solution import Solution
from utils import greedy, score
from io_funcs import scan_file, write_output
import datetime
import copy
import random
from genetic_algorithm import genetic_algorithm, mutate_solution, generate_random

def genetic(inputfile):
        
    n_books, n_libraries, n_days, scores, libraries, printLibraries = scan_file("input/" + inputfile)
    population_size = 10
    generations = 1000
    mutation_prob = 0.05
    swap_prob = 0.05


    print("\n***", inputfile, "***")
    t = datetime.datetime.now()

    greedy_solution = greedy(libraries, n_days, scores)
    print("found greedy")
    population = [greedy_solution]
    #population = []
    for i in range(population_size-1):
        new_solution = mutate_solution(greedy_solution.sol, libraries, 0.1)
        day = 0 
        books2lib = dict()
        books = set()
        while day < n_days:
            lib = new_solution[day]
            books2lib[lib] = libraries[lib].get_books(n_days - day)
            books.update(books2lib[lib])

        population.append(Solution(new_solution, score(books, scores), books2lib))

    print("population done")
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