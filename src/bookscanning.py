import copy
import datetime

from genetic_algorithm import genetic_algorithm, mutate_solution, generate_random
from io_funcs import scan_file, write_output, read_output
from utils import find_best_neighbour, find_first_neighbour, generate_solution, simulated_annealing, random_neighbour
from utils import greedy


# calculates the elapsed time given a start datetime
def get_elapsed_time(t):
    return datetime.datetime.now() - t


# function responsible for reading the input file, executing the given algorithm and writing the solution to a file
def book_scanning(inputfile, algorithm, greedy_injection):
    n_days, scores, libraries = scan_file("input/" + inputfile)  # scans the input file and saves all the necessary info

    t = datetime.datetime.now()  # starts the timer

    solution = None
    if algorithm == 1:  # greedy algorithm
        all_libraries = copy.deepcopy(libraries)
        solution = greedy(all_libraries, n_days, scores)  # executes the greedy algorithm to get a solution
    else:
        if greedy_injection:  # use greedy solution to execute a local search or simulated annealing
            print("\n--------------------------------")
            print(" Greedy is done, optimizing now!")
            print("--------------------------------")
            solution = read_output("greedy/" + inputfile, libraries, scores,
                                   n_days)  # reads the file with the greedy solution
        else:
            print("\n--------------------------------------------")
            print(" Random Solution was found, optimizing now!")
            print("--------------------------------------------")
            solution = generate_random(n_days, libraries, scores)  # generates a random solution for the input file

        found_better = True

        if algorithm == 2:  # local search - first neighbour
            while found_better:
                found_better, solution = find_first_neighbour(solution, libraries, scores, n_days)

        elif algorithm == 3:  # local search - best neighbour
            while found_better:
                found_better, solution = find_best_neighbour(solution, libraries, scores, n_days)

        elif algorithm == 4:  # local search - random neighbour
            for _ in range(30):  # executes random neighbour 30 times to give it a chance to find a better solution
                new_solution = random_neighbour(solution, libraries, scores, n_days, True)
                if new_solution.score > solution.score:  # accepts new solution if its score is higher than the previous solution
                    print("Found better:", new_solution.score)
                    solution = new_solution

        if algorithm == 5:  # simulated annealing
            solution = simulated_annealing(solution, libraries, scores, n_days)

    solution.print_solution(get_elapsed_time(t))  # calculates the elapsed time ans prints the solution

    write_output(inputfile, solution)  # writes solution in the respective output file


# function responsible for reading the input file, executing the genetic algorithm and writing the solution to a file
def genetic(inputfile, population_size, generations, mutation_prob, swap_prob, population_variation):
    n_days, scores, libraries = scan_file("input/" + inputfile)  # scans the input file and saves all the necessary info

    t = datetime.datetime.now()  # starts the timer

    greedy_solution = read_output("greedy/" + inputfile, libraries, scores,
                                  n_days)  # reads the file with the greedy solution

    print("\n--------------------------------")
    print(" Greedy is done, optimizing now!")
    print("--------------------------------")

    population = [greedy_solution]  # first population is greedy solution

    for i in range(population_size - 1):  # generates population
        new_solution = mutate_solution(greedy_solution.libraries_list, libraries,
                                       population_variation)  # mutates the greedy solution
        population.append(generate_solution(new_solution, libraries,
                                            scores))  # generates new solution and appends it to the population
        print("generated solution")

    print("population done")

    for i in range(generations):
        new_population = genetic_algorithm(population, libraries, scores, mutation_prob, swap_prob,
                                           population_variation)  # executes the genetic algorithm
        population = []
        for s in new_population:
            if s in population:  # if population contains s, mutates that solution and appends it to population
                best = sorted(new_population, key=lambda x: x.score, reverse=True)[0]  # the best solution is the first one when the array is ordered by scores
                new_solution = mutate_solution(best.libraries_list, libraries, 0.1)  # mutates the solution
                population.append(generate_solution(new_solution, libraries, scores))  # generates new solution and appends it to the population
            else:  # if population does not contains s, appends it
                population.append(s)

        best = sorted(population, key=lambda x: x.score, reverse=True)[0]  # the best solution is the first one when the array is ordered by scores
        mean = sum([x.score for x in population]) / len(population)  # calculates scores mean

        print(i, "- max:", best.score, "avg:", mean)

    elapsed_time = get_elapsed_time(t)  # calculates the elapsed time

    best = sorted(population, key=lambda x: x.score, reverse=True)[0]  # the best solution is the first one when the array is ordered by scores

    best.print_solution(elapsed_time)  # prints the solution

    write_output(inputfile, best)
