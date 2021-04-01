import datetime

from genetic_algorithm import genetic_algorithm, mutate_solution, generate_random
from io_funcs import scan_file
from utils import generate_solution

if __name__ == "__main__":
    n_days, scores, libraries = scan_file("input/b_read_on.txt")

    population_size, generations, mutation_prob, swap_prob, population_variation = get_parameters(inputfile)

    print(population_size, generations, mutation_prob, swap_prob, population_variation)

    t = datetime.datetime.now()

    population = []

    for i in range(population_size):
        population.append(generate_random(n_days, libraries, scores))

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
