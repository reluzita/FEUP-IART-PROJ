import sys
from library import Library 
from solution import Solution
from utils import greedy, score, generate_solution, find_first_neighbour, find_best_neighbour, random_neighbour, cooling_function, accept_with_probability
from genetic_algorithm import generate_random
from io_funcs import scan_file, write_output, read_output
import datetime

import matplotlib.pyplot as plt


if __name__ == "__main__":
    n_days, scores, libraries = scan_file("input/e_so_many_books.txt")
    
    solution = generate_random(n_days, libraries, scores)

    t1 = datetime.datetime.now()

    best_scores = []
    all_scores = []
    iterations = []
    i = 0

    not_accepted = 0
    time = 0

    while not_accepted < 30:
        new_solution = random_neighbour(solution, libraries, scores, n_days) # gets new solution using random_descendent on previous found solution
        t = cooling_function(time)
        
        if t < 0.01: break # no need to keep trying to "cool down"
        delta = new_solution.score - solution.score

        if delta <= 0 and not accept_with_probability(delta, t): 
            not_accepted += 1
        else:
            solution = new_solution
            print("Found better:", solution.score)

        time += 1

        iterations.append(i)
        all_scores.append(new_solution.score)
        best_scores.append(solution.score)
        i+=1
 


    """
    population_size, generations, mutation_prob, swap_prob, population_variation = get_parameters("e_so_many_books.txt")

    print(population_size, generations, mutation_prob, swap_prob, population_variation)

    t = datetime.datetime.now()

    population = []

    for i in range(population_size):
        population.append(generate_random(n_days, libraries, scores))

    print("population done")
    best_scores = []
    avg_scores = []
    for i in range(generations):
        new_population = genetic_algorithm(population, libraries, scores, mutation_prob, swap_prob,
                                           population_variation)
        population = []
        for s in new_population:
            if s in population:
                best = sorted(new_population, key=lambda x: x.score, reverse=True)[0]
                new_solution = mutate_solution(best.libraries_list, libraries, 0.1)
                population.append(generate_solution(new_solution, libraries, scores))
            else:
                population.append(s)

        best = sorted(population, key=lambda x: x.score, reverse=True)[0]
        mean = sum([x.score for x in population]) / len(population)

        best_scores.append(best.score)
        avg_scores.append(mean)

        print(i, "- max:", best.score, "avg:", mean)
    """
    
    elapsed_time = datetime.datetime.now() - t1

    #best = sorted(population, key=lambda x: x.score, reverse=True)[0]

    solution.printSol(elapsed_time)

    #gen_list = range(generations)
    plt.plot(iterations, best_scores, 'r', iterations, all_scores, 'b')
    plt.ylabel('scores')
    plt.xlabel('iterations')
    plt.show()
    
                    
    
    
