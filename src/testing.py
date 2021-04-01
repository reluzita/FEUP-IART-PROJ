import datetime

import matplotlib.pyplot as plt

from genetic_algorithm import genetic_algorithm, mutate_solution, generate_random
from io_funcs import scan_file
from utils import generate_solution

if __name__ == "__main__":
    n_days, scores, libraries = scan_file("input/f_libraries_of_the_world.txt")

    population_size, generations, mutation_prob, swap_prob, population_variation = get_parameters(
        "f_libraries_of_the_world.txt")

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

    elapsed_time = datetime.datetime.now() - t

    best = sorted(population, key=lambda x: x.score, reverse=True)[0]

    best.printSol(elapsed_time)

    gen_list = range(generations)
    plt.plot(gen_list, best_scores, 'r', gen_list, avg_scores, 'b')
    plt.ylabel('scores')
    plt.xlabel('generations')
    plt.show()