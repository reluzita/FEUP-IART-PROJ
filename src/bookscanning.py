import copy
import datetime

from genetic_algorithm import genetic_algorithm, mutate_solution, generate_random
from io_funcs import scan_file, write_output, read_output
from utils import find_best_neighbour, find_first_neighbour, generate_solution, simulated_annealing, random_neighbour
from utils import greedy


def get_elapsed_time(t):
    return datetime.datetime.now() - t


def book_scanning(inputfile, algorithm, greedy_injection):
    n_days, scores, libraries = scan_file("input/" + inputfile)

    t = datetime.datetime.now()

    solution = None
    if algorithm == 1:
        all_libraries = copy.deepcopy(libraries)
        solution = greedy(all_libraries, n_days, scores)
    else:
        if greedy_injection:
            solution = read_output("greedy/" + inputfile, libraries, scores)
        else:
            solution = generate_random(n_days, libraries, scores)

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
            for _ in range(30):
                new_solution = random_neighbour(solution, libraries, scores, n_days, True)
                if new_solution.score > solution.score:
                    print("Found better:", new_solution.score)
                    solution = new_solution

        if algorithm == 5:
            solution = simulated_annealing(solution, libraries, scores, n_days)

    elapsed_time = datetime.datetime.now() - t
    solution.print_solution(elapsed_time)

    write_output(inputfile, solution)


def genetic(inputfile, population_size, generations, mutation_prob, swap_prob, population_variation):
    _, scores, libraries = scan_file("input/" + inputfile)

    print(population_size, generations, mutation_prob, swap_prob, population_variation)

    t = datetime.datetime.now()

    greedy_solution = read_output("greedy/" + inputfile, libraries, scores)
    print("found greedy")
    population = [greedy_solution]

    for i in range(population_size - 1):
        new_solution = mutate_solution(greedy_solution.libraries_list, libraries, population_variation)
        population.append(generate_solution(new_solution, libraries, scores))
        print("generated solution")

    print("population done")

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

        print(i, "- max:", best.score, "avg:", mean)

    elapsed_time = datetime.datetime.now() - t

    best = sorted(population, key=lambda x: x.score, reverse=True)[0]

    best.print_solution(elapsed_time)

    write_output(inputfile, best)
