from bookscanning import book_scanning, genetic
from genetic_algorithm import get_parameters


def choice_input(min_value, max_value):
    user_in = input("Insert a number from the menu: ")
    while True:
        try:
            val = int(user_in)
            if val < min_value or val > max_value:
                user_in = input("Invalid input, please insert a valid one: ")
            else:
                break
        except ValueError:
            user_in = input("Invalid input, please insert a valid one: ")

    return val


def value_input(value, default, is_integer, min_value, max_value):
    user_in = input("\nInsert a value for " + value + " (default value: " + str(default) + "): ")

    while True:
        try:
            val = int(user_in) if is_integer else float(user_in)
            if val < min_value or val > max_value:
                user_in = input(
                    "Invalid input, please insert a valid one (min: " + str(min_value) + ", max: " + str(
                        max_value) + "): ")
            else:
                break
        except ValueError:
            user_in = input(
                "Invalid input, please insert a valid one (min: " + str(min_value) + ", max: " + str(max_value) + "): ")

    return val


def print_menu(options, message):
    print("\n***************************************")
    print(message, '\n')

    for key, value in options.items():
        print(key + ". " + value)
    print("\n***************************************")

    return choice_input(1, len(options))


# ##############################################################################################################################################################################

def best_scores():
    print("\n***************************************")
    print(" Best Scores\n")

    print(" File                         | Score     | Algorithm")
    print("-------------------------------------------------------------------")
    print(" a_example.txt                |        21 | Greedy")
    print(" b_read_on.txt                | 5 822 900 | Greedy")
    print(" c_incunabula.txt             | 5 689 952 | Random Neighbor")
    print(" d_tough_choices.txt          | 5 028 530 | Greedy")
    print(" e_so_many_books.txt          | 5 037 291 | Genetic")
    print(" f_libraries_of_the_world.txt | 5 329 948 | Simulated Annealing")

    print("\n***************************************")
    input("Press enter to return to main menu...")
    return 0


# ##############################################################################################################################################################################

def main_menu():
    options = {"1": "Choose an input file", "2": "See the best score for each file", "3": "Exit"}
    message = "What do you want to do:"
    choice = print_menu(options, message)

    if choice == 3:
        return -1
    return choice


def file_menu():
    files = {"1": "a_example.txt", "2": "b_read_on.txt", "3": "c_incunabula.txt", "4": "d_tough_choices.txt",
             "5": "e_so_many_books.txt", "6": "f_libraries_of_the_world.txt", "7": "Return to main menu"}
    message = "Choose an input file:"
    choice = print_menu(files, message)

    if choice == 7:
        return 0
    return files[str(choice)]


def algorithm_menu(file):
    algorithms = {"1": "Greedy", "2": "Local Search - First Neighbour", "3": "Local Search - Best Neighbour",
                  "4": "Local Search - Random Neighbour", "5": "Simulated Annealing", "6": "Genetic",
                  "7": "Choose another file"}
    message = "Choose the algorithm to apply to " + file + ": "

    while True:
        algorithm = print_menu(algorithms, message)
        if algorithm == 7:
            break

        if algorithm == 1:
            print("\n***************************************")
            print("Applying " + algorithms[str(algorithm)] + " to " + file, '\n')
            book_scanning(file, algorithm, False)

        elif 2 <= algorithm <= 5:
            options = {"1": "Use greedy solution", "2": "Use random solution"}
            message = "What do you want to do?"
            option = print_menu(options, message)

            greedy_injection = True if option == 1 else False

            print("\n***************************************")
            print("Applying " + algorithms[str(algorithm)] + " to " + file, '\n')
            book_scanning(file, algorithm, greedy_injection)

        elif algorithm == 6:
            menu_genetic(file)

        print("\n***************************************")
        input("Press enter to return to algorithms menu...")

    return 1


def menu_genetic(file):
    options = {"1": "Use default values", "2": "Personalize values"}
    message = "Genetic uses constant values for population size, number of generations, mutation and swap " \
              "probabilities and population variation. \nWhat do you want to do? "
    choice = print_menu(options, message)

    population_size, generations, mutation_prob, swap_prob, population_variation = get_parameters(file)

    if choice == 2:
        print("\n***************************************")
        population_size = value_input("Population Size", population_size, True, 6, 100)
        generations = value_input("Number of Generations", generations, True, 10, 1000)
        mutation_prob = value_input("Mutation Probability", mutation_prob, False, 0, 1)
        swap_prob = value_input("Swap Probability", swap_prob, False, 0, 1)
        population_variation = value_input("Population Variation", population_variation, False, 0, 1)

    print("\n***************************************")
    print("Applying Genetic to " + file, '\n')
    genetic(file, population_size, generations, mutation_prob, swap_prob, population_variation)


# ##############################################################################################################################################################################

def menu():
    current_menu = 0
    file = "a_example.txt"

    while current_menu != -1:
        if current_menu == 0:  # main menu
            current_menu = main_menu()

        elif current_menu == 1:  # files menu
            file = file_menu()
            if file == 0:
                current_menu = 0
            else:
                current_menu = 3

        elif current_menu == 2:  # best scores
            current_menu = best_scores()

        elif current_menu == 3:  # algorithm menu
            current_menu = algorithm_menu(file)
