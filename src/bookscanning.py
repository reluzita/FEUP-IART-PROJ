import sys
from library import Library 
from solution import Solution
from utils import find_best_neighbour, calculate_total_score, choose_best_score, find_first_neighbour, random_walk, score, generate_solution
from io_funcs import scan_file, write_output
import datetime
import copy
from utils import greedy
from genetic_algorithm import genetic_algorithm, generate_random, mutate_solution

def getElapsedTime(t):
    return datetime.datetime.now() - t

def bookScanning(inputfile, algorithm):
    n_books, n_libraries, n_days, scores, libraries, printLibraries = scan_file("input/" + inputfile)

    print("\n***", inputfile, "***")

    t = datetime.datetime.now()

    all_libraries = copy.deepcopy(libraries)

    solution = greedy(all_libraries, n_days, scores)
    best_solution = solution

    if algorithm != 1:
        print("\n--------------------------")
        print("Greedy is done, optimizing now!")
        print("-------------------------- ")

        found_better = True

        if algorithm == 2:
         while found_better:
             found_better, solution = find_first_neighbour(solution, libraries, scores, n_days)

        if algorithm == 3:
         while found_better:
             found_better, solution = find_best_neighbour(solution, libraries, scores, n_days)

        
        if algorithm == 4:
            for _ in range(1000):
                solution = random_walk(solution, libraries, scores, n_days)
                if solution.score > best_solution.score:
                    best_solution = solution
                print(solution.score)
    


    libraries_list = []
    for lib in best_solution.sol:
        if lib not in libraries_list and lib != -1:
            libraries_list.append(lib)
    
    elapsed_time = datetime.datetime.now() - t
    print("Elapsed time: " + str(elapsed_time))
    print(best_solution.score)

    write_output(inputfile, libraries_list, best_solution.books2lib)

def genetic(inputfile):
    n_books, n_libraries, n_days, scores, libraries, printLibraries = scan_file("input/" + inputfile)
    population_size = 20
    generations = 10
    mutation_prob = 0.1
    swap_prob = 0.1


    print("\n***", inputfile, "***")
    t = datetime.datetime.now()

    greedy_solution = greedy(libraries, n_days, scores)
    print("found greedy")
    population = [greedy_solution]
    #population = []
    for i in range(population_size-1):
        new_solution = mutate_solution(greedy_solution.sol, libraries, 0.1)
        population.append(generate_solution(new_solution, libraries, scores))

    print("population done")
    for i in range(generations):
        new_population = genetic_algorithm(population, libraries, scores, mutation_prob, swap_prob)
        population = []
        for s in new_population:
            if s in population:
                best = sorted(new_population, key=lambda x: x.score, reverse=True)[0]
                new_solution = mutate_solution(best.sol, libraries, 0.1)
                population.append(generate_solution(new_solution, libraries, scores))
            else:
                population.append(s)

        best = sorted(population, key=lambda x: x.score, reverse=True)[0]
        mean = sum([x.score for x in population])/len(population)

        print(i, "- max:", best.score, "avg:", mean)

    elapsed_time = datetime.datetime.now() - t
    print("Elapsed time: " + str(elapsed_time))

    best = sorted(population, key=lambda x: x.score, reverse=True)[0]
    libraries_list = []
    for lib in best.sol:
        if lib not in libraries_list and lib != -1:
            libraries_list.append(lib)

    write_output(inputfile, libraries_list, best.books2lib)

